"""运行入口。先浏览馆藏，再处理借还请求，最后生成报表。"""

import argparse
import asyncio
import json
from pathlib import Path

from catalog import CatalogError, book_pages, find_books, load_catalog
from lending import LendingDesk, LoanError, apply_request
from models import MemberReader, Reader
from notices import iter_notices
from reports import build_report, save_report

SAMPLE_CATALOG = Path(__file__).with_name("sample_books.csv")
# 把这里的请求当成一叠便签，程序从第一张处理到最后一张。
REQUESTS = (
    ("借书", "小林", "B01"),
    ("借书", "小林", "B02"),
    ("借书", "小周", "B02"),  # 库存不足。
    ("借书", "小林", "B03"),  # 超过普通读者的借阅上限。
    ("借书", "小周", "B03"),
    ("还书", "小林", "B02"),
    ("借书", "小周", "B02"),  # 小林还书后可以再借。
    ("借书", "小周", "B01"),
    ("借书", "小周", "B01"),  # 同一本书不能重复借。
    ("还书", "小林", "B03"),  # 小林没有借过这本。
)


async def main(catalog_path: Path, output: Path | None = None) -> None:
    if output is not None and output.resolve() == catalog_path.resolve():
        raise CatalogError("请为报表指定一个不同于馆藏 CSV 的路径")

    books = load_catalog(catalog_path)
    print("=== 浏览馆藏 ===")
    for number, page in enumerate(book_pages(list(books.values())), start=1):
        labels = [book.label for book in page]
        print(f"第 {number} 页｜{'、'.join(labels)}")

    # := 把查询结果存进 matches，同时判断列表是否有内容。
    if matches := find_books(books, "python", tags=("编程",)):
        print("检索 Python 编程书｜", [book.title for book in matches])
    else:
        print("检索 Python 编程书｜没有找到匹配的图书")

    print("\n=== 借书与还书 ===")
    reader_list = [Reader("小林"), MemberReader("小周")]
    readers = {reader.name: reader for reader in reader_list}
    for reader in reader_list:
        print(reader.describe())

    desk = LendingDesk(books)
    accepted = 0
    rejected = []
    for request in REQUESTS:
        try:
            apply_request(desk, readers, request)
        except LoanError as error:
            message = f"{' '.join(request)}｜{error}"
            print(f"请求未通过｜{message}")
            rejected.append(message)
        else:
            accepted += 1  # try 里的请求成功后，才会运行 else。

    print("\n=== 借阅报表 ===")
    # ** 展开统计字典，再附上本批请求的处理结果。
    report = {**build_report(desk), "成功请求数": accepted, "失败请求": rejected}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if output is not None:
        save_report(output, report)
        print(f"报表已保存到 {output}")

    print("\n=== 模拟通知 ===")
    counts = {name: 0 for name in readers}
    for name, _ in desk:
        counts[name] += 1
    # async for 每次等待一条发送结果。两条消息的先后由任务完成顺序决定。
    async for message in iter_notices(counts):
        print(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行图书借还练习")
    parser.add_argument("--catalog", type=Path, default=SAMPLE_CATALOG, help="馆藏 CSV 路径")
    parser.add_argument("--output", type=Path, help="将报表保存为 JSON 文件")
    args = parser.parse_args()
    try:
        asyncio.run(main(args.catalog, args.output))
    except (CatalogError, OSError) as error:
        parser.exit(1, f"运行失败：{error}\n")
