import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

client = genai.Client(
    api_key=os.getenv("CLOSEAI_API_KEY"),
    http_options={
        "base_url": os.getenv("CLOSEAI_BASE_URL_GOOGLE")
    }
)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="你是谁，能做什么",
)


print(response.text)