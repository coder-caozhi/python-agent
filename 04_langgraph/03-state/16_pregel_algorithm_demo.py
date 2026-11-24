import operator
import time
from pprint import pprint
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义图状态
class State(TypedDict):
    aggregate: Annotated[list, operator.add]

# 2. 定义节点函数
def a(state: State, config):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}

def b(state: State, config):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}

def c(state: State, config):
    time.sleep(5)
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
# graph.add_edge("b_2", "d")
# graph.add_edge("c", "d")
# d节点只执行一次的方案
graph.add_edge(["b_2","c"], "d")

graph.add_edge("d", END)

# 5. 编译图
app = graph.compile()


# pprint(app.nodes['a'].__dict__)

# 6. 执行图，查看执行结果
output_state = app.invoke({"aggregate": []})
print('执行图后的状态为', output_state, end="\n\n")

# 7. 查看当前图的节点
print('当前图的节点为', app.nodes, end="\n\n")

# 8. 查看当前图的 channels
print('当前图的channels为', app.channels, end="\n\n")

# 9. 查看 a 节点的 trigger（当前节点的订阅）和 writers
print('节点a的triggers为', app.nodes['a'].triggers, end="\n\n")
print('节点a的writers为', app.nodes['a'].writers, end="\n\n")

# 10. 查看 d 节点的 trigger 和 writers
print('当前图的节点d的triggers为', app.nodes['d'].triggers, end="\n\n")
print('当前图的节点d的writers为', app.nodes['d'].writers, end="\n\n")