from multiprocessing import Pool
import emotiontracker.emotion_screenshot as emo_scr
import asyncio

kill = 0

async  def heavy_work():
    print("일 시작!!!")
    result = 0
    for i in range(4000000):
        result += i
    print('it\'s done')

async def main():
    loop_task = asyncio.create_task(emo_scr.emoscr())  # Runs in the background
    await heavy_work()  # Runs calculation
    await loop_task  # Keeps the infinite loop running


if __name__ == '__main__':
    asyncio.run(main())



