# USAGE
# python liveliness_detection.py --model liveness.model --le le.pickle --detector face_detector

from imutils.video import VideoStream
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os


class Liveliness():

    def __init__(self,args):
        self.args = args


    def load_detector(self):
        protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
        modelPath = os.path.sep.join([args["detector"],
            "res10_300x300_ssd_iter_140000.caffemodel"])
        network = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        return network

    def load_model(self):
        model = load_model(args["model"])
        le = pickle.loads(open(args["le"], "rb").read())
        return model,le

    def detect(self):
        network = self.load_detector()
        model,le = self.load_model()
        video_stream = VideoStream(src=0).start()
        time.sleep(2.0)

        while True:
            frame = video_stream.read()
            frame = imutils.resize(frame, width=600)

            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                (300, 300), (104.0, 177.0, 123.0))

            network.setInput(blob)
            detections = network.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > args["confidence"]:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    startX = max(0, startX)
                    startY = max(0, startY)
                    endX = min(w, endX)
                    endY = min(h, endY)

                    face = frame[startY:endY, startX:endX]
                    face = cv2.resize(face, (32, 32))
                    face = face.astype("float") / 255.0
                    face = img_to_array(face)
                    face = np.expand_dims(face, axis=0)

                    preds = model.predict(face)[0]
                    j = np.argmax(preds)
                    label = le.classes_[j]

                    label = "{}: {:.4f}".format(label, preds[j])
                    cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        (0, 0, 255), 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        video_stream.stop()
    


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", type=str, required=True,
        help="path to trained model")
    ap.add_argument("-l", "--le", type=str, required=True,
        help="path to label encoder")
    ap.add_argument("-d", "--detector", type=str, required=True,
        help="path to OpenCV's deep learning face detector")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
        help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    live = Liveliness(args)
    live.detect()