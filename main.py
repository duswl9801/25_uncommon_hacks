import emotiontracker.emotion_screenshot as emo_scr
import asyncio
from guide.guide import Guide
import time

kill = 0

async def heavy_work():
    print("일 시작!!!")
    result = 0
    for i in range(4000000):
        result += i
    print('it\'s done')

async def clickGameStart():
    pass

async def clickGameFinish():
    pass

async def clickTimer():
    pass

async def clickGuide():
    while True:

        guide = Guide()
        best_description = guide.findMostSimilarImage()
        print('before searchguide')
        guide.printGuide(best_description)

        await asyncio.sleep(40)


async def main():
    loop_task1 = asyncio.create_task(emo_scr.emoscr())  # Runs in the background
    await heavy_work()  # Runs calculation
    #loop_task2 = asyncio.create_task(clickGuide())  # Runs in the background
    await loop_task1
    #await asyncio.gather(loop_task1, loop_task2)


if __name__ == '__main__':
    asyncio.run(main())




