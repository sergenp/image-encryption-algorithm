import asyncio

async def do_while_idle():
    for _ in range(3):
        print("IDLE")
        await asyncio.sleep(1)

    return "Done stuff while idling"

async def long_task():
    await asyncio.sleep(3)
    return "DONE !"

async def main():
    task = asyncio.create_task(long_task())
    task2 = asyncio.create_task(do_while_idle())
    done, _ = await asyncio.wait({task, task2})
    
    if task in done:
        task2.cancel()
        print(task.result())

asyncio.run(main())