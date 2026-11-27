
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# ===== 第1步：用JSON Schema手动描述工具 =====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市在指定日期的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称",
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式为YYYY-MM-DD",
                    }
                },
                "required": ["city", "date"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

# ===== 第2步：定义工具的实际执行逻辑 =====
def get_weather(city, date):
    return f"{city} 在 {date} 天气晴朗，适合爬山。"

# ===== 第3步：把用户消息和工具描述一起发给LLM =====
messages = [
    {"role": "user", "content": "北京2026-07-25的天气怎么样？"}
]

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    tools=tools
)


# ===== 第4步：处理LLM的输出 =====
print(response.choices[0].message)
messages.append(response.choices[0].message)

# ===== 第5步：遍历工具并执行 =====
for tool_call in  response.choices[0].message.tool_calls:
    if tool_call.function.name == "get_weather":

        # 获取函数的参数
        args = json.loads(tool_call.function.arguments)
        result = get_weather(args["city"], args["date"])
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps({"weather": result})
        })


# ===== 第6步：LLM真正调用工具
final_response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    tools=tools
)
print(final_response.choices[0].message.content)
