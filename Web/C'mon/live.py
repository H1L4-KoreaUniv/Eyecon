import cv2

import datetime
import random


def webcam(camera, Frame):
    """Video streaming generator function."""
    sec = 1
    count = 0
    while camera.isOpened():
        ret, frame = camera.read()
        fps=camera.get(cv2.CAP_PROP_FPS)
        if frame is None:
            print("frame is none")
            break
        if count % (int(fps) * sec) == 0:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #print("time: ",time)
            Frame.push([frame,time])
        frame = cv2.flip(frame, 1)  # 그냥 frame에 출력하면됌
        ret, jpeg = cv2.imencode('.jpg', frame)
        # print("after get_frame")
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            print("frame is none")
        count+=1