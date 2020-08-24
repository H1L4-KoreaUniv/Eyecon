"""
Created on Tue Aug 18 22:28:19 2020
@author: 이다혜
"""
import cv2
import numpy as np
import os
import json
from collections import OrderedDict
from headpose import HeadposeDetection
from cut_facelm import get_facelm_img
from cut_eyelm import get_eye

# NOTICE ======================================================================
# 비디오 파일명 형식 : 1_free_ver1_LDH3.mp4
# 아래 directory가 모두 동위에 있어야 하며, 그렇지 않을 경우 경로 수정 필요
'''
- video # 비디오 있는 폴더
- facelm_img # 얼굴 사진 저장할 폴더
- eyelm_img # 눈 사진 저장할 폴더
- generate_data.py 
'''
# 반드시 json 파일 저장 이름 체크, 덮어쓰지 않게 주의할 것
# ============================================================================

# 비디오 폴더 경로 작성
path_dir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/ver3/Video_friend/' #path of video dir
file_list = os.listdir(path_dir)
file_list.sort()
print(file_list)


# 비디오 파일 이름을 인자로 받아 parsing한 값을 리턴하는 함수
def parse_name(videoname): 
    temp = videoname.split('_') #name split
    label = temp[0]
    version = temp[2][3]
    subject = temp[3].split('.')[0]
    return videoname, label, version, subject


# metadata를 저장하기 위한 함수
data = [] #list of metadata 
def get_json(subject, file_name, label, version, head_pose, face_landmarks, facelmname, eyelmname): # get json
    file_data = OrderedDict()
    file_data["subject"] = subject
    file_data["file_name"] = file_name
    file_data["label"] = label
    file_data["version"] = version
    file_data["head_pose"] = {'pitch':str(head_pose[0]),'yaw':str(head_pose[1]),'roll':str(head_pose[2])}#pitch,yaw,roll
    file_data["face_landmarks"] =face_landmarks
    file_data["facelmname"] = facelmname
    file_data["eyelmname"] = eyelmname
    data.append(file_data)

    
# 비디오 파일 이름을 인자로 받는 data preprocessing 함수 
def preprocessing(videoname):
    hpd = HeadposeDetection(1, 'model/shape_predictor_68_face_landmarks.dat')
    file_name, label, version, subject = parse_name(videoname)
    imgname = f'{label}_ver{version}_{subject}'
    print(path_dir + videoname)
    video = cv2.VideoCapture(path_dir + videoname)
    # frame per sec 확인
    fps = int(video.get(cv2.CAP_PROP_FPS))
    # 해당 초(sec)마다 영상에서 프레임 추출
    sec = 1
    count = 0
    framenum = 0
    
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
                landmarks = hpd.landmarks_to_numpy(landmark_coords)
                face_landmarks = landmarks
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
                faceimgname = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/ver3/Image_friend/facelm_img/' + imgname + f'_frame{framenum}_facelm.jpg'
                cv2.imwrite(faceimgname, faceimg)
                lefteyeimgname = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/ver3/Image_friend/eyelm_img/' + imgname + f'_frame{framenum}_eyelm_left.jpg'
                righteyeimgname = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/ver3/Image_friend/eyelm_img/' + imgname + f'_frame{framenum}_eyelm_right.jpg'
                cv2.imwrite(lefteyeimgname, lefteyeimg)
                cv2.imwrite(righteyeimgname, righteyeimg)
                
                facelmname = imgname + f'_frame{framenum}_facelm.jpg'
                eyelmname = [imgname + f'_frame{framenum}_eyelm_left.jpg', imgname + f'_frame{framenum}_eyelm_right.jpg']
                
                framenum += 1
                print('Saved frame%d' % framenum)
                # print(subject, file_name, label, version, head_pose, face_landmarks, facelmname, eyelmname)
                get_json(subject, file_name, label, version, head_pose, face_landmarks, facelmname, eyelmname)
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
with open('C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/ver3/Image_friend/metadata_ver3_LJWFRIENDS1.json', 'w', encoding="utf-8") as make_file:
    json.dump(datadict, make_file, ensure_ascii=False, indent='\t')
    
