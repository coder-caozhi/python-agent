import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)
response = client.responses.create(
    model="gpt-5.6",
    input="今天的金价是多少",
    tools=[{"type": "web_search"}]
)

print(response.output_text)
