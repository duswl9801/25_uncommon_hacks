import numpy as np
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing import image
import os

# extract features from user's screenshot image
def extractFeatures(img_path,  target_size=(224, 224)):
    model = MobileNet(weights='imagenet', include_top=False, pooling='avg')

    img = image.load_img(img_path, target_size=target_size)
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    features = model.predict(img_data)
    return features.flatten()


def createMetadata(image_folder, descriptions):
    image_paths = [os.path.join(image_folder, file)
                   for file in os.listdir(image_folder)
                   if file.lower().endswith((".png", ".jpg", ".jpeg"))]

    embeddings_list = []

    for path in image_paths:
        embedding = extractFeatures(path)
        embeddings_list.append(embedding)

    stored_embeddings = np.array(embeddings_list)
    np.save("stored_embeddings.npy", stored_embeddings)
    np.save("descriptions.npy", descriptions)
    print("Meta data created")

    return 0


if __name__ == '__main__':
    meta_data_foler = "screenshot_sample/meta"
    descriptions = [
        "On the box with the buttons. Press FEATHERS-LION-SCARAB and grab the lid. On the number's wheel put 6 in the Owl, 2 in the water and 4 in the snake drawing. Pull the lever and grab the lid.",
        "On the box with the buttons. Press FEATHERS-LION-SCARAB and grab the lid. On the number's wheel put 6 in the Owl, 2 in the water and 4 in the snake drawing. Pull the lever and grab the lid.",
    ]

    createMetadata(meta_data_foler, descriptions)
