from pydantic import BaseModel


# 1. 定义state的结构
class UserState(BaseModel):
    name: str
    age: int

# 实例化
user_state = UserState(name="Annie", age=30)

# 自动数据类型转换
# user_state = UserState(name="Annie", age="30")

# user_state = UserState(name="Annie", ag="30")

print(user_state)


# 和TypedDict的区别是:pydantic的BaseModel有自动数据类型转换的功能
# 和TypedDict的共同点是:pydantic的BaseModel可以在编译阶段提示数据定义的错误