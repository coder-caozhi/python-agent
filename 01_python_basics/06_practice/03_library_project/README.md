# 图书借还 · Python 综合练习

从一份馆藏 CSV 出发，先浏览和检索，再处理一批借还请求，最后统计库存和在借记录。每一步都能在终端看到结果，适合先跑一遍，再顺着代码跟敲。

想跟读每条请求如何改变库存，可以查看[业务与代码阅读说明](业务与代码阅读说明.md)。

## 运行

使用 Python 3.10 或更新版本，只用标准库。从仓库根目录运行。

```powershell
.\.venv\Scripts\python.exe -X utf8 .\01_python_basics\06_practice\03_library_project\run_demo.py
```

默认样例有 4 种图书，10 条请求里有 6 条成功，最终借出 4 本。小林借了 1 本，小周借了 3 本。报告默认打印到终端，加上 `--output .\library_report.json` 可以保存到仓库根目录。想用自己的馆藏表练习时，可以加上 `--catalog .\my_books.csv`。通知是本地模拟，先后顺序可能不同。

## 跟读和跟敲顺序

| 顺序 | 从哪里看 | 先弄懂什么 |
| --- | --- | --- |
| 1 | [run_demo.py](run_demo.py) 的 `main()` | 看数据经过哪些步骤。第一遍读到异步通知就可以先停。 |
| 2 | [models.py](models.py)、[sample_books.csv](sample_books.csv) 和 [catalog.py](catalog.py) | 从 CSV 选一行，跟到 `Book.from_row()`，看字符串怎样变成图书对象。再跟到 `find_books()` 和 `book_pages()`。 |
| 3 | [lending.py](lending.py) | 只跟第一条借书请求。看 `apply_request()` 选中哪个方法，再看 `_active_loans` 如何变化。接着试还书和借不到的情况。 |
| 4 | [reports.py](reports.py) | 用当前在借记录计算库存、排名和报表。重点看统计循环和几个推导式。 |
| 5 | [activity_log.py](activity_log.py) 和 [notices.py](notices.py) | 回看借还方法如何自动打印日志，再观察两条模拟通知如何并发执行。 |

## 语法定位

| 想练的语法 | 去哪里看 | 在这里做什么 |
| --- | --- | --- |
| 变量、常量、字符串、整数、布尔判断、`None`、f-string | `models.py` 的 `Book.from_row()` 和 `label`、`lending.py` 的 `get_book()` | 清洗输入、检查册数、格式化书名和处理找不到书的情况 |
| 列表、元组、字典、集合、索引、切片、解包 | `run_demo.py` 的 `REQUESTS`、`catalog.py` 的 `book_pages()`、`lending.py` 的 `LendingDesk`、`reports.py` 的排序 | 存一批请求、按页取书、记录在借关系、按本数排序 |
| `if/else`、`and/or/not`、`in`、`for`、`while`、`continue`、`match/case`、`:=` | `catalog.py` 的三个函数、`lending.py` 的 `apply_request()`、`run_demo.py` 的 `main()` | 跳过空行、筛选图书、分页、分派借还请求，以及边查找边判断 |
| 函数、默认参数、仅限关键字参数、`return`、类型注解、联合类型 | `catalog.py` 的 `find_books()` 和 `book_pages()`、`run_demo.py` 的 `main()` | 缩小筛选范围、自定义页大小、允许省略报表路径 |
| 类、实例、`self`、`__init__`、数据类、枚举、类属性、类方法、属性、继承、`super()` | `models.py`、`lending.py` 的 `LendingDesk` | 建立图书和读者对象，为不同读者设置借阅上限，保存当前借阅 |
| `yield`、`__iter__`、`__len__`、`next()`、`enumerate()` | `catalog.py` 的 `load_catalog()` 和 `book_pages()`、`lending.py` 的 `LendingDesk` | 取走表头，逐页读取馆藏，让借阅台支持 `for` 和 `len()` |
| 列表、字典、集合推导式，生成器表达式，`lambda`，`sorted()` | `reports.py` 的 `build_report()`、`lending.py` 的 `available_copies()` | 生成排名和库存报表、去重标签、计算已借出几本 |
| `try/except/else`、自定义异常、`raise ... from`、`with` | `catalog.py` 的 `load_catalog()`、`run_demo.py` 的 `main()`、`reports.py` 的 `save_report()` | 定位 CSV 错误，记录借还失败，确保文件关闭 |
| 装饰器、嵌套函数、闭包、`nonlocal`、`*args` 和 `**kwargs`、字典展开 | `activity_log.py` 的 `log_action()`、`run_demo.py` 的 `report` | 独立记录借书和还书次数，透传原函数参数，拼接报表字段 |
| `async def`、`await`、异步生成器、`async for` | `notices.py`、`run_demo.py` 的通知循环 | 并发模拟发送消息，完成一条就显示一条 |
| 模块导入、`__name__`、CSV、JSON 和命令行参数 | `run_demo.py` 的导入和文件末尾、`catalog.py`、`reports.py` | 连接各模块，导入馆藏和导出报表 |

## 动手改三次

1. 把 `B02` 的册数改成 `2`。运行后看看第 3 条请求为什么变成成功，以及后面哪条请求会因重复借阅失败。
2. 把馆藏预览的 `book_pages(...)` 改成每页 3 本，观察末页如何取到剩下的 1 本。
3. 新增一种读者，借阅上限设为 1 本。先仿照 `MemberReader` 写类，再在 `reader_list` 和 `REQUESTS` 中加两次借书，验证第二次被拒绝。
