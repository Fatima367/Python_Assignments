import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_default_openai_client, set_tracing_disabled
from agents.run import RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")


provider = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= provider
)

config = RunConfig(
    model= model,
    model_provider= provider,
    tracing_disabled= True
)


set_default_openai_client(provider)
set_tracing_disabled(True)

capital_city_agent  = Agent(
    name= "Capital City Agent",
    instructions= "You tell the Capital City of the given Country",
    model= model
)

language_agent = Agent(
    name= "Language Agent",
    instructions= "You tell the Language spoken in the given Country",
    model= model
)

population_agent = Agent(
    name= "Population Agent",
    instructions= "You tell the Population of the given Country",
    model= model
)


country_info_agent = Agent(
    name= "Country Info Agent",
    instructions= """
    You're a Country Info Agent. You take the country name and 
    tell capital city, language and population of that country using tools.
    Add the flag emoji of that specific country in response.
    Never translate on your own, you always use the provided tools.
    """,
    tools= [
        capital_city_agent.as_tool(
            tool_name= "capital_city_tool",
            tool_description= "Tells the Capital City of the given Country",
        ),
        language_agent.as_tool(
            tool_name= "language_agent_tool",
            tool_description= "Tells the Language spoken in the given Country"
        ),
        population_agent.as_tool(
            tool_name= "population_agent_tool",
            tool_description= "Tells the Population of the given Country",
        )
        ],
    model= model
)

def main():

    print("Hello! from Country Info Bot.\nEnter the country name to get its info.")
    
    while True:
        print("Enter 'q' to quit.")
        user_input= input("Country name: ")

        if user_input.lower() == 'q':
            print("Quitting...\nGood Bye!")
            break

        response = Runner.run_sync(
            country_info_agent,
            user_input,
            run_config= config
            )
        
        print(f"\nInfo:\n{response.final_output}\n")
        print(f"Responded by: {response.last_agent.name}\n")


if __name__ == "__main__":
    main()