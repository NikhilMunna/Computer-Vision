# USAGE
# python scan.py --image images/page.jpg


from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

class Scanner():

    def __init__(self,image):
        self.image = image

    def resize(self):
        ratio = self.image.shape[0] / 500.0
        orig = self.image.copy()
        image = imutils.resize(self.image, height = 500)
        return image,orig

    def find_edges(self):
        image,_ = self.resize()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # show the original image and the edge detected image
        print("STEP 1: Edge Detection")
        cv2.imshow("Image", image)
        cv2.imshow("Edged", edged)
        cv2.waitKey(0)        
        return edged

    def contour(self):
        edged = self.find_edges()
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break
        return screenCnt
    
    def perspective_transform(self):
        screenCnt = self.contour()
        image,orig = self.resize()
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Outline", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ratio = orig.shape[0] / 500.0
        
        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset = 10, method = "gaussian")
        warped = (warped > T).astype("uint8") * 255

        # show the original and scanned images
        print("STEP 3: Apply perspective transform")
        cv2.imshow("Original", imutils.resize(orig, height = 650))
        cv2.imshow("Scanned", imutils.resize(warped, height = 650))
        cv2.waitKey(0)




if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
        help = "Path to the image to be scanned")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    scanned = Scanner(image)
    scanned.perspective_transform()

