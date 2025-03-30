from emotiontracker.emotions import Emotions
import util
import asyncio
import os

async def emoscr():

    cycle = 5   # cycle of detecting emotion and screenshot. track things every 5 seconds
    user_emotions = Emotions()

    while True:
        emotion_sum, label = user_emotions.trackEmotion()
        path = os.getcwd() + '\\screenshot\\emotion\\'
        util.captureandsendScreenshot(path)

        if emotion_sum <= -3:
            print('###WARNING. PERSISTENCE OF NEGATIVE FEELING###')
            user_emotions.emotions.clear()

        await asyncio.sleep(cycle)
