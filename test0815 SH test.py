# pip install tensorflow-gpu==1.14.0
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
tf.debugging.set_log_device_placement(True)
tf.config.experimental.list_physical_devices('GPU')
print(tf.keras.__version__)
print(device_lib.list_local_devices())




#%%


# json 파일 불러오기
with open('metadata_merge.json') as json_file:
    meta = json.load(json_file)
with open('metadataLSH.json') as json_file:
    test_meta = json.load(json_file)

# 섞기
random.shuffle(meta['data'])
random.shuffle(test_meta['data'])


[x['eyelmname'][0] for x in meta['data']]


# json 에서 data 불러오기 (x 데이터)
x_data = [[list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\facelm_img', x['facelmname']))),
           list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\eye_left', x['eyelmname'][0]))),
            list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\eye_right', x['eyelmname'][1]))),
           np.array(list(x['head_pose'].values()))]
          for x in meta['data']]
    
x_test_data = [[list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\facelm_img', x['facelmname']))),
                list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\eye_left', x['eyelmname'][0]))),
                list(cv2.imread(os.path.join(r'C:\Users\sodaus\Downloads\Eyecon-master\make_metadata\img_ver1\eye_right', x['eyelmname'][1]))),
           np.array(list(x['head_pose'].values()))]
          for x in test_meta['data']]
                 
# 'labe' 로 y_data 만들기
y_train = np.array([x['label'] for x in meta['data']])
y_test = np.array([x['label'] for x in test_meta['data']])

# label 0, 1로 바꾸기
y_train = np.array([ '1' if i != '0' else '0' for i in y_train])
y_test = np.array([ '1' if i != '0' else '0' for i in y_test])

# 나누기 코드. json 하나만 불러서 split 할 때 사용  
# from sklearn.model_selection import train_test_split
# x_train, x_test, y_train, y_test = train_test_split(x_data, labels, test_size=0.2, random_state=3)

# train, test set의 라벨 비
print(list(y_train).count('0')/list(y_train).count('1'))
print(list(y_test).count('0')/list(y_test).count('1'))

# 최종: input data 만들기(array)
face_pic_train = np.array([_[0] for _ in x_data])
face_pic_test = np.array([_[0] for _ in x_test_data])

eye_pic_left_train = np.array([_[1] for _ in x_data])
eye_pic_left_test = np.array([_[1] for _ in x_test_data])

eye_pic_right_train = np.array([_[2] for _ in x_data])
eye_pic_right_test = np.array([_[2] for _ in x_test_data])

head_pose_train = np.array([_[3] for _ in x_data])
head_pose_test = np.array([_[3] for _ in x_test_data])


#%%

# face_pic 용 CNN 네트워크
input_1 = Input(shape=(300,300,3), name='face_pic')
x = Conv2D(32, (3, 3), activation='relu', name='cnn1')(input_1)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)
x = Dense(16, activation='relu')(x)
output_1 = Dense(8, activation='relu')(x)


# head율_pose 이 들어가는 FC 
input_2 = Input(shape=(3), name='head_pose')
x = Dense(32, activation='relu')(input_2)
#x = Dense(32, activation='relu')(x)
x = Dense(16, activation='relu')(x)
output_2 = Dense(8)(x)

# 여기서 합쳐집니다~
# feature를 늘릴 때, 별도의 네트워크를 구성하고 이 레이어에 합칠 것.
x = tf.keras.layers.concatenate([output_1, output_2])

x = Dense(32, activation='relu')(x)
x = Dense(16, activation='relu')(x)
# 최종 output. 라벨에 따라 shape을 바꾸세요
main_output = Dense(1, activation='softmax', name='main_output')(x)


# model은 face_pic, head_pose를 입력받고, main_output 을 출력합니다.
model = Model(inputs=[input_1, input_2], outputs=[main_output])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#%%

model.summary()
# 모델 구조도
plot_model(model)

#%%
# =============================================================================
# 학 습
# =============================================================================
hist = model.fit(
    [face_pic_train, head_pose_train], [y_train],
    validation_data = [[face_pic_test, head_pose_test], y_test],
    epochs=6)


#성능평가
model.evaluate([face_pic_test, head_pose_test],[y_test])


# history plot
import matplotlib.pyplot as plt
plt.plot(hist.history["acc"])
plt.plot(hist.history['val_acc'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy \n"])
plt.show()

plt.plot(hist.history["loss"])
plt.plot(hist.history['val_loss'])
plot_model(model, 'model_test_01.png')
