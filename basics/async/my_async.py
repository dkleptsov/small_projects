import asyncio

async def main():
    print("one")
    task = asyncio.create_task(foo("foo"))
    await asyncio.sleep(2)
    print("finished")

async def foo(text):
    print(text)
    await asyncio.sleep(2)

asyncio.run(main())
