# USAGE
# python Tut_1.py


import imutils
import cv2

class Image():

    def __init__(self,image,angle):
        self.image = cv2.imread(image)
        self.angle = angle

    def dimensions(self):
        (h, w, d) = self.image.shape
        print("width={}, height={}, depth={}".format(w, h, d))
        return w,h

    
    def show_image(self):
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)

    def show_rbg(self):
        (B, G, R) = self.image[100, 50]
        print("R={}, G={}, B={}".format(R, G, B))   

    def roi(self):
        roi = self.image[60:160, 320:420]
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)

    def resize_without_ar(self): #ar = aspect ratio
        resized = cv2.resize(self.image, (200, 200))
        cv2.imshow("Fixed Resizing", resized)
        cv2.waitKey(0)

    def resize_with_ar(self): #ar = aspecct ratio
        w,h = self.dimensions()
        r = 300.0 / w
        dim = (300, int(h * r))
        resized = cv2.resize(self.image, dim)
        cv2.imshow("Aspect Ratio Resize", resized)
        cv2.waitKey(0)


    def resize_with_imutils(self):
        resized = imutils.resize(self.image, width=300)
        cv2.imshow("Imutils Resize", resized)
        cv2.waitKey(0)


    def rotate(self):
        w,h = self.dimensions()
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h))
        cv2.imshow("OpenCV Rotation", rotated)
        cv2.waitKey(0)  


    def rotate_with_imutils(self):
        rotated = imutils.rotate(self.image, -45)
        cv2.imshow("Imutils Rotation", rotated)
        cv2.waitKey(0) 


    def rotate_with_bound(self):
        rotated = imutils.rotate_bound(self.image, 45)
        cv2.imshow("Imutils Bound Rotation", rotated)
        cv2.waitKey(0)

    def guassian_blur(self):
        blurred = cv2.GaussianBlur(self.image, (11, 11), 0)
        cv2.imshow("Blurred", blurred)
        cv2.waitKey(0)

    def draw_rectangle(self):
        output = self.image.copy()
        cv2.rectangle(output, (320, 60), (420, 160), (0, 0, 255), 2)
        cv2.imshow("Rectangle", output)
        cv2.waitKey(0)

    def draw_circle(self):
        output = self.image.copy()
        cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
        cv2.imshow("Circle", output)
        cv2.waitKey(0)



    def draw_line(self):
        output = self.image.copy()
        cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
        cv2.imshow("Line", output)
        cv2.waitKey(0)



    def text(self):
        output = self.image.copy()
        cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Text", output)
        cv2.waitKey(0)
    

if __name__ == "__main__":
    image = Image("jp.png",-45)
    image.dimensions()
    image.show_image()
    image.show_rbg()
    image.roi()
    image.resize_without_ar()
    image.resize_with_ar()
    image.resize_with_imutils()
    image.rotate()
    image.rotate_with_imutils()
    image.rotate_with_bound()
    image.guassian_blur()
    image.draw_rectangle()
    image.draw_circle()
    image.draw_line()
    image.text()