import emotiontracker.emotion_screenshot as emo_scr
import asyncio
#import gui

async def heavy_work():
    print("Start Working!!!")
    result = 0
    for i in range(4000000):
        result += i
    print('One thread is done')

async def main():
    #gui.startGameCatcher()
    #loop_task2 = emo_scr.emoscr()

    #loop_task1 = asyncio.create_task(emo_scr.emoscr())  # Runs in the background

    #await gui.startGameCatcher()

    #await loop_task2
    #await heavy_work()  # Runs calculation
    #loop_task2 = asyncio.create_task(clickGuide())  # Runs in the background

    #await asyncio.gather(loop_task1, loop_task2)
    await emo_scr.emoscr()


if __name__ == '__main__':
    asyncio.run(main())




