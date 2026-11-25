"""从 CSV 读入馆藏，再按书名和标签检索。"""

import csv
from collections.abc import Iterator
from pathlib import Path

from models import Book


class CatalogError(ValueError):
    """馆藏表里有无法导入的记录。"""


def load_catalog(path: Path) -> dict[str, Book]:
    books: dict[str, Book] = {}
    # with 会在离开代码块时关闭文件。newline="" 让 csv 模块处理换行。
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.reader(file)
        next(rows, None)  # 取走表头。文件为空时返回 None。

        for row_number, raw_row in enumerate(rows, start=2):
            if not raw_row:
                continue

            row = [field.strip() for field in raw_row]
            try:
                book = Book.from_row(row)
            except ValueError as error:
                # from 保留原始错误，同时告诉读者应该检查哪一行数据。
                raise CatalogError(f"第 {row_number} 条记录有误：{error}") from error

            if book.book_id in books:
                raise CatalogError(f"第 {row_number} 条记录的编号重复：{book.book_id}")
            books[book.book_id] = book

    return books


def find_books(
    books: dict[str, Book],
    keyword: str = "",
    *,
    tags: tuple[str, ...] = (),
) -> list[Book]:
    # * 后面的参数通过名字传入，例如 tags=("编程",)。单元素元组需要逗号。
    keyword = keyword.strip().casefold()
    required_tags = set(tags)
    matches = []
    for book in books.values():
        # 空关键词会匹配所有书名。<= 判断所需标签是否都出现了。
        if keyword in book.title.casefold() and required_tags <= set(book.tags):
            matches.append(book)
    return matches


def book_pages(books: list[Book], page_size: int = 2) -> Iterator[list[Book]]:
    """每次交出一页，调用者可以按需继续取下一页。"""
    if page_size <= 0:
        raise ValueError("每页至少要有一本书的位置")

    start = 0
    while start < len(books):
        end = start + page_size
        yield books[start:end]  # 左闭右开。末页可以少于 page_size 本。
        start = end
