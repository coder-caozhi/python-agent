"""并发模拟通知。每个发送任务都等一小会儿，再返回一条消息。"""

import asyncio
from collections.abc import AsyncIterator


async def send_notice(name: str, count: int) -> str:
    # await 期间其他任务可以执行。这里用 sleep 模拟等待发送结果。
    await asyncio.sleep(0.01)
    return f"发给{name}的模拟通知：你当前借了 {count} 本书。"


async def iter_notices(counts: dict[str, int]) -> AsyncIterator[str]:
    # 这一行创建协程。as_completed 安排它们一起执行，谁先完成就先取谁。
    notices = [send_notice(name, count) for name, count in counts.items()]
    for pending_result in asyncio.as_completed(notices):
        yield await pending_result
