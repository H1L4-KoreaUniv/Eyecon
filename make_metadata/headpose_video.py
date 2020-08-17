# headpose_video.py
#   Headpose Detection for Video
#   Written by Qhan
#   Last Update: 2019.1.9
#

import argparse
import cv2
import numpy as np
import os.path as osp
import headpose
import Gaze_Tracking 
from Gaze_Tracking.eye_detection import detect_eye


class Headpose_video():
    def __init__(self, input_file, ouput_file):
        self.filename = input_file  # video path
        self.cnt = 0
        self.imgfile = ouput_file
    
    def get_land_img(self, bbox, original):
        x1 = int(bbox[0]) 
        y1 = int(bbox[1]) 
        y2 = int(bbox[3])
        # 얼굴 사진 따로 저장할 하위 폴더명
        facelmdir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Image/ver3/facelm_img/'
        # 전체 경로 포함한 저장 파일명
        facelmname = facelmdir + self.imgfile.split('/')[-1] + f'_frame{self.cnt}_facelm.jpg'
        # facelmname = self.imgfile.split('/')[0] + '/' + facelmdir + self.imgfile.split('/')[-1] + f'frame{self.cnt}_facelm.jpg'
        try:
            cv2.imwrite(facelmname, cv2.resize(original[ y1:y2, x1:x1+y2-y1], dsize=(300, 300), interpolation=cv2.INTER_AREA))
        except cv2.error as e:
            print('invalid frame: ', self.cnt)
            return None
        return facelmname

    def run_video(self):
        cap = cv2.VideoCapture(self.filename)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        hpd = headpose.HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
        
        ang = []
        box = []
        facelmname = []
        eyelmlist = []
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None: 
                break
            else:
                original = frame.copy()
                try:
                    eyelm = detect_eye(original)
                except cv2.error as e:
                    print('detect_eye(original) error: ', eyelmname)
                    continue
                frame, angles, bbox = hpd.process_image(frame)
                
                if bbox is None:
                    print("pass bbox")
                    continue
                else:
                    if(int(cap.get(1)) % 16 == 0):  #fps에 따라 다르게
                        eyelmdir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Image/ver3/eyelm_img/'
                        eyelmname = eyelmdir + self.imgfile.split('/')[-1] + f'_frame{self.cnt}_eyelm'
                        if(hpd.get_eye(image=original, path=eyelmname) is None):
                            print("pass get eye")
                            continue
                        tmp = self.get_land_img(bbox,original)
                        if (tmp is not None):
                            facelmname.append(tmp)
                        else:
                            continue
                        ang.append(angles)
                        box.append(bbox)
                        eyelmlist.append(eyelm)
                        # 눈 사진 따로 저장할 하위 폴더명
                        eyelmdir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Image/ver3/eyelm_img/'
                        # 전체 경로 포함
                        
                        #eyelmname = self.imgfile.split('/')[0] + '/' + eyelmdir + self.imgfile.split('/')[-1] + f'frame{self.cnt}_eyelm'  # 눈 부분만 저장
                        #hpd.get_eye(image=original, path=eyelmname)
                        #print(angles) #angle
                        #print(bbox)
                        temp = self.imgfile.split('/')[-1]
                        imgname = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Image/ver3/raw_img/'+f'{temp}_frame{self.cnt}.jpg'  # 캡쳐한 raw 이미지 저장
                        cv2.imwrite(imgname, original)
                        print(f'Saved frame{self.cnt}.jpg') 
                        
                        self.cnt += 1
        cap.release()
        cv2.destroyAllWindows()
        return ang, box, facelmname, eyelmlist