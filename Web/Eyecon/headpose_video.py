#
#   Headpose Detection for Video
#   Written by Qhan
#   Last Update: 2019.1.9
#

import argparse
import cv2
import numpy as np
import os.path as osp
import headpose
# import Gaze_Tracking
# from Gaze_Tracking.eye_detection import detect_eye


class Headpose_video():
    def __init__(self, input_file, ouput_file):
        self.filename=input_file #video path
        self.cnt=0
        self.imgfile=ouput_file
    
    # def get_land_img(self, bbox,original):
    #     x1=int(bbox[0])
    #     y1=int(bbox[1])
    #     y2=int(bbox[3])
    #     # 얼굴 사진 따로 저장할 하위 폴더명
    #     facelmdir = 'facelm_img/'
    #     # 전체 경로 포함한 저장 파일명
    #     facelmname = self.imgfile.split('/')[0] + '/' + facelmdir + self.imgfile.split('/')[-1] + f'frame{self.cnt}_facelm.jpg'
    #     cv2.imwrite(facelmname, cv2.resize(original[ y1:y2, x1:x1+y2-y1], dsize=(300, 300), interpolation=cv2.INTER_AREA))
    #     return facelmname

    def run_video(self):
        cap = cv2.VideoCapture(self.filename)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        hpd = headpose.HeadposeDetection(1,'model/shape_predictor_68_face_landmarks.dat')
        
        ang=[]
        box=[]
        facelmname=[]
        eyelmlist=[]
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None: 
                break
            else:
                original = frame.copy()
                eyelm = detect_eye(original)
                frame, angles, bbox = hpd.process_image(frame)
                
                if bbox is None:
                    print('pass bbox')
                    continue
                else:
                    if(int(cap.get(1)) % 30 == 0): #fps에 따라 다르게
                        # 눈 사진 따로 저장할 하위 폴더명
                        eyelmdir = 'eyelm_img/'
                        # 전체 경로 포함 
                        eyelmname = self.imgfile.split('/')[0] + '/' + eyelmdir + self.imgfile.split('/')[-1] + f'frame{self.cnt}_eyelm' # 눈 부분만 저장    
                        if (hpd.get_eye(image=original, path=eyelmname) is None):
                            print("pass get eye")
                            continue
                        facelmname.append(self.get_land_img(bbox,original))
                        ang.append(angles)
                        box.append(bbox)
                        eyelmlist.append(eyelm)
                        
                        
                        #print(angles) #angle
                        #print(bbox)
                        imgname = f'{self.imgfile}frame{self.cnt}.jpg' # 캡쳐한 raw 이미지 저장
                        cv2.imwrite(imgname, original)
                        print(f'Saved frame{self.cnt}.jpg') 
                        
                        self.cnt += 1
        cap.release()
        cv2.destroyAllWindows()
        return ang, box, facelmname, eyelmlist