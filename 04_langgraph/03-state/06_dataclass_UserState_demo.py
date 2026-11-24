from dataclasses import dataclass


# 1. 创建数据类
@dataclass
class UserState:
    name: str
    age: int

    # def __init__(self, name: str, age: int):
    #     self.name = "Charlie"
    #     self.age = 35
    #
    # def __repr__(self):
    #     return f"UserState(name={self.name}, age={self.age})"

# 2. 实例化
user_state = UserState(name="Helen", age=36)

# 输出
print(user_state)