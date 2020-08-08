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

class Headpose_video():
    def __init__(self, input_file, ouput_file):
        self.filename=input_file #video path
        self.cnt=0
        self.imgfile=ouput_file
    
    def get_land_img(self, bbox,original):
        x1=int(bbox[0]) 
        y1=int(bbox[1]) 
        y2=int(bbox[3])
        facelmname = f'{self.imgfile}frame{self.cnt}_facelm.jpg'
        cv2.imwrite(facelmname, cv2.resize(original[ y1:y2, x1:x1+y2-y1], dsize=(300, 300), interpolation=cv2.INTER_AREA))
        return facelmname

    def run_video(self):
        cap = cv2.VideoCapture(self.filename)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        hpd = headpose.HeadposeDetection(1,'model/shape_predictor_68_face_landmarks.dat')

        ang=[]
        box=[]
        facelmname=[]
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None: 
                break
            else:
                original = frame.copy()
                frame, angles, bbox = hpd.process_image(frame)
                if bbox is None:
                    continue
                else:
                    if(int(cap.get(1)) % 30 == 0): #fps에 따라 다르게
                        facelmname.append(self.get_land_img(bbox,original))
                        ang.append(angles)
                        box.append(bbox)
                        #print(angles) #angle
                        #print(bbox)
                        print(f'Saved frame{self.cnt}.jpg')
                        self.cnt += 1
        cap.release()
        cv2.destroyAllWindows()
        return ang, box, facelmname