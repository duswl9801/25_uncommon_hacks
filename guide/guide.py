import util
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.preprocessing import image as kimage
import numpy as np
from tensorflow.keras.applications.mobilenet import preprocess_input
import google.generativeai as genai
import os
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
from PIL import Image as pimage

class Guide:
    solution = "There is no guide. Good Luck"
    image_target_size = (224, 224)
    game_name = "Escape Simulator"
    path = os.getcwd() + '\\screenshot\\guide\\'

    temp_img = pimage.open("guide/screenshot_sample/test/test.webp")

    def __init__(self):
        self.stuck_point = util.captureandsendScreenshot(self.path)


    def extractFeatures(self):
        model = MobileNet(weights='imagenet', include_top=False, pooling='avg')
        #img = self.stuck_point.resize(self.image_target_size)
        img = self.temp_img.resize(self.image_target_size)
        img_data = kimage.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        features = model.predict(img_data)
        return features.flatten()


    def findMostSimilarImage(self):
        features_array = np.load("guide/stored_embeddings.npy")
        metadata_array = np.load("guide/descriptions.npy")

        image_features = self.extractFeatures()

        best_score = float('inf')
        best_index = None

        for i, features in enumerate(features_array):
            score = cosine(image_features, features)
            if score < best_score:
                best_score = score
                best_index = i

        best_description = metadata_array[best_index] if best_index is not None else None

        return best_description


    def searchGuide(self, best_description):

        prompt = f"""
        You are analyzing a game screenshot from *{self.game_name}*

        Here is the relevant walkthrough step:
        "{best_description}"

        Please:
        1. Look at the image and determine which part of the above walkthrough the player is currently on.
        2. Return only the **next step** the player should take.
        3. Be as concise as possible (1-2 sentences).
        """

        # API
        load_dotenv()
        api_key = os.getenv('GEMINI')

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        #image = PIL.Image.open()

        response = model.generate_content(
            #contents=[prompt, self.stuck_point]
            contents=[prompt, self.temp_img]
        )
        #TODO -> Grap only "text" part
        answer = response

        return answer

    def printGuide(self, best_description):
        answer = self.searchGuide(best_description)
        print(answer)



"""
guide = Guide()

best_description = guide.findMostSimilarImage()
print('before searchguide')
guide.printGuide(best_description)
"""



