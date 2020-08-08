# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 21:14:49 2020

@author: sodaus
"""
import os
import keras
import tensorflow as tf
from keras.models import Sequential
from sklearn.model_selection import cross_val_score, train_test_split
from keras.layers import Dense, Conv2D, MaxPool2D , Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import matplotlib.pyplot as plt
import datetime
#%%


# X_train, X_test, Y_train, Y_test = train_test_split(data, 0.2, random_state=0)
#%%

target_size = (300,300)

train = ImageDataGenerator(
        rotation_range=0,
        width_shift_range=0.05,
        height_shift_range=0.05,
        rescale=1./255,
        shear_range=0.05,
        zoom_range=0.05,
        horizontal_flip=False,
        fill_mode='nearest')

train_data = train.flow_from_directory(directory="/data",target_size=target_size)

test = ImageDataGenerator(rescale=1./255)

test_data = test.flow_from_directory(directory="/test", target_size=target_size)

#%%

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape= target_size+ (3,)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(5))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
    )

#%%
model.summary()
#%%

checkpoint = ModelCheckpoint("ahmoo_model.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')


hist = model.fit_generator(
    steps_per_epoch=10,
    generator=train_data,
    validation_data= test_data,
    validation_steps=10,
    epochs=100,
    callbacks=[checkpoint,early])


#%%

plt.plot(hist.history["acc"])
plt.plot(hist.history['val_acc'])
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()