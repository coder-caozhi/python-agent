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

# todo 配置一个多智能体,带有三个工具
# todo 添加人机交互!
# 需求: 删除添加人机交互, delete_file如果删除的info.txt就拦截!  调用delete_database删除user表就拦截!!/ 查询可以直接放行


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

# todo: 步骤3 执行添加thread_id
config = {"configurable":{"thread_id":"9527"}}
result = main_agent.invoke(input={
    "messages": [
        HumanMessage(content="先删除teacher的表数据!再查询product对应的表数据,最后删除info.txt文件!!")
    ]
},config=config)


#todo: 注意: 一旦触发了人机交互拦截的动作! 是所有的工具都不执行!! 包括查询数据表!! -> 配置放行或者拦截动作 -> 会再次规划调用流程 -> 触发
#todo 步骤4: 配置放行动作... 二次执行..
# 配置放行动作 = 拦截工具 = [{type:"reject/approve"},{}]
interrupts = result.get("__interrupt__") # 装拦截工具的信息
print(interrupts)  # interrupts = [Interrupt(value={})]
interrupt_tool_list = interrupts[0].value['action_requests']
decisions = []
for tool in interrupt_tool_list:
    #tool =  {'name': 'delete_database', 'args': {'table_name': 'user'},
    tool_name = tool['name']
    if tool_name == 'delete_file':
        file_name = tool['args']['file_name']
        if file_name == "info.txt":
            # 拦截
            decisions.append({
                "type":"reject"
            })
        else:
            # 放行
            decisions.append({
                "type":"approve"
            })
    elif tool_name == 'delete_database':
        table_name = tool['args']['table_name']
        if table_name == "user":
            decisions.append({
                "type":"reject"
            })
        else:
            decisions.append({
                "type":"approve"
            })
    else:
        decisions.append({
            "type": "approve"
        })
# 第二次执行
result = main_agent.invoke(
    Command(resume={"decisions":decisions}),config=config)

print(result['messages'][-1].content)

# [Interrupt(
#    value=
#        {
#           'action_requests': [  -> 拦截的工具和参数信息!
#                                {'name': 'delete_database', 'args': {'table_name': 'user'},
                        #        {'name': '工具', 'args': {'table_name': 'user'}
#                             ],
#           'review_configs': [{'action_name': 'delete_database',
#                                  'allowed_decisions': ['approve', 'edit', 'reject', 'respond']}]}, id='307699679dfa70298d3d39e457354f78')]