import os
from dotenv import load_dotenv
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client = external_client,
    model = "gemini-2.0-flash"
)

config = RunConfig(
    model_provider = external_client,
    model = model,
    tracing_disabled = True
)