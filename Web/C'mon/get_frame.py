import threading
from time import sleep
# from process_frame import  process_frame

from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye
import datetime
import random
import cv2

class Get_frame(object):
    def __init__(self,meta):
        self.input_queue=[]
        self.out_queue=[]
        self.hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
        self.meta = meta

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.input_queue:
            return
        input = self.input_queue.pop()
        input_img=input[0]
        input_time=input[1]
        print("input_time: ",input_time)
        original = input_img.copy()
        _, angles, bbox = self.hpd.process_image(input_img)
        landmark_coords, _, rect = self.hpd.get_landmarks(original)

        if (angles is not None) and (landmark_coords is not None):
            print(angles[0], angles[1], angles[2])
            try:
                facelm_img = get_facelm_img(rect, original)
                lefteyelm_img, righteyelm_img = get_eye(landmark_coords, original)
                if facelm_img is None:
                    label = 0
            except:
                print("except error")
                label = 0  # 에러 뜨면 라벨 0으로 처리해버리기
            # return angles, facelm_img, lefteyelm_img, righteyelm_img
        else:
            label = 0
            print('Head pose detection failed')

        meta_dic = {'time': input_time, 'value': random.randrange(0, 2)}
        if meta_dic['value'] == 0:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (255, 0, 0), -1)

        elif meta_dic['value'] == 1:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (0, 0, 255), -1)

        self.meta.push(meta_dic)
        print(len(self.meta.queue))
        output_img = cv2.flip(output_img, 1)  # 그냥 frame에 출력하면됌
        ret, jpeg = cv2.imencode('.jpg', output_img)
        self.out_queue.append(jpeg)

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