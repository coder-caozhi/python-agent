from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# 1. 定义结构
class AgentState(BaseModel):
    """使用Pydantic BaseModel定义状态"""

    # 必需字段
    user_id: str = Field(description="用户唯一标识")
    query: str = Field(min_length=1, max_length=20, description="用户输入的查询")
    timestamp: datetime = Field(default_factory=datetime.now, description="状态创建时间")

    # 可选字段
    rag_result: Optional[str] = Field(None, description="RAG检索结果")
    web_search_result: Optional[str] = Field(None, description="网络搜索结果")
    final_answer: Optional[str] = Field(None, description="最终回复")

    # 创建验证器
    @field_validator("query")
    @classmethod
    def validate_query_empty(cls, v):
        """
        验证查询不能为空
        :param v: query的输入信息
        :return: 用户的输入
        """
        if not v or not v.strip():
            raise ValueError("查询不能为空")
        return v.strip()

try:
    # 实例化状态
    state = AgentState(
        user_id="user_123",
        query="法国的首都是哪 法国的首都是哪法国的首都是哪法国的首都是哪法国的首都是哪",
    )

    # 3. 数据访问
    print("Pydantic状态测试:")
    print(f"用户ID: {state.user_id}")
    print(f"查询: {state.query}")
    print(f"时间戳: {state.timestamp}")

    # 4. 转成dict
    state_dict = state.model_dump()
    print(f"状态字典: {type(state)}")
    print(f"状态字典: {type(state_dict)}")

except ValueError as e:

    # 5. 验证错误的捕获
    print(f"验证错误的捕获: {e}")


# 校验的优先级：
# 如果没有提供query属性: 触发 必填字段的校验
# 如果提供了query属性,但是值为"", 触发Field中的属性校验
# 如果提供了query属性,但是值为"",Field中没有提供属性校验,则触发校验器@field_validator


