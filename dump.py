def detectEmotion(self, face):
    model_name = get_model_list()[0]
    fer = EmotiEffLibRecognizer(engine="onnx", model_name=model_name, device = device)
    emotion, _ = fer.predict_emotions(face, logits=True)
    print(emotion[0])


#### For more than 2 people
    # make rectangle around detected faces
    for (x, y, w, h) in faces:


        extracted_face = gray[y:y+h, x:x+w]
        # fit face image to preprocessing size
        #zoom_extracted_face = zoom(ini_extracted_face, (shape_x/ini_extracted_face.shape[0],
        #                          shape_y/ini_extracted_face.shape[1]))
        zoom_extracted_face = cv2.resize(extracted_face, (48, 48))
        #img_name = img_path + str(count) + '.jpg'

        #cv2.imwrite(img_name, zoom_extracted_face)

        extracted_face = zoom_extracted_face.astype(np.float32)
        extracted_face /= float(extracted_face.max())   # sacled
        # zoomed_faces.append(zoom_extracted_face)
        #ed.detectEmotion(zoom_extracted_face)
        zoom_extracted_face = zoom_extracted_face / 255.0
        zoom_extracted_face = zoom_extracted_face.reshape(1, 48, 48, 1)

        ed.detectEmotion(zoom_extracted_face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (300, 300, 300), 3)    # BGR, the weight of line
        for i in range(x, x + w):
            for j in range(y, y + h):
                for k in range(3):
                    if frame[j, i, k] + 50 > 255:
                        frame[j, i, k] = 255
                    else:
                        frame[j, i, k] = frame[j, i, k] + 50














import multiprocessing
import emotiontracker.emotion_screenshot as emo_scr

def heavy_work():
    print("일 시작!!!")
    result = 0
    for i in range(4000000):
        result += i
    print('it\'s done')


if __name__ == '__main__':
    procs = [emo_scr.emoscr(), heavy_work()]

    for i in procs:
        p = multiprocessing.Process(target=i)
        p.start()

    for p in procs:
        p.join()
        print("1개 끝!")

