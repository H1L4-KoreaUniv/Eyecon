from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye
import cv2
import tensorflow as tf
import numpy as np


class Process(object):
    def __init__(self, metadata):
        # test change!!
        self.model = tf.keras.models.load_model('model/ver4-6_f(el,er)h_mobile.h5')  # load model
        self.hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')  # for headpose estimation
        self.meta = metadata  # for professor
        self.label_list = []  # Judging on constant focus
        self.count=0
        self.headpose_list=[]
    def check_focus(self):
        a = np.array(self.label_list)
        AVG = np.mean(a)  # get average about student focus
        focus = 0
        if AVG <= 0.2:
            self.meta.warning+=1
            focus = 1
        self.label_list.clear()
        return focus

    # prediction label with model
    def check_label(self, inputs):
        prediction = self.model.predict(inputs)
        print("prediction....", prediction)
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
            print(headpose[0], headpose[1], headpose[2])
            try:
                facelm_img = get_facelm_img(rect, original)
                lefteyelm_img, righteyelm_img = get_eye(landmark_coords, original)
                cv2.imwrite(f'captured_img/facelm_img{self.count}.jpg', facelm_img)
                cv2.imwrite(f'captured_img/eyeleft_img{self.count}.jpg',lefteyelm_img)
                cv2.imwrite(f'captured_img/eyeright_img{self.count}.jpg',righteyelm_img)

                facelm_img=cv2.cvtColor(facelm_img, cv2.COLOR_BGR2RGB)
                lefteyelm_img=cv2.cvtColor(lefteyelm_img,cv2.COLOR_BGR2RGB)
                righteyelm_img=cv2.cvtColor(righteyelm_img,cv2.COLOR_BGR2RGB)
                self.count+=1
                self.headpose_list.append(headpose)
                if facelm_img is None:
                    label = 0
            except:
                print("except error")
                label = 0
        else:
            label = 0
            print('Head pose detection failed')

        if label != 0:
            facelm_img = (facelm_img / 255.0).reshape(1, 224, 224, 3)
            headpose = np.array(headpose).reshape(1, 3)
            lefteyelm_img = (lefteyelm_img / 255.0).reshape(1, 224, 224, 3)
            righteyelm_img = (righteyelm_img / 255.0).reshape(1, 224, 224, 3)
            landmark_coords = np.array(self.hpd.landmarks_to_numpy(landmark_coords)).reshape(1, 68, 2)
            # test change!!
            inputs = [facelm_img, [lefteyelm_img, righteyelm_img], headpose]
            label = self.check_label(inputs)
        print("label : ", label)

        # check attendance
        self.label_list.append(label)
        focus = 0

        if (len(self.label_list) == 5):  # check focus every 10 sec
            focus = self.check_focus()

        # make metadata for professor_page
        meta_dic = {'time': input_time, 'value': label}
        self.meta.student_info.append(meta_dic)
        if meta_dic['value'] == 0:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (0, 0, 255), -1)

        elif meta_dic['value'] == 1:
            output_img = cv2.rectangle(original, (150, 200), (250, 300), (255, 0, 0), -1)

        self.meta.push(meta_dic)

        return output_img, focus
