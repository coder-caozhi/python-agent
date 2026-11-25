"""借书、还书和库存检查。库存从当前借阅记录算出。"""

from collections.abc import Iterator

from activity_log import log_action
from models import Book, Reader


class LoanError(ValueError):
    """借还请求违反了图书馆的规则。"""


class LendingDesk:
    def __init__(self, books: dict[str, Book]) -> None:
        self.books = books
        # 集合里的每项是 (读者姓名, 图书编号)。同一人同一本书只借一次。
        self._active_loans: set[tuple[str, str]] = set()

    def get_book(self, book_id: str) -> Book:
        book = self.books.get(book_id)
        if book is None:
            raise LoanError(f"没有编号为 {book_id} 的图书")
        return book

    def available_copies(self, book_id: str) -> int:
        book = self.get_book(book_id)
        # sum 逐项读生成器。_ 表示这里用不到解包出来的读者姓名。
        borrowed = sum(1 for _, active_id in self._active_loans if active_id == book_id)
        return book.copies - borrowed

    @log_action("借书")
    def borrow(self, reader: Reader, book_id: str) -> str:
        book = self.get_book(book_id)
        loan = (reader.name, book_id)
        if loan in self._active_loans:
            raise LoanError(f"{reader.name}已经借了{book.label}")

        reader_loans = sum(1 for name, _ in self._active_loans if name == reader.name)
        if reader_loans >= reader.borrow_limit:
            raise LoanError(f"{reader.name}已达到 {reader.borrow_limit} 本的借阅上限")
        if self.available_copies(book_id) == 0:
            raise LoanError(f"{book.label}已借完")

        # 所有检查通过才修改记录。失败后，报表里仍是原来的数。
        self._active_loans.add(loan)
        return f"{reader.name}借了{book.label}"

    @log_action("还书")
    def return_book(self, reader: Reader, book_id: str) -> str:
        book = self.get_book(book_id)
        loan = (reader.name, book_id)
        if loan not in self._active_loans:
            raise LoanError(f"{reader.name}没有借阅{book.label}")

        self._active_loans.remove(loan)
        return f"{reader.name}还了{book.label}"

    def __iter__(self) -> Iterator[tuple[str, Book]]:
        # for name, book in desk 会调用这个方法，按姓名、图书编号的顺序取记录。
        for name, book_id in sorted(self._active_loans):
            yield name, self.books[book_id]

    def __len__(self) -> int:
        # len(desk) 返回当前借出多少本。
        return len(self._active_loans)


def apply_request(
    desk: LendingDesk,
    readers: dict[str, Reader],
    request: tuple[str, str, str],
) -> str:
    """执行一条形如 ("借书", "小林", "B01") 的请求。"""
    action, name, book_id = request
    reader = readers.get(name)
    if reader is None:
        raise LoanError(f"找不到读者 {name}")

    match action:
        case "借书":
            return desk.borrow(reader, book_id)
        case "还书":
            return desk.return_book(reader, book_id)
        case _:
            raise LoanError(f"无法识别的操作：{action}")
