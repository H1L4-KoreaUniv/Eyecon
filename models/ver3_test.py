
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
# from PIL import Image

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

datagen = ImageDataGenerator(
    validation_split=0.2,
    rescale=1./255,
    #data_format='channels_first'
)

data_dir = r'/Users/sodaus/Desktop/data/ver3/tmp'
train_generator = datagen.flow_from_directory(
    directory=data_dir,
    subset='training',
    target_size=(300, 300),
    batch_size=32,
    shuffle=True,
    class_mode='binary',
    seed=112
)

valid_generator = datagen.flow_from_directory(
    directory=data_dir,
    subset='validation',
    target_size=(300, 300),
    batch_size=32,
    shuffle=True,
    class_mode='binary',
    seed=112
)

input_1 = Input(shape=(300,300,3), name='face_pic')
x = Conv2D(32, (3, 3), activation='relu', name='cnn1')(input_1)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)
x = Dense(16, activation='relu')(x)
output_1 = Dense(8, activation='relu')(x)

main_output = Dense(1, activation='sigmoid', name='main_output')(output_1)


model = Model(inputs=input_1, outputs=main_output)
model.compile(optimizer=tf.keras.optimizers.Adam(), 
              loss='binary_crossentropy', metrics=['accuracy'])

with tf.device('/device:GPU:0'):
    fit_history = model.fit(
        train_generator,
        steps_per_epoch=len(train_generator),
        epochs=5,
        validation_data=valid_generator,
        validation_steps=len(valid_generator)
        # callbacks=[cb_early_stopper]
    )

