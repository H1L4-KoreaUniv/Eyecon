#video name foramt
#2_downpitch_video1_v1.mp4
#generate_meta.py
import headpose_video
import json
import os
from collections import OrderedDict

#find all video
path_dir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Video/ver3/' #path of video dir
file_list = os.listdir(path_dir)
file_list.sort()
print(file_list)
def parse_name(name): #find label data
    #1_uppitch_ver1_LDH.mp4
    nsp = name.split('_') #name split
    #need to change
    label = nsp[0]
    movement = nsp[1]
    version = nsp[2][3]
# <<<<<< HEAD
    subject = nsp[3].split('.')[0]
# =======
    subject = nsp[3] # LDH.mp4
    subject = subject.split('.')[0] # LDH
# >>>>>>> c6f0492cef010ab38a48b926fdaca3df5bb83344
    return label, movement, version, subject


data = [] #list of metadata 
def get_json(subject, file_name, label, movement, version, head_pose, facelm, facelmname, eyelm, eyelmname): # get json
    file_data = OrderedDict()
    file_data["subject"] = subject
    file_data["file_name"] = file_name
    file_data["label"] = label
    file_data["movement"] = movement
    file_data["version"] = version
    file_data["head_pose"] = {'pitch':str(head_pose[0]),'yaw':str(head_pose[1]),'roll':str(head_pose[2])}#pitch,yaw,roll
    file_data["facelm"] =facelm
    file_data["facelmname"] = facelmname
    file_data["eyelm"] = eyelm
    file_data["eyelmname"] = eyelmname
    data.append(file_data)


imgdir = 'C:/Users/JIWON/workspace_python/Korea_Univ/Project/Data/Image/ver3/'
rawimgdir = imgdir + 'raw_img/' #path of imgdir 
for video in file_list:
    if video == '.DS_Store':
        continue
    print(video)
    path_file = path_dir + video
    label, movement, version, subject = parse_name(video)
    imgname = f'{label}_{movement}_ver{version}_{subject}'
    imgpath = rawimgdir + imgname
    #print(imgname)
    hpd = headpose_video.Headpose_video(path_file,imgpath)
    angle, bbox, facelmfile, eyelmlist = hpd.run_video()
    n = len(angle)
    for i in range(n): #get each frame data
        head_pose = angle[i] #(x,y,z) = (pitch,yaw,roll)
        # facelm = bbox[i]
        bbox[i] = list(map(int,bbox[i])) #make each value int
        facelm = list(map(str, bbox[i])) #make each value str for json
        facelmname = facelmfile[i].split('/')[-1]
        # (facelmname)
        # 눈 좌표 저장 [(x1, y1), (x2, y2)] 형태
        eyelm = list(map(str,eyelmlist[i]))
        # print(imgname)
        # 눈만 자른 이미지 저장된 이름 - 왼쪽 오른쪽 한장씩 
        eyelmname = [imgname + '_frame' + str(i) + '_eyelm_left.jpg', imgname + '_frame' + str(i) + '_eyelm_right.jpg']
        get_json(subject, video, label, movement, version, head_pose, facelm, facelmname, eyelm, eyelmname)

#write 
datadict = {}
datadict['data'] = data 
json.dumps(datadict, ensure_ascii=False, indent="\t")

with open('metadata_ver3_LJW3.json', 'w', encoding="utf-8") as make_file:
    json.dump(datadict, make_file, ensure_ascii=False, indent='\t')