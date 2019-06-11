import imutils
import cv2

class Image():

    def __init__(self,image):
        self.image = cv2.imread(image)
       
    def dimensions(self):
        (h, w, d) = self.image.shape
        print("width={}, height={}, depth={}".format(w, h, d))





image = Image("photo.jpeg")
image.dimensions()
