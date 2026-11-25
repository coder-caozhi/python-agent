"""把当前馆藏和借阅记录整理成可以读写的 JSON 报表。"""

import json
from collections import Counter
from pathlib import Path

from lending import LendingDesk


def build_report(desk: LendingDesk) -> dict[str, object]:
    loans = []
    # Counter 对首次出现的姓名给出 0，因此可以直接加 1。
    counts: Counter[str] = Counter()
    for reader_name, book in desk:
        loans.append({"读者": reader_name, "书名": book.title})
        counts[reader_name] += 1

    # dict.items() 产生 (姓名, 本数)。lambda 指定先按本数降序，再按姓名排序。
    ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    readers = [{"读者": name, "借阅数": count} for name, count in ranking]

    # 字典推导式和集合推导式都用花括号。前者有键和值，后者收集不重复的值。
    stock = {book_id: desk.available_copies(book_id) for book_id in desk.books}
    tags = {tag for book in desk.books.values() for tag in book.tags}
    return {
        "馆藏种数": len(desk.books),
        "当前借出本数": len(desk),
        "在借记录": loans,
        "读者借阅排名": readers,
        "剩余库存": stock,
        "馆藏标签": sorted(tags),
    }


def save_report(path: Path, report: dict[str, object]) -> None:
    # ensure_ascii=False 让中文以原文写入。indent=2 给 JSON 内容缩进。
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")
