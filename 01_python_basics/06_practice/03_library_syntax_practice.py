"""用列表、字典和函数生成一份图书馆借阅报表。"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent


# 每行依次是编号、书名、借阅次数和类型。
SAMPLE_RECORDS = dedent("""\
    B01 | Python 入门 | 8 | 纸质
    B02 | 海边的故事 | 3 | 电子异常记录 | 缺少字段
    B03 | 星星从哪里来 | 5 | 纸质
    B04 | 数据整理笔记 | 2 | 纸质
    B05 | 演示无效次数 | -1 | 纸质
    B01 | 演示重复编号 | 1 | 纸质
""")
SAMPLE_STOCK = {"B01": 3, "B02": 0, "B03": 1}
POPULAR_THRESHOLD = 5


def read_books(records):
    """按图书编号保存有效记录，跳过格式错误和重复的记录。"""
    books = {}
    for line in records.splitlines():
        if not line.strip():
            continue

        try:
            book_id, title, count_text, kind = [field.strip() for field in line.split("|")]
            borrowed = int(count_text)
        except ValueError:
            print(f"跳过格式错误的记录：{line}")
            continue

        if not book_id or not title or borrowed < 0 or kind not in ("纸质", "电子"):
            print(f"跳过无效记录：{line}")
            continue
        if book_id in books:
            print(f"跳过重复编号：{book_id}")
            continue

        books[book_id] = {"书名": title, "借阅次数": borrowed, "类型": kind}

    return books


def find_by_title(books, keyword):
    """返回第一本书名包含关键词的图书，找不到时返回 None。"""
    keyword = keyword.strip().lower()
    if not keyword:
        return None

    for book in books.values():
        if keyword in book["书名"].lower():
            return book

    return None


def summarize(books):
    total_borrowed = 0
    popular_titles = []
    for book in books.values():
        total_borrowed += book["借阅次数"]
        if book["借阅次数"] >= POPULAR_THRESHOLD:
            popular_titles.append(book["书名"])

    book_count = len(books)
    average = total_borrowed / book_count if book_count else 0
    popular_ratio = len(popular_titles) / book_count if book_count else 0
    return {
        "馆藏本数": book_count,
        "总借阅次数": total_borrowed,
        "平均每本借阅次数": round(average, 2),
        "热门图书占比": f"{popular_ratio:.0%}",
        "热门图书": popular_titles,
    }


def check_stock(books, stock):
    result = {}
    for book_id in books:
        count = stock.get(book_id)
        if count is None:
            result[book_id] = "待核对"
        elif count == 0:
            result[book_id] = "已借完"
        else:
            result[book_id] = f"剩余 {count} 本"

    return result


def main():
    print("=== 图书馆借阅报表 ===")
    books = read_books(SAMPLE_RECORDS)

    keyword = "python"
    found = find_by_title(books, keyword)
    if found is None:
        print(f"\n查找 {keyword}：未找到")
    else:
        print(f"\n查找 {keyword}：{found['书名']}（{found['类型']}）")

    report = summarize(books)
    report["库存"] = check_stock(books, SAMPLE_STOCK)
    report_text = json.dumps(report, ensure_ascii=False, indent=2)

    # 用临时目录练习写 JSON，程序结束时会自动清理。
    with TemporaryDirectory() as directory:
        path = Path(directory) / "library_report.json"
        path.write_text(report_text, encoding="utf-8")

    print(f"\n{report_text}")


if __name__ == "__main__":
    main()
