import cv2
import glob
import os
import time
import argparse

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image_dir", type=str, default="", help="directory for images")

class Image2Video:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.writer = cv2.VideoWriter()
        fourcc = cv2.VideoWriter.fourcc(*"H264")
        filename = "{}.avi".format(int(time.time()))
        self.writer.open(filename, fourcc, fps, (width, height))
        if not self.writer.isOpened():
            print("H264 does not support, switch to MJPG")
            fourcc = cv2.VideoWriter.fourcc(*"MJPG")
            self.writer.open(filename, fourcc, fps, (width, height))

    def record(self, img_dir):
        imgpaths = []
        for fmt in ["*.jpg", "*.png"]:
            paths = glob.glob(os.path.join(img_dir, fmt))
            imgpaths.extend(paths)

        i = 0
        while self.writer.isOpened():
            img_p = imgpaths[i]
            img = cv2.imread(img_p)
            img = cv2.resize(img, (self.width, self.height))
            self.writer.write(img)
            time.sleep(1 / self.fps)  # sleep by fps
            cv2.imshow("img", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyAllWindows()
                self.writer.release()
                break
            i = (i + 1) % len(imgpaths)


if __name__ == '__main__':
    
    img2video = Image2Video(1280, 720, 20)
    img2video.record("")
