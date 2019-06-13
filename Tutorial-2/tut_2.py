# USAGE
# python tut_2.py --image tetris_blocks.png

import argparse
import imutils
import cv2



class Tetris():

    def __init__(self,image):
        self.image = image
    
    def show_image(self):
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)

    def convert_to_grayscale(self):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray


    def show_grayscale(self):
        cv2.imshow("Gray", gray)
        cv2.waitKey(0)
        


    def outlines(self):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged_fig = cv2.Canny(gray, 30, 150)
        cv2.imshow("Edged", edged_fig)
        cv2.waitKey(0)

    def threshold(self):
        gray = self.convert_to_grayscale()    
        threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow("Thresh", threshold)
        cv2.waitKey(0)
        return threshold

    def find_contours(self):
        threshold = self.threshold()
        gray = self.convert_to_grayscale()
        contours= cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        contours= imutils.grab_contours(contours)
        
        return contours

    def draw_outline(self):
        contours= self.find_contours()
        output = self.image.copy()
        for c in contours:
            cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
            cv2.imshow("Contours", output)
            cv2.waitKey(0)

    def no_of_contours(self):
        contours= self.find_contours()
        text = "I found {} objects!".format(len(contours))
        
        output = self.image.copy()
        cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (240, 0, 159), 2)
        cv2.imshow("Contours", output)

    def erode(self):
        thresh = self.threshold()
        mask = thresh.copy()
        mask = cv2.erode(mask, None, iterations=5)
        cv2.imshow("Eroded", mask)
        cv2.waitKey(0)


    def dilate(self):
        thresh = self.threshold()
        mask = thresh.copy()
        mask = cv2.dilate(mask, None, iterations=5)
        cv2.imshow("Dilated", mask)
        cv2.waitKey(0)    

    def bitwise_and(self):
        thresh = self.threshold()
        mask = thresh.copy()
        output = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("bitwise", output)
        cv2.waitKey(0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image")
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"])
    tetris_image = Tetris(image)
    tetris_image.outlines()
    tetris_image.threshold()
    tetris_image.find_contours()
    tetris_image.draw_outline()
    tetris_image.no_of_contours()
    tetris_image.erode()
    tetris_image.dilate()
    tetris_image.bitwise_and()
