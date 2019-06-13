# USAGE
# python face_detect.py --image rooster.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

import numpy as np
import argparse
import cv2


class Detect():
    
    def __init__(self,image,args):
        self.image = image
        self.args = args 

    def load_model(self):
        network = cv2.dnn.readNetFromCaffe(self.args["prototxt"], self.args["model"])
        return network

    def shape(self):
        (h, w) = image.shape[:2]
        return h,w

    def blob(self):
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        return blob

    def detect(self):
        network = self.load_model()
        blob = self.blob()
        h,w = self.shape()
        network.setInput(blob)
        detections = network.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > args["confidence"]:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
        
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
                cv2.putText(image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        cv2.imshow("Output", image)
        cv2.waitKey(0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image")
    ap.add_argument("-p", "--prototxt", required=True,
        help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True,
        help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
        help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())    

    image = cv2.imread(args["image"])
    face = Detect(image,args)
    face.detect()
