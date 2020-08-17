# Lee Jiwon
# 2020-08-17-21:50
# Check if there are 

import os
import re


path = r'C:\Users\JIWON\workspace_python\Korea_Univ\Project\Data\Image\ver3'


raw = os.listdir(path + r'\raw_img')
face = os.listdir(path + r'\facelm_img')
eye = os.listdir(path + r'\eyelm_img')


raw_list = []
for _ in range(len(raw)):
    raw_list.append(raw[_][:-4])
    
face_list = []
for _ in range(len(face)):
    face_list.append(face[_][:-11])
    
eye_list = []
for _ in range(len(eye)):
    eye_list.append(re.sub(re.findall('_\w{5}_\w{4,5}[.]\w{3}', eye[_])[0], '', eye[_]))
    
    
    
print('raw vs face: ', set(raw_list) ^ set(face_list))
print('face vs eye: ', set(face_list) ^ set(eye_list))
print('eye vs raw: ', set(eye_list) ^ set(raw_list))