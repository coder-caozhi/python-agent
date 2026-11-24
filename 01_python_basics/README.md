# 01 Python 基础

| 章节 | 练习内容 |
| --- | --- |
| [01 基础语法](01_syntax/) | 变量、类型、运算符、条件与循环 |
| [02 容器与函数](02_containers_and_functions/) | 列表、字典、集合、参数和返回值 |
| [03 面向对象与模块](03_oop_and_modules/) | 类、实例、继承、导入 |
| [04 文件与异常](04_files_exceptions_and_advanced/) | 读写文件、处理异常、使用高级语法 |
| [05 调试](05_debugging/README.md) | 断点、单步运行、检查变量 |
| [06 实践](06_practice/README.md) 与 [07 综合练习](07_comprehensive_practice/) | 用学生管理和记账脚本回顾前面的知识 |
| [08 高级 Python](08_advanced_python/README.md) | 迭代器、生成器、打包解包和异步 |

从仓库根目录运行第一个练习。

```powershell
uv run --locked python .\01_python_basics\01_syntax\01_变量.py
```

进入 FastAPI 前，试着写一个带类型标注的函数，从字典里读取字段，验证输入并返回新的字典。回顾异步章节时，先跑同步示例，再观察 `async` 与 `await` 的调用顺序。
