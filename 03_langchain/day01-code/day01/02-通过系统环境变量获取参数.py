import os

# 读取配置
# 没有调用 load_dotenv()，它不会去读 .env 文件，而是直接读取 Windows 操作系统环境变量。
print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_BASE_URL"))