import cv2
import os

path  = os.path.dirname(os.path.abspath('__file__'))


def get_img(path=path):
    categories = [0,1,2,3,4]
    for category in categories:
        for video in os.listdir(path+'\\videos\{}' .format(category)):
            capture = cv2.VideoCapture(os.path.join(str(path+'\\videos\{}' .format(category)), video))
            count = 0
            while(capture.isOpened()):
                ret, image = capture.read()
                if ret:
                    count += 1
                    if count % 5 == 0: # FPS=20 이면 5, 30이면 6
                        cv2.imwrite(path+"\data\image\{}\\{} frame{}.jpg" .format(category, video, count), image)
                        print('Saved frame {} .jpg' .format(count))
                        count += 1
                else:
                    capture.release()
            

get_img(path)

