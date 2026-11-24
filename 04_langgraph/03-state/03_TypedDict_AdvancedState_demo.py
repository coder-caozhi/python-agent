from typing import TypedDict, NotRequired, List


# 从mongodb中获取历史聊天记录
# conversation_history = []

# 1. 定义结构
class AdvancedState(TypedDict):
    """包含可选字段和复杂类型的TypedDict"""
    # 必需字段
    user_query: str
    conversation_history: List[str] #mongodb 分布式项目中的大批量的业务数据

    # 可选字段 - 使用NotRequired表示该字段可以缺失
    rag_documents: NotRequired[List[dict]]
    search_results: NotRequired[List[dict]]

# 2. 实例化
# 2.1 创建不包含可选字段的状态
simple_state: AdvancedState = {
    "user_query": "请解释LangGraph的状态管理",
    "conversation_history": ["你好，我是AI助手", "我能帮您了解LangGraph"],
}

# 2.1 创建完整的状态
full_state: AdvancedState = {
    "user_query": "请解释LangGraph的状态管理",
    "conversation_history": ["你好，我是AI助手", "我能帮您了解LangGraph"],
    "rag_documents": [
        {"title": "LangGraph文档", "content": "状态管理章节..."},
        {"title": "最佳实践", "content": "TypedDict是推荐方式..."}
    ],
    "search_results": [
        {"title": "LangGraph文档", "content": "状态管理章节..."},
        {"title": "最佳实践", "content": "TypedDict是推荐方式..."}
    ]
}

print(f"简单状态字段的展示:{list(simple_state.keys())}")
print(f"完整状态字段的展示:{list(full_state.keys())}")