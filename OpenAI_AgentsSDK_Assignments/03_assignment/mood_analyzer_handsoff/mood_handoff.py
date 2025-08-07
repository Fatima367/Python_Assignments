import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")


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


activity_suggester = Agent(
    name= "Activity Suggester Agent",
    instructions= """
    You checks the user’s mood from their message (like “happy”, “sad”, etc.)
    Then suggests an activity according to their mood.
    """,
    handoff_description= """
    Checks the user’s mood from their message (like “happy”, “sad”, etc.)
    Then suggests an activity according to their mood.
    """
)


mood_analyst = Agent(
    name= "Mood Analyst",
    instructions= """
    You checks the user’s mood from their message (like “happy”, “sad”, etc.) 
    and handsoff to the appropriate agent.
    """,
    handoffs= [activity_suggester]
)

def main():

    print("\nHello I'm your Mood Analyzer Agent!\n")

    while True:

        print("Enter 'q' to exit.\n")
        user_input = input("Your message: ")

        if user_input.lower() == 'q':
            print("Quitting...\nGood Bye!")
            break

        result = Runner.run_sync(
            mood_analyst,
            input= user_input,
            run_config= config
            )

        print("\nAgent's Response:\n")
        print(f"{result.final_output}\n")
        print(f"Responded by: {result.last_agent.name}\n\n")


if __name__ == "__main__":
    main()