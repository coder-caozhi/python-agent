import operator
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# 1. 定义图状态
class State(TypedDict):
    aggregate: Annotated[list, operator.add]

# 2. 定义节点函数
def a(state: State, config):
    print(f'Adding "A" to {state["aggregate"]}')
    print("config:", config)
    return {"aggregate": ["A"]}

def b(state: State, config):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}

def c(state: State, config):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}

def b_2(state: State, config):
    print(f'Adding "B_2" to {state["aggregate"]}')
    return {"aggregate": ["B_2"]}

def d(state: State, config):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}

# 3. 通过状态创建图实例
graph = StateGraph(State)
graph.add_node("a", a)
graph.add_node("b", b)
graph.add_node("b_2", b_2)
graph.add_node("c", c)
graph.add_node("d", d)

# 4. 添加边
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("a", "c")
graph.add_edge("b", "b_2")
graph.add_edge("b_2", "d")
graph.add_edge("c", "d")
graph.add_edge("d", END)

# 5. 编译
os.makedirs("./sqlite_data", exist_ok=True)
conn = sqlite3.connect(database="./sqlite_data/checkpointer.db", check_same_thread=False)
app = graph.compile(checkpointer=SqliteSaver(conn))

# 6. 执行
output_state = app.invoke({}, config={"configurable": {"thread_id": "user_session3"}})
print(output_state)

# 7. 获取所有历史状态信息
all_states = app.get_state_history(
    config={"configurable": {"thread_id": "user_session3"}}
)
print(all_states)

for state in all_states:
    print(state)

# 8. 获取最后一个超步的状态
last_state = app.get_state(config={"configurable": {"thread_id": "user_session3"}})
print(last_state)