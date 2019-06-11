import imutils
import cv2

class Image():

    def __init__(self,image,angle):
        self.image = cv2.imread(image)
        self.angle = angle

    # load the input image and show its dimensions, keeping in mind that
    # images are represented as a multi-dimensional NumPy array with
    # shape no. rows (height) x no. columns (width) x no. channels (depth)
    def dimensions(self):
        (h, w, d) = self.image.shape
        print("width={}, height={}, depth={}".format(w, h, d))
        return w,h

    
# display the image to our screen -- we will need to click the window
# open by OpenCV and press a key on our keyboard to continue execution
    def show_image(self):
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)

# access the RGB pixel located at x=50, y=100, keepind in mind that
# OpenCV stores images in BGR order rather than RGB
    def show_rbg(self):
        (B, G, R) = self.image[100, 50]
        print("R={}, G={}, B={}".format(R, G, B))   

# extract a 100x100 pixel square ROI (Region of Interest) from the
# input image starting at x=320,y=60 at ending at x=420,y=160
    def roi(self):
        roi = self.image[60:160, 320:420]
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)

# resize the image to 200x200px, ignoring aspect ratio
    def resize_without_ar(self): #ar = aspect ratio
        resized = cv2.resize(self.image, (200, 200))
        cv2.imshow("Fixed Resizing", resized)
        cv2.waitKey(0)

# fixed resizing and distort aspect ratio so let's resize the width
# to be 300px but compute the new height based on the aspect ratio
    def resize_with_ar(self): #ar = aspecct ratio
        w,h = self.dimensions()
        r = 300.0 / w
        dim = (300, int(h * r))
        resized = cv2.resize(self.image, dim)
        cv2.imshow("Aspect Ratio Resize", resized)
        cv2.waitKey(0)


# manually computing the aspect ratio can be a pain so let's use the
# imutils library instead

    def resize_with_imutils(self):
        resized = imutils.resize(self.image, width=300)
        cv2.imshow("Imutils Resize", resized)
        cv2.waitKey(0)

# let's rotate an image 45 degrees clockwise using OpenCV by first
# computing the image center, then constructing the rotation matrix,
# and then finally applying the affine warp

    def rotate(self):
        w,h = self.dimensions()
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h))
        cv2.imshow("OpenCV Rotation", rotated)
        cv2.waitKey(0)  

# rotation can also be easily accomplished via imutils with less code

    def rotate_with_imutils(self):
        rotated = imutils.rotate(self.image, -45)
        cv2.imshow("Imutils Rotation", rotated)
        cv2.waitKey(0) 

    # OpenCV doesn't "care" if our rotated image is clipped after rotation
    # so we can instead use another imutils convenience function to help
    # us out

    def rotate_with_bound(self):
        rotated = imutils.rotate_bound(self.image, 45)
        cv2.imshow("Imutils Bound Rotation", rotated)
        cv2.waitKey(0)

# apply a Gaussian blur with a 11x11 kernel to the image to smooth it,
# useful when reducing high frequency noise
    def guassian_blur(self):
        blurred = cv2.GaussianBlur(self.image, (11, 11), 0)
        cv2.imshow("Blurred", blurred)
        cv2.waitKey(0)

# draw a 2px thick red rectangle surrounding the face
    def draw_rectangle(self):
        output = self.image.copy()
        cv2.rectangle(output, (320, 60), (420, 160), (0, 0, 255), 2)
        cv2.imshow("Rectangle", output)
        cv2.waitKey(0)

# draw a blue 20px (filled in) circle on the image centered at
# x=300,y=150
    def draw_circle(self):
        output = self.image.copy()
        cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
        cv2.imshow("Circle", output)
        cv2.waitKey(0)

# draw a 5px thick red line from x=60,y=20 to x=400,y=200

    def draw_line(self):
        output = self.image.copy()
        cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
        cv2.imshow("Line", output)
        cv2.waitKey(0)

# draw green text on the image

    def text(self):
        output = self.image.copy()
        cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Text", output)
        cv2.waitKey(0)
    

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