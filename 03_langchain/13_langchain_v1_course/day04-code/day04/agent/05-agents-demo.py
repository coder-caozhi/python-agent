# day04/agents/06-agents-demo.py

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_tavily import TavilySearch

from dotenv import load_dotenv
load_dotenv(override=True)

# ===== 1. 定义自定义工具 =====
@tool
def calculate(expression: str) -> str:
    """计算数学表达式的结果。
    :param city: expression: 数学表达式，如 "2 + 3 * 4"、"100 / 7"
    :return: 计算结果
    """
    try:
        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算出错：{e}"

@tool
def get_current_date() -> str:
    """获取当前日期和时间，不需要任何参数。"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

# ===== 2. 使用第三方工具 =====
search = TavilySearch(max_results=3)

# ===== 3. 初始化LLM =====
llm = init_chat_model(model="deepseek-v4-pro", model_provider="openai")

# ===== 4. 创建Agent =====
agent = create_agent(
    model=llm,
    tools=[calculate, get_current_date, search],
    system_prompt="""你是一个智能助手，拥有以下能力：
- 计算数学表达式
- 查询当前日期时间
- 搜索网络信息

请根据用户的问题，选择合适的工具来回答。如果不需要工具就能回答，直接回答即可。""",
)

# ===== 5. 运行Agent =====
for i, step in enumerate(agent.stream(
    {"messages": [{"role": "user", "content": "今天是几号？帮我算一下距离2027年五一还有多少天"}]}
), start=1):
    print(f"=== 第 {i} 步 ===")
    print(step, end="\n\n")