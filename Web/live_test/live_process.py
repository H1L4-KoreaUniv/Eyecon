from generate_data.headpose import HeadposeDetection
from generate_data.cut_facelm import get_facelm_img
from generate_data.cut_eyelm import get_eye
import cv2
import tensorflow as tf
import numpy as np


class Process(object):
    def __init__(self, metadata):
        # change!!
        self.model = tf.keras.models.load_model('live_test/model/Deep_Mobile')  # load model
        self.hpd = HeadposeDetection(1,
                                     'live_test/model/shape_predictor_68_face_landmarks.dat')  # for headpose estimation
        self.meta = metadata  # for teacher
        self.label_list = []  # Judging on constant focus

    def check_focus(self):
        a = np.array(self.label_list)
        AVG = np.mean(a)  # get average about student focus
        focus = 0
        if AVG <= 0.2:
            self.meta.warning += 1
            focus = 1
        self.label_list.clear()
        return focus

    # prediction label with model
    def check_label(self, inputs):
        prediction = self.model.predict(inputs)
        # print("prediction....", prediction)
        prediction = 1 if prediction >= 0.5 else 0
        return prediction  # or 0 # 50% 상이면 1 아니면 0!

    # get input for model and get ouput_img
    def process_img(self, input):
        input_img = input[0]
        input_time = input[1]
        original = input_img.copy()

        _, headpose, bbox = self.hpd.process_image(input_img)
        landmark_coords, _, rect = self.hpd.get_landmarks(original)
        label = -1
        # if there is no headpose estimation then label is zero
        if (headpose is not None) and (landmark_coords is not None):
            # print(headpose[0], headpose[1], headpose[2])
            try:
                facelm_img = get_facelm_img(rect, original)
                lefteyelm_img, righteyelm_img = get_eye(landmark_coords, original)
                facelm_img = cv2.cvtColor(facelm_img, cv2.COLOR_BGR2RGB)
                lefteyelm_img = cv2.cvtColor(lefteyelm_img, cv2.COLOR_BGR2RGB)
                righteyelm_img = cv2.cvtColor(righteyelm_img, cv2.COLOR_BGR2RGB)
                if facelm_img is None:
                    label = 0
            except:
                print("except error")
                label = 0
        else:
            label = 0
            print('Head pose detection failed')
        if label != 0:
            facelm_img = (facelm_img / 255.0).reshape(1, 152, 152, 3)
            lefteyelm_img = (lefteyelm_img / 255.0).reshape(1, 224, 224, 3)
            righteyelm_img = (righteyelm_img / 255.0).reshape(1, 224, 224, 3)
            headpose = np.array(headpose).reshape(1, 3)
            headpose[0][0] = (headpose[0][0] - (-2.197817099482598)) / 7.068855130829307
            headpose[0][1] = (headpose[0][1] - (-0.7655871715669659)) / 16.022392917636346
            headpose[0][2] = (headpose[0][2] - (0.5030293287537536)) / 6.097833417815505
            inputs = [facelm_img, lefteyelm_img, righteyelm_img, headpose]
            label = self.check_label(inputs)
        # print("label : ", label)

        # check attendance
        self.label_list.append(label)
        focus = 0

        if len(self.label_list) == 30:  # check focus every 30 sec
            focus = self.check_focus()

        # make metadata for professor_page
        self.meta.sum += label
        meta_dic = {'time': input_time, 'value': label, 'data_rate': round(self.meta.sum / self.meta.cnt, 2)}
        self.meta.student_info.append(meta_dic)
        self.meta.cnt += 1
        if meta_dic['value'] == 0:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (0, 0, 255), -1)

        elif meta_dic['value'] == 1:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (255, 0, 0), -1)

        self.meta.push(meta_dic)

        return output_img, focus
