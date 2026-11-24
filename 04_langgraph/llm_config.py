# 定义minerU服务配置
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(override=True)

@dataclass
class LLMConfig:
    llm_model: str
    model_provider: str
    base_url: str
    api_key : str

llm_config = LLMConfig(
    llm_model="deepseek-v4-pro",
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)