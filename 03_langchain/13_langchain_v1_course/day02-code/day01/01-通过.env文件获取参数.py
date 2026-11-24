import os

from dotenv import load_dotenv

# 1. 加载.env文件
# 只要系统环境变量中存在同名变量，则系统优先
# load_dotenv()
# 如果需要文件优先，则在函数中添加 override = True
load_dotenv(override=True)

# 2. 读取配置
print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_BASE_URL"))

# 最佳实践
# 开发时，不要配置系统环境变量，一律从.env读取
# 生产时（正式环境），配置系统环境变量