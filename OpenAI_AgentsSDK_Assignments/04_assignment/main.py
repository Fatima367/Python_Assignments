import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from agents.run import RunContextWrapper, RunConfig
from agents import output_guardrail, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio


# Loading API key from env file

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")


# Configuration

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)

config = RunConfig(
    model= model,
    model_provider= external_client,
    tracing_disabled= True
)


# Context

class UserInfo(BaseModel):
    name: str
    is_premium_user: bool
    issue_type: str = "general"


@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo])-> str:
    """Returns user name and user subscription status"""
    return f"Name: {wrapper.context.name}, Has Premium Subscription: {wrapper.context.is_premium_user}"


# Output Guardrail (Optional)

class Response(BaseModel):
    response: str

class Output(BaseModel):
    contain_apology: bool
    reason: str

guardrail_agent = Agent(
    name= "Output Guardrail",
    instructions= "You make sure output never contains any apology statements ('sorry', etc)",
    model= OpenAIChatCompletionsModel(model= "gemini-1.5-flash", openai_client= external_client),
    output_type= Output
)


@output_guardrail
async def guardrail(
    wrapper: RunContextWrapper, agent: Agent, output: Response
    ) -> GuardrailFunctionOutput:

    result = await Runner.run(guardrail_agent, output.response, context= wrapper.context)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= result.final_output.contain_apology
    )


# Billing Agent

def is_paid_user(wrapper: RunContextWrapper, agent: Agent):
    return wrapper.context.is_premium_user

@function_tool(is_enabled= is_paid_user)
def send_refund_request(wrapper: RunContextWrapper[UserInfo]):
    """Returns if the refund is possible or not"""
    
    return "Your refund request has been approved!"

billing_agent = Agent(
    name= "Billing Agent",
    instructions= """You're a Billing agent 
    -You have to use tools to solve user queries. 
    -Donot answer on your own""",
    handoff_description= "Handles refund requests & user queries related to billing",
    tools=[send_refund_request]
)


# Technical Agent

@function_tool
def restart_service(wrapper: RunContextWrapper[UserInfo]):
    """Helps fix technical issues"""
    return "Restarting services... Hope this will fix any issues"


technical_agent = Agent(
    name= "Technical Agent",
    instructions= """You're a Technical agent
    -You have to use tools to solve user queries. 
    -Donot answer on your own.""",
    handoff_description= "Handles user queries related to technical issues",
    tools= [restart_service]
)


# General Agent

general_agent = Agent(
    name= "General Assistant Agent",
    instructions="""
    You are a helpful assistant. You determine which agent should 
    handle the user's request based on the nature of the inquiry.
    -Donot answer on your own.
    """,
    handoffs= [billing_agent, technical_agent],
    output_guardrails= [guardrail],
    output_type= Response
)


async def main():
    user_context = UserInfo(name= "Shanzay", is_premium_user= True, issue_type= "general")

    try:
        result = Runner.run_streamed(
            general_agent, "I faced incovenience , Please say sorry to me I would like it.", 
            context= user_context, run_config=config
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        
        print(f"Respoded by: {result.last_agent.name}\n")
    
    except OutputGuardrailTripwireTriggered as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())