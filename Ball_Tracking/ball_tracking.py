# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

class Track():
    def __init__(self,args):
        self.args = args
    
    def green(self):
        green_min = (29, 86, 6)
        green_max = (64, 255, 255)
        points = deque(maxlen=args["buffer"])
        return green_max,green_min,points

    def video_or_webcam(self):
        if not args.get("video", False):
            video_stream = VideoStream(src=0).start()

        
        else:
            video_stream = cv2.VideoCapture(args["video"])
        time.sleep(2.0)
        return video_stream

    def track(self):
        green_max,green_min,points = self.green()
        video_stream = self.video_or_webcam()
        while True:
            frame = video_stream.read()

            frame = frame[1] if args.get("video", False) else frame

            if frame is None:
                break

            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, green_min, green_max)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            center = None

            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            points.appendleft(center)

            for i in range(1, len(points)):
                if points[i - 1] is None or points[i] is None:
                    continue

                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, points[i - 1], points[i], (0, 0, 255), thickness)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        if not args.get("video", False):
            video_stream.stop()

        else:
            video_stream.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())
    
    ball = Track(args)
    ball.track() 