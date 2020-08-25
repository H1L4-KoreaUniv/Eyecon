import threading
from time import sleep
# from process_frame import  process_frame

from flask_socketio import SocketIO, emit
import cv2

from app import socketio


class Get_frame(object):
    def __init__(self, Process):
        self.input_queue=[]
        self.out_queue=[]
        self.process = Process
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.input_queue:
            return
        input = self.input_queue.pop()
        output_img,attendance = self.process.process_img(input)
        output_img = cv2.flip(output_img, 1)  # 그냥 frame에 출력하면됌
        ret, jpeg = cv2.imencode('.jpg', output_img)
        self.out_queue.append([jpeg,attendance])

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def push(self, input):
        #input type is json{ time, label, name}
        self.input_queue.append(input)

    def pop(self):
        while not self.queue:
            continue
        return self.input_queue.pop(0)

    def get_frame(self):
        while not self.out_queue:
            sleep(0.05)
        return self.out_queue.pop(0)