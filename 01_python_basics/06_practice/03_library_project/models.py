"""先认识项目里的两种对象：图书和读者。"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class BookKind(Enum):
    """样例表格中允许填写的图书类型。"""

    PAPER = "纸质"
    DIGITAL = "电子"


@dataclass(frozen=True)
class Book:
    # dataclass 根据这些字段生成 __init__。frozen=True 固定图书的原始资料。
    book_id: str
    title: str
    kind: BookKind
    copies: int
    tags: tuple[str, ...] = ()

    @classmethod
    def from_row(cls, row: list[str]) -> "Book":
        """把 CSV 的一行字符串转换成一本书。"""
        book_id, title, kind_text, copies_text, tags_text = row
        copies = int(copies_text)
        if not book_id or not title or copies < 0:
            raise ValueError("编号和书名必须填写，册数不能小于 0")

        # 先清理空格，再用生成器表达式留下非空标签。
        raw_tags = tags_text.split("|")
        tags = tuple(tag for tag in map(str.strip, raw_tags) if tag)
        return cls(book_id, title, BookKind(kind_text), copies, tags)

    @property
    def label(self) -> str:
        # 用 book.label 读取。value 是枚举成员对应的中文值。
        return f"《{self.title}》（{self.kind.value}）"


@dataclass(frozen=True)
class Reader:
    name: str
    # ClassVar 是类属性。Reader("小林") 只需要传入名字。
    borrow_limit: ClassVar[int] = 2

    def describe(self) -> str:
        return f"{self.name}（可借 {self.borrow_limit} 本）"


class MemberReader(Reader):
    # 子类沿用 Reader 的初始化方法，可以覆盖类属性和方法。
    borrow_limit = 3

    def describe(self) -> str:
        return f"会员{super().describe()}"
