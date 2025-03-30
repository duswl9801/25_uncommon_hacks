# Image Embedding
import numpy as np
from PIL import Image
from game_description import extractFeatures
from scipy.spatial.distance import cosine

# LLM
#from google import genai
import PIL.Image
import google.generativeai as genai

# API key
from dotenv import load_dotenv
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

load_dotenv()
api_key = os.getenv('GEMINI')

stored_embeddings = np.load("stored_embeddings.npy")
description = np.load("descriptions.npy", allow_pickle=True)


def findMostSimilarImage(query_img_path, features_path="stored_embeddings.npy", metadata_path="descriptions.npy"):
    features_array = np.load(features_path)
    metadata_array = np.load(metadata_path)

    query_features = extractFeatures(query_img_path)

    best_score = float('inf')
    best_index = None

    for i, features in enumerate(features_array):
        score = cosine(query_features, features)
        if score < best_score:
            best_score = score
            best_index = i

    best_description = metadata_array[best_index] if best_index is not None else None

    return best_description


def getCheatInfo(query_image_path, game, description):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    image = PIL.Image.open(query_image_path)

    prompt = f"""
    You are analyzing a game screenshot from *{game}*

    Here is the relevant walkthrough step:
    "{description}"

    Please:
    1. Look at the image and determine which part of the above walkthrough the player is currently on.
    2. Return only the **next step** the player should take.
    3. Be as concise as possible (1-2 sentences).
    """

    response = model.generate_content(
        contents=[prompt, image]
    )
    #TODO -> Grap only "text" part
    answer = response

    return answer


if __name__ == '__main__':
    query_image_path = "screenshot_sample/test/test.webp"
    game = "Escape Simulator"

    description = findMostSimilarImage(query_image_path)
    print(description)
    answer = getCheatInfo(query_image_path, game, description)
    print(answer)
