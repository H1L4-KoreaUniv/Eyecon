# title           : generate_data.py
# description     : Generate face image, left eye image, right eye image and headpose values for input of model.  
# date            : 20200818
# python_version  : 3.8.3
# ==============================================================================

import cv2
import numpy as np
import os
import json
from collections import OrderedDict
from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye

# NOTICE ======================================================================
# 비디오 파일명 형식 : 1_LDH3.mp4
# 반드시 json 파일 저장 이름 체크, 덮어쓰지 않게 주의할 것
# ============================================================================

# 비디오 폴더 경로 작성
video_dir = 'C:/Users/sodaus/Desktop/data/ver3456final/video/' #path of video dir
file_list = os.listdir(video_dir)
file_list.sort()
print(file_list)

# 이미지 저장할 폴더 경로 작성
img_dir = 'C:/Users/sodaus/Desktop/data/ver3456final/img/'

# 비디오 파일 이름을 인자로 받아 parsing한 값을 리턴하는 함수
def parse_name(video_name): 
    temp = video_name.split('_') #name split
    label = temp[0]
    subject = temp[1].split('.')[0]
    
    return video_name, label, subject


# metadata를 저장하기 위한 함수
data = [] #list of metadata 
def get_json(subject, video_name, frame_num, label, head_pose, faceimg_name, eyeimg_name): # get json
    file_data = OrderedDict()
    file_data["video_name"] = video_name
    file_data["frame_num"] = frame_num
    file_data["subject"] = subject
    file_data['label'] = label
    file_data["head_pose"] = {'pitch':str(head_pose[0]),'yaw':str(head_pose[1]),'roll':str(head_pose[2])}#pitch,yaw,roll
    # file_data["face_landmarks"] = face_landmarks
    file_data["faceimg_name"] = faceimg_name
    file_data["eyeimg_name"] = eyeimg_name
    data.append(file_data)

    
# 비디오 파일 이름을 인자로 받는 data preprocessing 함수 
def preprocessing(video_name):
    hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
    video_name, label, subject = parse_name(video_name)
    img_name = f'{label}_{subject}'
    print(video_dir + video_name)
    video = cv2.VideoCapture(video_dir + video_name)
    # frame per sec 확인
    fps = int(video.get(cv2.CAP_PROP_FPS))
    # 해당 초(sec)마다 영상에서 프레임 추출
    sec = 1
    count = 0
    frame_num = 0
    
    while video.isOpened():
        ret, frame = video.read()
        if frame is None:
            print("frame is none")
            break
        original = frame.copy()

        # 1초마다 프레임 추출하여 preprocessing
        count += 1
        if count % (fps*sec) == 0:
            _, angles, bbox = hpd.process_image(frame)
            landmark_coords, _,rect = hpd.get_landmarks(original)
            
            # face landmarks와 head pose 모두 detection 되었는지 검사
            if (landmark_coords is not None) and (angles is not None): 
                # head pose values
                head_pose = angles
                # face landmark coordinates
                # landmarks = hpd.landmarks_to_numpy(landmark_coords)
                # face_landmarks = landmarks
                # face image 추출 되는지 확인
                try:
                    faceimg = get_facelm_img(rect, original)
                except:
                    print('pass frame') # 에러 뜨면 meatadata 저장 안함
                    continue 
                # eye image 추출 되는지 확인
                try:
                    lefteyeimg, righteyeimg = get_eye(landmark_coords, original)
                except:
                    print('pass frame') # 에러 뜨면 metadata 저장 안함
                    continue 
                   
                # 모든 preprocessing 문제 없을 경우 이미지 저장
                faceimg_dir = img_dir + img_name + f'_frame{frame_num}_face.jpg'
                cv2.imwrite(faceimg_dir, faceimg)
                lefteyeimg_dir = img_dir + img_name + f'_frame{frame_num}_eye_left.jpg'
                righteyeimg_dir = img_dir + img_name + f'_frame{frame_num}_eye_right.jpg'
                cv2.imwrite(lefteyeimg_dir, lefteyeimg)
                cv2.imwrite(righteyeimg_dir, righteyeimg)
                
                faceimg_name = img_name + f'_frame{frame_num}_face.jpg'
                eyeimg_name = [img_name + f'_frame{frame_num}_eye_left.jpg', img_name + f'_frame{frame_num}_eye_right.jpg']
                
                print('Saved frame%d' % frame_num)
                
                get_json(subject, video_name, frame_num, label, head_pose, faceimg_name, eyeimg_name)
                frame_num += 1
            else:
                print('pass frame due to head pose')


# 실행을 위한 함수 호출
for video in file_list:
    if video == '.DS_Store':
        continue
    print(video)
    preprocessing(video)
    
    
# metadata 저장을 위한 json 파일 생성 
datadict = {}
datadict['data'] = data 
json.dumps(datadict, ensure_ascii=False, indent="\t")
with open('C:/Users/sodaus/Desktop/data/ver3456final/final_metadata2.json', 'w', encoding="utf-8") as make_file:
    json.dump(datadict, make_file, ensure_ascii=False, indent='\t')

