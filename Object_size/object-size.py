# USAGE
# python object-size.py --image images/example_01.png --width 0.955
# python object-size.py --image images/example_02.png --width 0.955
# python object-size.py --image images/example_03.png --width 3.5

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

class Size():

    def __init__(self,image):
        self.image = image
    
    def convert_gray(self):
        return  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def blurred(self):
        gray = self.convert_gray()
        return cv2.GaussianBlur(gray, (7, 7), 0)

    def close_gaps(self):
        gray = self.convert_gray()
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        return edged

    def  find_and_sort_contours(self):
        edged = self.close_gaps()
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        (cnts, _) = contours.sort_contours(cnts)
        pixelsPerMetric = None  
        return cnts

    def calculate(self):
        cnts = self.find_and_sort_contours()
        pixelsPerMetric = None
        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue

            original = image.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            box = perspective.order_points(box)
            cv2.drawContours(original, [box.astype("int")], -1, (0, 255, 0), 2)

            for (x, y) in box:
                cv2.circle(original, (int(x), int(y)), 5, (0, 0, 255), -1)

            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)

            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            cv2.circle(original, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(original, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(original, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(original, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            cv2.line(original, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                (255, 0, 255), 2)
            cv2.line(original, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                (255, 0, 255), 2)

            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            if pixelsPerMetric is None:
                pixelsPerMetric = dB / args["width"]

            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric

            cv2.putText(original, "{:.1f}in".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
            cv2.putText(original, "{:.1f}in".format(dimB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)

            cv2.imshow("Image", original)
            cv2.waitKey(0)

    


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
    ap.add_argument("-w", "--width", type=float, required=True,
        help="width of the left-most object in the image (in inches)")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    object_size = Size(image)
    object_size.calculate()