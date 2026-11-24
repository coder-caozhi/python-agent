# -*- coding: utf-8 -*-
"""
DeepAgents 中断审批机制示例
核心功能：演示高危工具调用前的人工审批流程，支持删除数据库表/文件的审批控制
"""
import os
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver  # 内存检查点，用于保存中断状态
from langgraph.types import Command  # 恢复执行的指令类型
from dotenv import load_dotenv, find_dotenv
from langgraph.checkpoint.memory import InMemorySaver



# 加载环境变量（OPENAI_API_KEY、OPENAI_BASE_URL 等），优先查找当前目录的.env文件
load_dotenv(find_dotenv())


# ======================== 1. 定义工具函数 ========================
# 装饰器@tool将普通函数转为LangChain可调用工具，函数文档字符串会作为工具描述给Agent
@tool
def delete_database(table_name: str):
    """
    高危操作：删除数据库表
    :param table_name: 要删除的表名
    :return: 操作结果提示
    """
    print(f"[工具执行] 删除表: {table_name}")
    return f"已成功删除表: {table_name}"


@tool
def select_data(table_name: str):
    """
    普通操作：查询指定表名的数据（无需审批）
    :param table_name: 要查询的表名
    :return: 操作结果提示
    """
    print(f"[工具执行] 查询指定表名数据: {table_name}")
    return f"查询数据成功：{table_name}"


@tool
def delete_file(file_name: str):
    """
    高危操作：删除文件
    :param file_name: 要删除的文件路径/名称
    :return: 操作结果提示
    """
    print(f"[工具执行] 删除文件: {file_name}")
    return f"已成功删除文件: {file_name}"

model = init_chat_model(
    model=os.getenv("LLM_MODEL", "deepseek-chat"),
    model_provider="openai"
)


checkpointer = InMemorySaver()

# todo 步骤1: 指定哪些工具需要人机交互
# 创建多智能体
main_agent = create_deep_agent(
    model=model,
    system_prompt="""
       一个综合智能体,拥有: delete_database 删除指定表名工具 , select_data查询表数据工具,delete_file删除指定文件工具!
       如果有对应的需求,必须调用工具执行!
    """,
    tools=[delete_database, select_data, delete_file],
    interrupt_on={
        "delete_database":True,
        "delete_file":True,
        "select_data":False # 默认就是false
    },
    # todo 步骤2: 配置一个短期记忆对象
    checkpointer=checkpointer
)

# todo 需求:  delete_database 删除user表,拦截! 否则放行!  delete_file如果删除的info.txt -> 删除erdaye.txt放行! 其余的拦截
config = {"configurable":{"thread_id":"9527"}}
result = main_agent.invoke(
    input = {
        "messages":[
            HumanMessage(content="删除user的表数据!查询product对应的表数据,删除info.txt文件!!")
        ]
    },
    config=config
)

#todo 只要有拦截触发,所有工具都不会执行!!
tool_list = result.get("__interrupt__")[0].value['action_requests']
decisions = []

for tool_info in tool_list:
    # {name:"工具名",args:{table_name/file_name}}
    tool_name = tool_info['name']
    if tool_name == 'delete_database':
        table_name = tool_info['args']['table_name']
        if table_name == "user":
            # 拦截
            decisions.append(
                {
                    "type":"reject"
                }
            )
        else:
            # 放行
            decisions.append(
                {
                    "type":"approve"
                }
            )
    elif tool_name == 'delete_file':
        file_name = tool_info['args']['file_name']
        if file_name == "info.txt":
            # 编辑
            decisions.append({
                "type": "edit",
                "edited_action":{
                    "name":tool_name, # 工具名,
                    "args":{"file_name":"erdaye.txt"}
                }
            })
        else:
            # 拦截
            decisions.append({
                "type":"reject"
            })

# 二次执行
result = main_agent.invoke(
    Command(resume={"decisions":decisions}),config=config
)

print(f"最终执行结果:{result['messages'][-1].content}")