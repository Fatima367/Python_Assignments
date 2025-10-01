import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, 
    RunContextWrapper, ModelSettings,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered,
    input_guardrail, function_tool, enable_verbose_stdout_logging,
    set_default_openai_api, set_default_openai_client, set_tracing_disabled
    )


# Configurations

load_dotenv()
set_default_openai_api("chat_completions")

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, check your .env file")


external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


model= OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)


set_default_openai_client(external_client)
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()


# UserInfo class for Context

class UserInfo(BaseModel):
    member_id: int
    name: str = "guest"
    is_resgistered: bool = False
    


# Output Type of Input Guardrail Agent

class InputInfo(BaseModel):
    related_to_library: bool
    reason: str


# Guardrail Agent

guardrail_agent= Agent(
    name= "Input Guardrail",
    instructions="You are a guardrail agent you check if the user is asking questions related to library or books",
    output_type= InputInfo,
    model= model
)
 

# Input Guardrail

@input_guardrail
async def input_check(wrapper: RunContextWrapper, agent: Agent, input) -> RunContextWrapper:

    response = await Runner.run(guardrail_agent, input, context= wrapper.context)

    print(f"[DEBUG]   {response.final_output.reason}")

    return GuardrailFunctionOutput(
        output_info= response.final_output,
        tripwire_triggered= not response.final_output.related_to_library
    )


def is_user_registered(wrapper: RunContextWrapper, agent: Agent):

    if wrapper.context.is_resgistered == True:
        return True
    else:
        return False
    

def get_books_data():
    with open("books.py", 'r') as file:
        return file


# Function tools for Agent

@function_tool(is_enabled= is_user_registered)
def check_book_availaibility():
    """Checks book availability"""
    books = get_books_data()
    return books


@function_tool
def search_books():
    """Searchs for books"""
    books = get_books_data()
    return books


@function_tool
def get_timings():
    
    timings = {
        "opening": "8:00 AM",
        "closing": "8:00 PM"
    }

    return timings


# Dynamic Instructions

def dynamic_instructions(wrapper: RunContextWrapper, agent: Agent):
    return f"""You are a Library Assitant. Greet users with their name i.e {wrapper.context.name}
            You help users with all the Library related questions, using tools. 
            - Search for book in the library using `search_books` only if not, say we don't have this book.
            - Donot tell about the 'availaibility' of any book without using `check_book_availaibility` if you don't have this tool tell the user only registered members can now about book availability.
            """


def main():
    
    # Main Agent

    agent = Agent(
        name= "Library Assistant",
        instructions= dynamic_instructions,
        tools=[check_book_availaibility, search_books, get_timings],
        input_guardrails= [input_check],
        model= model,
        model_settings= ModelSettings(temperature= 0.5)
    )


    # User Context

    user1 = UserInfo(member_id= 497)

    while True:
        print("Enter 'q' to quit.")
        user_input= input("Enter your message: ")

        if user_input.lower() == 'q':
            print("Quitting...\nGood Bye!")
            break

        try:
            result = Runner.run_sync(
                agent, 
                user_input, 
                context= user1, 
                )
            print(f"\n{result.final_output}")
        
        except InputGuardrailTripwireTriggered as e:
            print("Library Assistant didn't respond to irrelevant questions")
        

if __name__ == "__main__":
    main()