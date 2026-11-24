#实现步骤
# 1. 定义状态
# 1. 定义状态
from typing import TypedDict, Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.types import interrupt, Command


class TransferState(TypedDict):
    recipient: str # 给谁转账
    amount: int # 转账金额
    memo: str # 备注
    approved: bool # 是否通过审核
    final_status: str

# 2. 定义节点: 确认节点
def review_transfer(state: TransferState) -> dict[str, Any]:
    """
    审核节点：生成待审核信息，并调用 interrupt 暂停
    """
    print("\n[Node] 审核节点：生成待执行的转账请求")

    # 组织数据
    # 1. 准备待审核的数据
    pending_transfer = {
        "recipient": state["recipient"],
        "amount": state["amount"],
        "memo": state["memo"],
    }


    # 中断
    # 2. 通过interrupt触发审核中断：程序会在这里暂停
    # 使用user_review接收审核结果
    user_review = interrupt(
        {
            "title": "转账审核",
            "pending_transfer": pending_transfer,
            "instruction": "请返回 bool(是否批准) 或 dict(修改字段)",
        }
    )

    # 恢复
    # 3. 处理用户的审核结果
    approved = False # 是否审核通过 初始值
    updated_transfer = dict(pending_transfer)

    if isinstance(user_review, bool):
        approved = user_review
    elif isinstance(user_review, dict):

        # 用户更新了字段
        approved = bool(user_review.get("approved", True))
        for k in ["recipient", "amount", "memo"]:
            # 判断用户是否对当前字段进行了修改
            if k in user_review:
                updated_transfer[k] = user_review[k]

    print(f"[Node] 审核结果: {approved}")

    # 返回结果
    return {
        "approved": approved,
        "recipient": updated_transfer["recipient"],
        "amount": updated_transfer["amount"],
        "memo": updated_transfer["memo"],
    }


# 3. 模拟支付节点
def execute_transfer(state: TransferState) -> dict[str, str]:
    """
    执行节点：根据审核结果执行转账
    """
    if not state["approved"]:

        # 拦截支付
        print("\n[Node] execute_transfer：用户未批准，取消转账")
        return {"final_status": "已取消：用户未批准"}

    print("\n[Node] execute_transfer：模拟执行转账...")
    # TODO

    return {
        "final_status": f"成功转账 {state['amount']} 元给 {state['recipient']}"
    }


# 3. 构建图
def build_graph():
    # 必须传入 checkpointer 才能支持中断
    from langgraph.graph import StateGraph
    graph = StateGraph(TransferState)
    graph.add_node("review_transfer", review_transfer)
    graph.add_node("execute_transfer", execute_transfer)

    graph.add_edge(START, "review_transfer")
    graph.add_edge("review_transfer", "execute_transfer")
    graph.add_edge("execute_transfer", END)

    return graph.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":

    app = build_graph()
    config = {"configurable": {"thread_id": "transfer-thread-01"}}

    initial_state = {
        "recipient": "Alice",
        "amount": 100,
        "memo": "午餐AA",
        "approved": False,
        "final_status": "",
    }

    print("=== 第一次调用：触发中断 ===")
    # 第一次调用，图会在 interrupt 处暂停
    result = app.invoke(initial_state, config=config)

    # 获取中断信息
    interrupt_val = result["__interrupt__"][0]
    print(f"系统暂停，等待审核，待审核数据为：{interrupt_val.value}")

    print("=== 第二次调用：处理中断 ===")
    user_decision = {
        "approved": False,
        # "amount": 120,
        # "memo": "晚餐AA",
    }

    # 使用user_decision将数据传回节点中断的位置
    final_result = app.invoke(Command(resume=user_decision), config= config)

    print(f"[System] 运行结果：{final_result['final_status']}")


# 接受到中断信息
# 用户做出选择
# 恢复流程（第二次调用）
# 获取到第二次调用的结果

