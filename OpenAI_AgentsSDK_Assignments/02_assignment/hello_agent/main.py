import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

provider = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-1.5-flash",
    openai_client= provider
)

config = RunConfig(
    model=  model,
    model_provider= provider,
    tracing_disabled= True
)

async def main():
    agent = Agent(
    name= "Assistant",
    instructions= "You are a helpful assistant"
    )

    result = await Runner.run(agent, "Hello, How are you?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())