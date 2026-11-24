
# 1. 定义字典: 不推荐使用，推荐使用类来定义状态
user_state = {
    "name": 'Peter',
    "age": 25
}

# 2. 访问字典
print(user_state["name"])

# 编译时不会报错，运行时会报错
# 将问题前置在编译阶段
# print(user_state["aeg"])

# 3. 没有具体的规范
user_state['sex'] = True  # 添加新键值对
print(user_state["sex"])


# 4. 类型定义可能是模糊