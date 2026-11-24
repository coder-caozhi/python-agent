# 3. 定义图状态
from typing import TypedDict, List

from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

# 1. 模拟大模型客户端
class MockLLM:
    def invoke(self, prompt: str):
        return f"AI生成答案：'{prompt}'"


# 2. 模拟数据库客户端
class MockDatabase:
    def get_user_info(self, user_id: str):
        return {
            "id": user_id,
            "role": "vip" if "vip" in user_id else "standard"
        }


class CustomerSupportState(TypedDict):
    query: str  # 用户问题
    response: str  # 客服回复
    log: List[str]  # 处理日志


# 4. 创建节点函数
def node_customer_service(state: CustomerSupportState, config: RunnableConfig, runtime: Runtime) -> dict:

    # 1 【参数1演示】从 state 中读取用户输入
    user_query = state["query"] # 当不保证query一定存在的时候，使用get()方法获取，并做兜底处理
    # user_query = state.get("query","")
    print(f"[State] 用户问题: {user_query}")

    # 2 【参数2演示】从 config 中读取参数
    configurable = config.get("configurable")
    user_id = configurable.get("user_id", "guest")

    if user_id == "vip_user_999":
        print(f"[Config] 用户ID: {user_id}")
    else:
        print(f"[Config] 用户ID: {user_id}，非VIP用户，请勿进行敏感操作")

    # 3 【参数3演示】从 context 中读取依赖对象
    llm_client = runtime.context.get("llm_client")
    db_client = runtime.context.get("db_client")

    # 验证对象是否存在
    if not llm_client:
        # raise ValueError("LLM客户端不存在")
        return {
            "response": "系统异常，请稍后再试",
            "log": ["失败：LLM客户端不存在"]
        }

    # 验证对象是否存在
    if not db_client:
        # raise ValueError("DB客户端不存在")
        return {
            "response": "系统异常，请稍后再试",
            "log": ["失败：DB客户端不存在"]
        }

    user_info = db_client.get_user_info(user_id)
    user_role = user_info.get("role")
    prompt = f"用户({user_role})提问：{user_query}"
    llm_response = llm_client.invoke(prompt)

    return {
        "response": llm_response,
        "log": ["成功：任务结束"]
    }


# 5. 构建图
def build_graph():
    workflow = StateGraph(CustomerSupportState)
    workflow.add_node(node_customer_service)
    workflow.add_edge(START, "node_customer_service")
    workflow.add_edge("node_customer_service", END)
    return workflow.compile()


# 运行示例
if __name__ == "__main__":

    # 创建图实例
    app = build_graph()

    # 初始化状态对象
    initial_state = {"query": "如何升级会员？"}

    # 初始化config对象
    config = {
        "configurable": {
            "user_id": "vip_user_999",
        }
    }

    # 初始化上下文运行环境(资源对象)
    context = {
        "llm_client": MockLLM(),
        "db_client": MockDatabase()
    }

    # 运行
    print("[System] 开始运行图，并注入依赖对象...")
    result = app.invoke(input=initial_state, config=config, context=context)
    print(result)
