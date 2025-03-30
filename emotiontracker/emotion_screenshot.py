from emotiontracker.emotions import Emotions
import util
import asyncio
import os
import pymysql

async def emoscr():

    cycle = 1   # cycle of detecting emotion and screenshot
    user_emotions = Emotions()

    # Establish database connection
    #conn = pymysql.connect(host='127.0.0.1', user='root', password='9078', database='gamecatcher')
    #cursor = conn.cursor()


    while True:
        emotion_sum, label = user_emotions.trackEmotion()
        path = os.getcwd() + '\\screenshot\\emotion\\'
        screenshot, dest = util.captureandsendScreenshot(path)

        insert_query = """
            INSERT INTO emotion (screenshot, emotion_label)
            VALUES (%s, %s)
            """
        #cursor.execute(insert_query, (dest, label))

        #conn.commit()

        if emotion_sum <= -3:
            print('###WARNING. PERSISTENCE OF NEGATIVE FEELING###')
            user_emotions.emotions.clear()

        await asyncio.sleep(cycle)
