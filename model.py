import cv2
import tensorflow as tf
import numpy as np

print("TensorFlow version:", tf.__version__)
print("OpenCV version:", cv2.__version__)

model_path = "emotiontracker/facialemotionmodel.h5"
model = tf.keras.models.load_model(model_path)

emotion_labels = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']


face_img = cv2.imread("emotiontracker/data0.jpg")
face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

print(face_img.shape)
face_img = cv2.resize(face_img, (48, 48))
face_img = face_img / 255.0
print(face_img.shape)
face_img = face_img.reshape(1, 48, 48, 1)

prediction = model.predict(face_img, verbose=0)
emotion_idx = np.argmax(prediction)
confidence = float(np.max(prediction) * 100)

print(emotion_labels[emotion_idx], confidence)