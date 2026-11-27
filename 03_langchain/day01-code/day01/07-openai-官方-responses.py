import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("openai_base_url")
)
response = client.responses.create(
    model="deepseek-v4-pro",
    input="hello world"
)

print(response.output_text)
