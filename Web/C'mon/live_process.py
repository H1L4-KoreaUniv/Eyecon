from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye
import random
import cv2
import tensorflow as tf
import datetime
import numpy as np

from flask_socketio import SocketIO, emit
from tkinter import messagebox

class Process(object):
    def __init__(self, metadata):
        self.model = tf.keras.models.load_model('model/goodmodel.h5')
        self.hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
        self.meta = metadata
        self.label_list = []
        self.status = 0

    def check_attendance(self):
        a = np.array(self.label_list)
        AVG = np.mean(a)
        attendanace=0
        if AVG <= 0.2:
            attendanace=1
        self.label_list.clear()
        return attendanace

    def check_label(self, inputs):
        prediction = self.model.predict(inputs)
        print("prediction....", prediction)
        prediction = 1 if prediction >= 0.5 else 0
        return prediction  # or 0 # 50% 상이면 1 아니면 0!

    def process_img(self, input):
        input_img = input[0]
        input_time = input[1]
        original = input_img.copy()

        _, headpose, bbox = self.hpd.process_image(input_img)
        landmark_coords, _, rect = self.hpd.get_landmarks(original)

        label = -1
        if (headpose is not None) and (landmark_coords is not None):
            print(headpose[0], headpose[1], headpose[2])
            try:
                facelm_img = get_facelm_img(rect, original)
                lefteyelm_img, righteyelm_img = get_eye(landmark_coords, original)
                if facelm_img is None:
                    label = 0
            except:
                print("except error")
                label = 0  # 에러 뜨면 라벨 0으로 처리해버리기
        else:
            label = 0
            print('Head pose detection failed')

        if label != 0:
            facelm_img = (facelm_img // 255.0).reshape(1, 224, 224, 3)
            headpose = np.array(headpose).reshape(1, 3)
            lefteyelm_img = (lefteyelm_img // 255.0).reshape(1, 224, 224, 3)
            righteyelm_img = (righteyelm_img // 255.0).reshape(1, 224, 224, 3)
            landmark_coords = np.array(self.hpd.landmarks_to_numpy(landmark_coords)).reshape(1, 68, 2)
            inputs = [facelm_img,lefteyelm_img, righteyelm_img,headpose]
            label = self.check_label(inputs)
        print("label : ", label)

        # check attendance
        self.label_list.append(label)
        attendance=0
        if (len(self.label_list) == 300):  # every 3 minutes
            attendance=self.check_attendance()

        # make metadata for professor_page
        meta_dic = {'time': input_time, 'value': label}
        if meta_dic['value'] == 0:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (0, 0, 255), -1)

        elif meta_dic['value'] == 1:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (255, 0, 0), -1)

        self.meta.push(meta_dic)

        return output_img,attendance
