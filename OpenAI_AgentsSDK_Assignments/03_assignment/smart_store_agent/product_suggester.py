import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv()

set_tracing_disabled(disabled= True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-1.5-flash",
    openai_client= external_client
)

agent = Agent(
    name= "Smart Store Agent",
    instructions= """
    You're Smart Store Agent.\nYou suggest a product based on your needs.
    Example: If the user says "I have a headache", you should suggest a medicine and explain why.
    """,
    model= model
)

def main():

    print("Welcome To Your Smart Store Agent.\nI suggest a product based on your needs.\n\n")

    while True:
        print("You can enter 'q' to exit.")
        user_input = input("Your message: ")

        if user_input.lower() == 'q':
            print("Quitting...\nGood Bye!")
            break
        
        response = Runner.run_sync(agent, user_input)

        print(f"\nAgent: {response.final_output}")


if __name__ == "__main__":
    main()