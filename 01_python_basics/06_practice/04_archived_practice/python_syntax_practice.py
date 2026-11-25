"""电商订单管理 · Python 语法示例（Python 3.12+，标准库）

阅读方式
直接运行文件，按第 01–10 节追踪一笔订单，在代码和输出之间对照每种语法的作用。

运行方式
    python python_syntax_practice.py
    python python_syntax_practice.py --report order.json

语法覆盖清单
[01] 导入、变量与赋值、str/int/float/bool、列表/元组、索引与切片、
     算术和比较运算、in、f-string、迭代解包与星号表达式
[02] if/elif/else、for、break/continue、逻辑运算、真假值与短路
[03] def/return、位置与关键字参数、默认值、*args/**kwargs 的打包与展开、
     类型注解、高阶函数、局部作用域与闭包
[04] 字典、类与实例、类属性和实例属性、实例/类/静态方法、继承与重写、
     @property、@dataclass、__init__/__len__/__iter__
[05] 集合、列表/字典/集合推导式与嵌套推导式、:=、lambda、None、
     enumerate/zip/sorted、any/all/map/filter、is 与 ==，条件表达式也见 [03]
[06] 自定义异常、pass、try/except/else/finally、raise、global
[07] 装饰器、@wraps、nonlocal、match/case
[08] while、可迭代对象与迭代器、iter/next、生成器表达式、yield 与惰性求值
[09] with、上下文管理器、Path、JSON 读写
[10] async/await、asyncio.gather/run

约定：金额统一用整数分计算，控制台显示为元。直接运行时会保存并读回
一个临时 JSON 文件。指定 --report 路径即可保留该文件。
"""

import argparse
import asyncio
import json
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict, dataclass
from functools import wraps
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar


# ============================================================
# 01 · 商品目录｜变量、字符串、容器和切片
# ============================================================

# SKU 是商品编号。每个元组依次存放编号、名称、单价（分）、库存和标签。
# 只有一个标签时也要留逗号，例如 ("外设",) 才是元组。
PRODUCT_ROWS = [
    ("KB01", "键盘", 12000, 4, ("外设", "办公")),
    ("MS01", "鼠标", 6500, 8, ("外设",)),
    ("ST01", "电脑支架", 8900, 0, ("办公",)),
]

# 模拟导入购物车。空行和备注会被跳过，END 后的支架记录不会被读取。
CART_ROWS = (" kb01, 2 ", "", "# 客服备注", "MS01,1", "END", "ST01,1")


def show_catalog_preview() -> None:
    first, *remaining = PRODUCT_ROWS  # 第一条赋给 first，剩余记录收进列表。
    sku, name, price, stock, tags = first
    price_in_yuan = price / 100  # / 的结果是 float。业务计算仍用整数分。
    in_stock = stock > 0
    print(f"目录首件：{sku} {name} ¥{price_in_yuan:.2f}，有库存：{in_stock}")  # .2f 显示两位小数。
    # [:2] 取前两条，[-1] 取末条。每条记录的 [1] 是商品名。
    print(f"前两件：{[row[1] for row in PRODUCT_ROWS[:2]]}，末件：{remaining[-1][1]}")
    print(f"首件属于外设：{'外设' in tags}")


# ============================================================
# 02 · 读购物车｜条件、循环、break 和 continue
# ============================================================

def read_cart_rows(rows: Iterable[str]) -> list[tuple[str, int]]:
    """读取「SKU,数量」。忽略空行与备注，遇到 END 后结束。"""
    items = []
    for row in rows:
        text = row.strip()
        if text == "END":
            break  # 结束整个循环，END 后面的商品都不会进入购物车。
        if not text or text.startswith("#"):  # 左边为真时，or 跳过右边。
            continue  # 只跳过当前行，继续读下一行。

        # 例如 "kb01, 2" 先按逗号拆开，再整理成 ("KB01", 2)。
        sku, quantity = text.split(",")
        items.append((sku.strip().upper(), int(quantity)))
    return items


def show_cart_size(quantity: int) -> None:
    if quantity == 0:
        message = "购物车为空"
    elif quantity == 1:
        message = "购物车有一件商品"
    else:
        message = f"购物车有 {quantity} 件商品"
    print(message)


# ============================================================
# 03 · 结算规则｜函数、参数、高阶函数和闭包
# ============================================================

def format_receipt(order_id: str, *labels: str, **details: str) -> str:
    # *labels 收集额外位置参数为元组，**details 收集额外关键字参数为字典。
    parts = [order_id, *labels]  # 以订单号开头，再逐个放入标签。
    # items() 给出键值对，下面把 {"渠道": "自营商城"} 写成 "渠道=自营商城"。
    parts.extend(f"{key}={value}" for key, value in details.items())
    return " | ".join(parts)


def make_coupon(minimum: int, reduction: int) -> Callable[[int], int]:
    """创建一个满减规则，返回的是优惠金额。"""
    # Callable[[int], int] 表示接收一个整数并返回整数的函数。
    def discount(subtotal: int) -> int:
        # 外层函数已返回，discount 依然能读取当时的 minimum 和 reduction。
        return reduction if subtotal >= minimum else 0

    return discount  # 返回函数本身。拿到小计后，由 calculate_total 调用它。


def calculate_total(
    subtotal: int, /, *, discount: Callable[[int], int] | None = None
) -> int:
    # / 前的 subtotal 按位置传入，* 后的 discount 按名字传入。省略 discount 时不打折。
    reduction = 0 if discount is None else discount(subtotal)
    if not 0 <= reduction <= subtotal:
        raise ValueError("优惠金额必须介于 0 和商品小计之间")
    return subtotal - reduction


# ============================================================
# 04 · 商品与购物车｜数据类、方法、属性和继承
# ============================================================

@dataclass  # 根据字段生成 __init__，例如 Product("MS01", "鼠标", 6500, 8)。
class Product:
    sku: str
    name: str
    price: int
    stock: int
    tags: tuple[str, ...] = ()

    @property  # 用 product.in_stock 读取，每次都按当前库存计算。
    def in_stock(self) -> bool:
        return self.stock > 0


class Cart:
    MAX_QUANTITY: ClassVar[int] = 99  # 类属性。每个实例有自己的 items。

    def __init__(self) -> None:
        self.items: dict[str, int] = {}

    @classmethod
    def from_rows(cls, rows: Iterable[tuple[str, int]]) -> "Cart":
        # 用 cls() 构造，MemberCart.from_rows() 会得到 MemberCart。
        cart = cls()
        for sku, quantity in rows:
            cart.add(sku, quantity)
        return cart

    @staticmethod
    def validate_quantity(quantity: int) -> None:
        # 只检查传入的数量，无需访问实例或类。
        if quantity <= 0:
            raise ValueError("商品数量必须大于 0")

    def add(self, sku: str, quantity: int) -> None:
        self.validate_quantity(quantity)
        total = self.items.get(sku, 0) + quantity  # 新商品从 0 开始，同一 SKU 累加。
        if total > self.MAX_QUANTITY:
            raise ValueError(f"{sku} 超过每种商品的数量上限")
        self.items[sku] = total

    @property
    def quantity(self) -> int:
        return sum(self.items.values())  # 键盘 2 个、鼠标 2 个时，总件数是 4。

    def __len__(self) -> int:
        return len(self.items)  # len(cart) 返回商品种类数。

    def __iter__(self) -> Iterator[tuple[str, int]]:
        return iter(self.items.items())  # 让 for sku, quantity in cart 可用。

    def discount(self, subtotal: int) -> int:
        return 0


class MemberCart(Cart):
    def discount(self, subtotal: int) -> int:
        # 重写父类方法。// 在这里把 5% 的优惠向下取整到分。
        return subtotal * 5 // 100


def build_sample_catalog() -> dict[str, Product]:
    # *row 把元组中的字段依次传给数据类的构造方法。
    return {row[0]: Product(*row) for row in PRODUCT_ROWS}


# ============================================================
# 05 · 检索商品｜推导式、排序和常用内置函数
# ============================================================

def show_catalog_tools(catalog: dict[str, Product]) -> None:
    products = list(catalog.values())
    prices = {product.sku: product.price for product in products}  # 编号 → 单价（分）。
    tags = {tag for product in products for tag in product.tags}  # 两层循环，集合去重。
    available = [product for product in products if product.in_stock]  # 只留下有库存的商品。
    # 外层为每个标签建键，内层列表收集这个标签下的在售 SKU。
    available_by_tag = {
        tag: [product.sku for product in available if tag in product.tags]
        for tag in sorted(tags)
    }

    # filter 先筛出有货商品，map 再取名称，list() 收集结果。
    names = list(map(lambda product: product.name, filter(lambda p: p.in_stock, products)))
    # lambda 定义一个短函数，返回排序键。先比价格，价格相同再比编号。
    ranked = sorted(available, key=lambda product: (product.price, product.sku))
    print(f"在售商品：{names}，价格表：{prices}")
    print(f"按标签查看在售商品：{available_by_tag}")
    for rank, product in enumerate(ranked, start=1):
        print(f"  {rank}. {product.name} ¥{product.price / 100:.2f}")

    # any() 找到一个真值就停止，all() 找到一个假值就停止。
    print(f"有缺货：{any(not product.in_stock for product in products)}")
    print(f"全部定价大于零：{all(product.price > 0 for product in products)}")

    # := 把查到的对象赋给 product，同时用 is None 判断是否缺少该记录。
    if (product := catalog.get("KB01")) is not None:
        same_sku = product.sku == "KB01"  # == 比较值，is 判断是不是同一个对象。
        print(f"查到 {product.name}，编号匹配：{same_sku}")


def join_import_columns(skus: list[str], quantities: list[int]) -> list[tuple[str, int]]:
    # 对齐表格的两列。strict=True 会在两列长度不同时报错。
    return list(zip(skus, quantities, strict=True))


# ============================================================
# 06 · 创建订单｜校验、异常处理和 global
# ============================================================

class OrderError(ValueError):
    # 自定义异常先只保留专用类型，pass 让类体保持合法。
    pass


@dataclass(frozen=True)  # 下单时记录商品名和单价，订单行的字段之后不能重新赋值。
class OrderLine:
    sku: str
    name: str
    quantity: int
    price: int


@dataclass
class Order:
    order_id: str
    lines: tuple[OrderLine, ...]
    subtotal: int
    total: int
    status: str = "待支付"


ORDERS_CREATED = 0  # 当前进程创建订单的累计次数。


def create_order(
    order_id: str,
    cart: Cart,
    catalog: dict[str, Product],
    *,
    coupon: Callable[[int], int] | None = None,
) -> Order:
    global ORDERS_CREATED  # 写入模块变量时声明 global。只读取时不需要。
    if not cart:  # Cart 的 __len__ 返回 0 时，购物车在条件判断中为假。
        raise OrderError("购物车为空")

    lines = []
    for sku, quantity in cart:
        product = catalog.get(sku)
        if product is None:
            raise OrderError(f"未知商品：{sku}")
        if not 0 < quantity <= product.stock:
            raise OrderError(f"{sku} 库存不足或数量无效")
        lines.append(OrderLine(sku, product.name, quantity, product.price))

    subtotal = sum(line.price * line.quantity for line in lines)
    rule = cart.discount if coupon is None else coupon  # 有满减券就用券，否则用购物车的折扣规则。
    total = calculate_total(subtotal, discount=rule)
    # 所有订单行与价格验证结束后才扣库存，避免只扣掉部分商品。
    for line in lines:
        catalog[line.sku].stock -= line.quantity

    ORDERS_CREATED += 1
    return Order(order_id, tuple(lines), subtotal, total)


def submit_checkout(
    order_id: str,
    cart: Cart,
    catalog: dict[str, Product],
    *,
    coupon: Callable[[int], int] | None = None,
) -> Order | None:
    try:
        order = create_order(order_id, cart, catalog, coupon=coupon)
    except ValueError as error:  # OrderError 继承自 ValueError，也会进入这里。
        print(f"结算失败：{error}")
        return None
    else:  # try 里的结算没有抛出异常时才进入。
        print(f"订单 {order.order_id} 创建成功")
        return order
    finally:  # 成功和失败分支即使执行了 return，也会先打印结束提示。
        print("本次结算结束")


# ============================================================
# 07 · 订单状态｜match、装饰器和 nonlocal
# ============================================================

def log_successful_actions(function):
    successes = 0  # 包装函数创建时初始化，支付和发货共享同一个计数。

    @wraps(function)  # 保留原函数的名字和文档。
    def wrapper(*args, **kwargs):
        nonlocal successes  # 修改外层作用域中的计数。
        result = function(*args, **kwargs)
        successes += 1  # 业务操作成功返回后才计数。
        print(f"状态操作成功累计：{successes}")
        return result

    return wrapper  # 此后调用 advance_order() 会先进入 wrapper，再调用原函数。


@log_successful_actions
def advance_order(order: Order, action: str) -> None:
    match order.status, action:  # 同时匹配当前状态和请求操作。
        case "待支付", "支付":
            order.status = "已支付"
        case "已支付", "发货":
            order.status = "已发货"
        case _:  # 兜底分支，例如从「待支付」直接请求发货。
            raise OrderError(f"{order.status}的订单无法执行“{action}”")

    print(f"{order.order_id} → {order.status}")


# ============================================================
# 08 · 销售统计｜while、生成器和惰性求值
# ============================================================

def paid_orders(orders: Iterable[Order]) -> Iterator[Order]:
    for order in orders:
        if order.status in {"已支付", "已发货"}:
            yield order  # 每执行一次 next()，推进到下一笔已收款订单。


def show_sales(orders: list[Order]) -> None:
    # paid_orders() 返回生成器，next() 才开始找符合条件的订单。
    iterator = iter(paid_orders(orders))
    order = next(iterator, None)  # 迭代器耗尽时用 None 表示读完。
    total = 0
    while order is not None:
        total += order.total
        order = next(iterator, None)

    # 上面的迭代器已经读完。新建生成器，逐笔逐行取数量交给 sum()。
    units = sum(line.quantity for order in paid_orders(orders) for line in order.lines)
    print(f"销售统计：{units} 件，实收 ¥{total / 100:.2f}")


# ============================================================
# 09 · 保存订单｜上下文管理器、文件和 JSON
# ============================================================

def save_order(path: Path, order: Order) -> None:
    # with 在退出代码块时关闭文件。asdict 将数据类转换成字典。
    with path.open("w", encoding="utf-8") as file:
        # dump() 直接写文件。ensure_ascii=False 保留中文，indent=2 让文件易读。
        json.dump(asdict(order), file, ensure_ascii=False, indent=2)


def load_order_record(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        # JSON 的数组读成 list。json.load 不会自动生成 Order 对象。
        return json.load(file)


# ============================================================
# 10 · 检查缺货｜async、await 和 gather
# ============================================================

async def query_stock(catalog: dict[str, Product], sku: str) -> tuple[str, int | None]:
    await asyncio.sleep(0.01)  # 模拟等待结果。等待期间其他协程可以运行。
    product = catalog.get(sku)
    # 0 表示商品存在但已经缺货，None 表示目录没有这个编号。
    return sku, None if product is None else product.stock


async def fetch_stock_report(
    catalog: dict[str, Product], skus: Iterable[str]
) -> dict[str, int | None]:
    requests = [query_stock(catalog, sku) for sku in skus]  # 先创建协程，此时还没开始查询。
    results = await asyncio.gather(*requests)  # 展开协程列表，同时等待，结果保持输入顺序。
    return dict(results)  # 把 (商品编号, 库存) 的列表转换成字典。


# ============================================================
# 运行入口｜完整订单流程
# ============================================================


def main(report_path: Path | None = None) -> None:
    print("\n[01–05 商品目录与购物车]")
    show_catalog_preview()
    catalog = build_sample_catalog()
    show_catalog_tools(catalog)
    imported_items = join_import_columns(["MS01"], [1])
    # * 展开两批明细。Cart.add() 会把两条鼠标记录合并为 2 个。
    cart = MemberCart.from_rows([*read_cart_rows(CART_ROWS), *imported_items])
    show_cart_size(cart.quantity)
    print(f"共 {len(cart)} 种商品：{list(cart)}")

    print("\n[06 创建订单]")
    # 先用缺货的支架走一遍失败分支，再创建正常订单。
    invalid_cart = Cart.from_rows([("ST01", 1)])
    submit_checkout("DEMO-FAIL", invalid_cart, catalog)

    before = ORDERS_CREATED
    coupon = make_coupon(minimum=30000, reduction=2000)  # 满 300 元减 20 元。
    order = submit_checkout("DEMO-001", cart, catalog, coupon=coupon)
    if order is None:
        raise RuntimeError("样例订单结算失败")

    labels = ("线上订单", "满减")
    details = {"渠道": "自营商城"}
    # * 展开位置参数，** 展开关键字参数。观察 format_receipt() 怎样收集它们。
    print(format_receipt(order.order_id, *labels, **details))
    print(f"商品小计 ¥{order.subtotal / 100:.2f}，应付 ¥{order.total / 100:.2f}")
    member_total = calculate_total(order.subtotal, discount=cart.discount)
    print(f"若改用会员折扣，应付 ¥{member_total / 100:.2f}")
    print(f"本次新增订单：{ORDERS_CREATED - before} 笔")

    print("\n[07–08 更新状态并统计销售]")
    advance_order(order, "支付")
    advance_order(order, "发货")
    show_sales([order])

    print("\n[09 保存并读回 JSON]")
    if report_path is None:
        # 普通演示写入临时目录，离开 with 后自动清理。
        with TemporaryDirectory() as directory:
            path = Path(directory) / "order.json"
            save_order(path, order)
            saved = load_order_record(path)
    else:
        save_order(report_path, order)
        saved = load_order_record(report_path)
        print(f"已保存到 {report_path}")
    print(f"读回 {saved['order_id']}，状态：{saved['status']}")

    print("\n[10 并发查询剩余库存]")
    # main() 是普通函数，由 asyncio.run() 执行协程并取回结果。
    stock_report = asyncio.run(fetch_stock_report(catalog, ["KB01", "MS01", "ST01", "UNKNOWN"]))
    for sku, count in stock_report.items():
        print(f"{sku}：{'待核对' if count is None else count}")


def cli() -> None:
    parser = argparse.ArgumentParser(description="运行订单演示")
    parser.add_argument("--report", type=Path, help="将演示订单保存到指定 JSON 文件，将覆盖同名文件")
    arguments = parser.parse_args()
    main(arguments.report)


if __name__ == "__main__":  # 直接运行时才进入演示，导入模块时不会执行这里。
    cli()
