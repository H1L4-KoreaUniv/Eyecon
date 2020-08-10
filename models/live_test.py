#!/usr/bin/env python
# coding: utf-8

# In[10]:


import cv2
import numpy as np
import tensorflow as tf

cap = cv2.VideoCapture(0)
# if cap.isOpen():
#     print('width: {}, height : {}'.format(cap.get(3), cap.get(4))

model = tf.keras.models.load_model('C:/Users/JIWON/Downloads/ahmoo_model1.h5')
          
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame',frame)
        img = frame.copy()
        if(int(cap.get(1)) % 30 == 0):
#             print(img.shape)
            resize_img = cv2.resize(img, (400,300))/255.0
#             print(resize_img.shape)
            classes = model.predict(resize_img.reshape(1, 400, 300, 3))
            print(np.argmax(classes))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print('error')
cap.release()
cv2.destroyAllWindows()

