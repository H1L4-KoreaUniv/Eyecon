#video name foramt
#2_downpitch_video1_v1.mp4

import headpose_video
import json
import os
from collections import OrderedDict

#find all video
path_dir = '/Users/hong-yujin/Downloads/test' #path of video dir
file_list=os.listdir(path_dir)
file_list.sort()

def parse_name(name): #find label data
    #3_uppitch_video1_v1.mp4
    nsp=name.split('_') #name split
    #need to change
    label = nsp[0]
    movement= nsp[1]
    version = nsp[3][1]
    subject = 'HYJ'
    return label,movement,version,subject


data=[] #list of metadata 
def get_json(subject,file_name,label,movement,version,head_pose,facelm,facelmname,eyelm,eyelmname): # get json
    file_data = OrderedDict()
    file_data["subject"]=subject
    file_data["file_name"]=file_name
    file_data["label"]=label
    file_data["movement"]=movement
    file_data["version"]=version
    file_data["head_pose"]= {'pitch':str(head_pose[0]),'yaw':str(head_pose[1]),'roll':str(head_pose[2])}#pitch,yaw,roll
    file_data["facelm"]=facelm
    file_data["facelmname"]=facelmname
    file_data["eyelm"]=eyelm
    file_data["eyelmname"]=eyelmname
    data.append(file_data)


imgdir = '/Users/hong-yujin/Downloads/test_img/' #path of imgdir
for video in file_list:
    if video == '.DS_Store':
        continue
    path_file = path_dir+'/'+video
    label,movement,version,subject=parse_name(video)
    imgpath=imgdir+f'{label}_{movement}_ver{version}_{subject}_'

    hpd = headpose_video.Headpose_video(path_file,imgpath)
    angle,bbox, facelmfile = hpd.run_video()
    n = len(angle)
    for i in range(n): #get each frame data
        head_pose=angle[i] #(x,y,z) = (pitch,yaw,roll)
        #facelm=bbox[i]
        bbox[i]=list(map(int,bbox[i])) #make each value int
        facelm = list(map(str, bbox[i])) #make each value str for json
        facelmname=facelmfile[i].split('/')[-1]
        eyelm=[['33','33'],['44','44']] #need to change
        eyelmname=[imgpath.split('/')[-1]+'frame'+str(i)+'_lefteyelm.jpg',imgpath.split('/')[-1]+'frame'+str(i)+'_righteyelm.jpg']
        get_json(subject,video,label,movement,version,head_pose,facelm,facelmname,eyelm,eyelmname)

#write 
datadict={}
datadict['data']= data
json.dumps(datadict,ensure_ascii=False,indent="\t")

with open('metadata.json','w',encoding="utf-8") as make_file:
    json.dump(datadict, make_file,ensure_ascii=False,indent='\t')
