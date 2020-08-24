# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:56:04 2020

@author: sodaus
"""

import os, shutil, random, datetime, json
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import tensorflow as tf
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation, Concatenate
from tensorflow.keras.utils import plot_model

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# GPU 관련 코드
from numba import cuda
from tensorflow.python.client import device_lib
import json

with open(r'C:\Users\sodaus\Desktop\test0818\metadata_merge.json') as json_file:
    meta = json.load(json_file)
meta['data']

random.shuffle(meta['data'])


# print(meta['data'][0]['facelmname'])
#get json file and make np.array
facelm_img =np.array([cv2.imread(os.path.join(r'C:\Users\sodaus\Desktop\test 0815\facelm_img',x['facelmname'])) for x in meta['data']])
headpose= np.array([(np.array(list(x['head_pose'].values())).astype('float')) for x in meta['data']])
eyelm_left =np.array([cv2.imread(os.path.join(r'C:\Users\sodaus\Desktop\test 0815\eyelm_img\left',x['eyelmname'][0])) for x in meta['data']])
eyelm_right =np.array([cv2.imread(os.path.join(r'C:\Users\sodaus\Desktop\test 0815\eyelm_img\right',x['eyelmname'][1])) for x in meta['data']])
# facelm=np.array([x['facelm'] for x in meta['data']])

data_list=[facelm_img,headpose,eyelm_left,eyelm_right]


print(facelm_img.shape)
# print(facelm[0])
print(type(headpose[0][0]))
# facelm_img_re=np.reshape(facelm_img,(facelm_img.shape[0],300,300,3,1))
# print(facelm_img_re.shape)
# '1' if i != '0' else '0' for i in y_train
#labels = np.array([ 1 if i != '0' else 0 for x in meta['data']['label']])
labels = np.array([int(x['label']) for x in meta['data']])
print(type(labels[0]))
# dataset= tf.data.Dataset.from_tensor_slices((facelm_img,headpose))
# dataset_label = tf.data.Dataset.from_tensor_slices(labels)

# dataset.element_spec
# dataset_label.element_spec

# dataset_merge = tf.data.Dataset.zip((dataset, dataset_label))
# dataset_merge.element_spec

# from sklearn.model_selection import train_test_split
# x_train, x_test, y_train, y_test = train_test_split(dataset, dataset_label, test_size=0.2, random_state=3)



input_1 = Input(shape=(300,300,3), name='face_pic')
x = Conv2D(32, (3, 3), activation='relu', name='cnn1')(input_1)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)
x = Dense(16, activation='relu')(x)
output_1 = Dense(8, activation='relu')(x)

# head율_pose 이 들어가는 FC 
input_2 = Input(shape=(3), name='head_pose')
x2 = Dense(32, activation='relu')(input_2)
#x = Dense(32, activation='relu')(x)
x2 = Dense(16, activation='relu')(x2)
output_2 = Dense(8)(x2)


input_3 = Input(shape=(100,100,3),name='eye_left')
x3 = Conv2D(32, (3, 3), activation='relu', name='cnn2')(input_3)
x3 = MaxPooling2D(pool_size=(2, 2))(x3)
x3 = Flatten()(x3)
x3 = Dense(16, activation='relu')(x3)
output_3 = Dense(8, activation='relu')(x3)

input_4 = Input(shape=(100,100,3),name='eye_right')
x4 = Conv2D(32, (3, 3), activation='relu', name='cnn3')(input_4)
x4 = MaxPooling2D(pool_size=(2, 2))(x4)
x4 = Flatten()(x4)
x4 = Dense(16, activation='relu')(x4)
output_4 = Dense(8, activation='relu')(x4)

# 여기서 합쳐집니다~
# feature를 늘릴 때, 별도의 네트워크를 구성하고 이 레이어에 합칠 것.
x5 = tf.keras.layers.concatenate([output_1, output_2,output_3,output_4])

x5 = Dense(32, activation='relu')(x5)
x5 = Dense(16, activation='relu')(x5)

main_output = Dense(1, activation='sigmoid', name='main_output')(x5)


model = Model(inputs= [input_1,input_2,input_3,input_4], outputs=main_output)
model.compile(optimizer=tf.keras.optimizers.Adam(), 
              loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

fit_history = model.fit([facelm_img,headpose,eyelm_left,eyelm_right],labels,epochs=5)










