import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt
import _pickle as pkl
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
from collections import OrderedDict

# model
x, y = pkl.load(open('./head_pose_estimation/model/samples.pkl', 'rb'))

roll, pitch, yaw = y[:, 0], y[:, 1], y[:, 2]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)
std = StandardScaler()
std.fit(x_train)
x_train = std.transform(x_train)
x_val = std.transform(x_val)
x_test = std.transform(x_test)

# test
def detect_face_points(image):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./head_pose_estimation/shape_predictor_68_face_landmarks.dat")
    face_rect = detector(image, 1)
    if len(face_rect) != 1: return []
    
    dlib_points = predictor(image, face_rect[0])
    face_points = []
    for i in range(68):
        x, y = dlib_points.part(i).x, dlib_points.part(i).y
        face_points.append(np.array([x, y]))
    return face_points
        
def compute_features(face_points):
    assert (len(face_points) == 68), "len(face_points) must be 68"
    
    face_points = np.array(face_points)
    features = []
    for i in range(68):
        for j in range(i+1, 68):
            features.append(np.linalg.norm(face_points[i]-face_points[j]))
            
    return np.array(features).reshape(1, -1)


def append_data(path, data, save_path):
    with open(path) as json_file:
        #read json file
        json_data = json.load(json_file)
        #add data
        json_data['data'].append(data)
        json.dumps(json_data,ensure_ascii=False,indent="\t")
        #write
        with open(save_path,'w',encoding="utf-8") as make_file:
            json.dump(json_data, make_file,ensure_ascii=False,indent='\t')
    return json_data

model = load_model('./head_pose_estimation/model/model.h5')
data=[]
for i in range(8,36): #Modified according to the frame number
    
    # Need to change in some cases
    path = './data/1_static_LDH/1_static_LDH_frame'+str(i)+'.jpg'
    # parsing
    spath=path.split('/')
    npath=spath[3].split('_')
    label=npath[0]
    movement=npath[1]
    subject=npath[2]
    file_name = spath[3]
    print(path)
    # test model
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    face_points_list=[]
    face_points = detect_face_points(im)

    for x, y in face_points:
        face_points_list.append([x,y])
        cv2.circle(im, (x, y), 1, (0, 255, 0), -1)

    std = StandardScaler()
    std.fit(x_train)
    features = compute_features(face_points)
    features = std.transform(features)

    y_pred = model.predict(features)

    roll_pred, pitch_pred, yaw_pred = y_pred[0]

    #create json
    #subject, name, label, pitch, yaw, roll,facepoints
    file_data = OrderedDict()
    file_data["subject"]=subject
    file_data["file_name"]=file_name
    file_data["label"]=label
    file_data["movement"]=movement
    file_data["head_pose"]= {'pitch':str(pitch_pred),'yaw':str(yaw_pred),'roll':str(roll_pred)}#pitch,yaw,roll
    file_data["face_points"]=str(face_points_list)
    data.append(file_data)

    
json.dumps(data,ensure_ascii=False,indent="\t")
#write
with open('metadata.json','w',encoding="utf-8") as make_file:
    json.dump(data, make_file,ensure_ascii=False,indent='\t')
