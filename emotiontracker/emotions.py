import tensorflow as tf
import numpy as np
import cv2
from collections import deque

class Emotions:
    emotions = deque(maxlen=3)   # save user's emotions. max 3
    emotion_types = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
    emotion_labels = ['Positive', 'Neutral', "Negative"]

    def detectEmotion(self, face):
        model_path = "emotiontracker/facialemotionmodel.h5"
        model = tf.keras.models.load_model(model_path)

        prediction = model.predict(face, verbose=0)
        emotion_idx = np.argmax(prediction)
        confidence = float(np.max(prediction) * 100)

        print(self.emotion_types[emotion_idx], confidence)

        return emotion_idx

    def extractFace(self):

        shape_x, shape_y = (48, 48)

        emotion_idx = -1

        # read face cascade file
        face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')   # Face recognition/detection related model (weight) file
        cam = cv2.VideoCapture(0)   # built-in camera: 0, external camera: 1

        # camera properties
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 350)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)

        # frame: frame numpy including each pixel values
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale
        #  get faces
        # scaleFactor: Makes faces that are far away in the image look smaller, and faces that are close up look larger
        # smaller than 1.1 => detect more faces, bigger than 1.1 => detect less faces
        # minNeighbors: Minimum number of candidate bounding boxes
        # that must exist around a face to select the final bounding box
        faces = face_cascade.detectMultiScale(gray,
                                    1.7,
                                     5,
                                                minSize=(30, 30))

        # print number of detected faces
        print(len(faces))

        if len(faces) != 0:
            # Get the largest face
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face

            # make rectangle around detected faces
            extracted_face = gray[y:y+h, x:x+w]
            # fit face image to preprocessing size
            zoom_extracted_face = cv2.resize(extracted_face, (shape_x, shape_y))

            zoom_extracted_face = zoom_extracted_face / 255.0
            zoom_extracted_face = zoom_extracted_face.reshape(1, shape_x, shape_y, 1)

            emotion_idx = self.detectEmotion(zoom_extracted_face)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (300, 300, 300), 3)    # BGR, the weight of line
            for i in range(x, x + w):
                for j in range(y, y + h):
                    for k in range(3):
                        if frame[j, i, k] + 50 > 255:
                            frame[j, i, k] = 255
                        else:
                            frame[j, i, k] = frame[j, i, k] + 50


        # print frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        return emotion_idx


    """
    Emotion Type => 0: "Anger", 1: "Disgust", 2: "Fear", 3: "Happiness", 4: "Neutral", 5: "Sadness", 6: "Surprise",
    Emotion Labels => 0: "Positive", 1: "Neutral", 2: "Negative"
    """
    def trackEmotion(self):

        emotion_idx = self.extractFace()

        if emotion_idx == 3:
            self.emotions.append(1)
            label = 0   # positive
        elif emotion_idx == 4 or emotion_idx == -1:
            self.emotions.append(0)
            label = 1   # neutral
        else:
            self.emotions.append(-1)
            label = 2   # negative

        print(self.emotions)
        emotion_sum = sum(self.emotions)

        return emotion_sum, label



Emotions().trackEmotion()
