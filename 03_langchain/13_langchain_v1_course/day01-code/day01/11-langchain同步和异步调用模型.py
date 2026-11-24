import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

# 0. 加载配置
load_dotenv(override=True)

async def llm_async_call():

    # 1. 初始化客户端
    model = init_chat_model(
        "openai:deepseek-v4-flash"
    )

    # 2. 调用模型
    # 2.1 同步调用
    # res = model.invoke(input="你好")

    # 2.2 异步调用（）
    res = await model.ainvoke(input="你好")

    # 3. 返回结果
    return res

if __name__ == '__main__':

    # 在python中有一个异步执行包：asyncio，用来配合执行异步代码
    # asyncio.run(协程对象)： 创建了事件循环、设置了事件循环、启动了事件循环
    res = asyncio.run(llm_async_call())
    print(res.content)

    # # 协程的本质
    # # 1. 创建事件循环
    # event_loop = asyncio.new_event_loop()
    # # 2. 设置事件循环
    # asyncio.set_event_loop(event_loop)
    # # 3. 启动事件循环
    # res = event_loop.run_until_complete(llm_async_call())
    # # 4. 获取返回结果
    # print(res.content)

