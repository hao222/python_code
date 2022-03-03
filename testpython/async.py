import asyncio

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    """
    需要3s的时间
    :return:
    """
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


# asyncio.create_task() 函数用来并发运行作为 asyncio 任务 的多个协程
async def main1():
    """
    并发执行 只需要消耗最大的那个时间
    :return:
    """
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


# 可等待对象 能在await语句中使用的对象    协程 任务  Future

# gather 并发运行任务  并发： 快速切换任务   并行： 同一时刻同时进行任务
async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def main3():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)


if __name__ == "__main__":
    # run() 此函数会运行传入的协程，负责管理 asyncio 事件循环，终结异步生成器，并关闭线程池。
    asyncio.run(main3())
