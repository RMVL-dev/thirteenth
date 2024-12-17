import asyncio


async def start_strongman(name, power):
    print(f"Силач {name} начал соревнования.")
    for i in range(1, 5):
        print(f"Силач {name} поднял {i} шар")
        await asyncio.sleep(1 / power)
    print(f"Силач {name} закончил соревнования.")


async def start_tournament():
    strongman_first = asyncio.create_task(start_strongman("William", 4))
    strongman_second = asyncio.create_task(start_strongman("Jack", 5))
    strongman_third = asyncio.create_task(start_strongman("Jim", 3))
    await strongman_first
    await strongman_second
    await strongman_third

asyncio.run(start_tournament())
