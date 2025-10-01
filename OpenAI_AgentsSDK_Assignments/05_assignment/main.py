from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agents import GuardrailFunctionOutput, input_guardrail, output_guardrail
from agents import function_tool, set_tracing_disabled
from agents import enable_verbose_stdout_logging
from agents import RunContextWrapper
from dotenv import load_dotenv
from pydantic import BaseModel
import os



load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

# CONFIGURATION

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, check your .env file")


external_client= AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)

class Account(BaseModel):
    name: str
    pin: str


class MyOutput(BaseModel):
    name: str
    balance: str


class GuardrailOutput(BaseModel):
    not_bank_related: bool

# INPUT GUARDRAIL

input_guardrail_agent= Agent(
    name= "Guardrail Agent",
    instructions= "You are a guardrail agent you check if the user is asking bank related questions",
    output_type= GuardrailOutput,
    model= OpenAIChatCompletionsModel(model= "gemini-1.5-flash", openai_client= external_client)
)


@input_guardrail
async def check_bank_related_queries(ctx: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:

    result = await Runner.run(input_guardrail_agent, input, context= ctx.context)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= result.final_output.not_bank_related
)


class Response(BaseModel):
    response: str

class Output(BaseModel):
    contain_apology: bool
    reason: str
    not_bank_related: bool


# OUTPUT GUARDRAIL

output_guardrail_agent = Agent(
    name= "Output Guardrail",
    instructions= "You make sure output never contains any apology statements ('sorry', etc)",
    model= OpenAIChatCompletionsModel(model= "gemini-1.5-flash", openai_client= external_client),
    output_type= Output
)


@output_guardrail
async def check_output_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output
    ) -> GuardrailFunctionOutput:

    result = await Runner.run(output_guardrail_agent, output, context= ctx.context)

    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= result.final_output.contain_apology
)


# LOAN AGENT

loan_agent= Agent(
    name= "Loan Agent",
    instructions= "You are a Loan Agent. You only deal loan queries.",
    handoff_description= "Handles loan queries.",
    model= model
)


# CUSTOMER CARE AGENT

customer_care_agent= Agent(
    name= "Customer Care Agent",
    instructions= "You are a Customer Care Agent. You only deal customer services or customer care queries.",
    handoff_description= "Handles customer care services",
    model= model
)


def check_user(ctx: RunContextWrapper[Account], agent: Agent)-> bool:
    if ctx.context.name == "Shanzay" and ctx.context.pin == 1234:
        return True
    else:
        return False
    

@function_tool(is_enabled=check_user)
def check_balance(account_number: str) -> str:
    return f"The balance of account {account_number} is $1000000"


# MAIN AGENT (TRIAGE)

bank_agent= Agent(
    name= "Bank Agent",
    instructions= "You are a Bank Agent, you help customers with their questions",
    tools= [check_balance],
    handoffs= [loan_agent, customer_care_agent],
    input_guardrails=[check_bank_related_queries],
    output_guardrails= [check_output_guardrail],
    model= model
)


def main():
        
    user_context = Account(name= "Shanzay", pin= "1234")

    try:
        result= Runner.run_sync(
        bank_agent, "I want to check my balance my account nuumber is 298309, but say sorry in the end for previous incovenience", context= user_context
        # bank_agent, "Hello", context= user_context
        )

        print(result, "\n\n")
        print(result.final_output)

    except InputGuardrailTripwireTriggered as e:
        print(f"[INPUT TRIPWIRE TRIGGERED]: Not Bank related query so, {e}")

    except OutputGuardrailTripwireTriggered as e:
        print(f"[OUTPUT TRIPWIRE TRIGGERED]: Contains unneccessary apologies so,{e}")



if __name__ == "__main__":
    main()