import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Activation
import datetime

#%%


from get_image import get_img
get_img()

img = load_img(r'C:\Users\sodaus\Desktop\고려대학교 과정\샘플\reslut0\Figure_1.png')
x = img_to_array(img) 
x = x.reshape((1,) + x.shape) 

i = 0
for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='preview', save_prefix='test', save_format='jpeg'):
    i += 1
    print(i)
    if i > 20:
        break  
    
#%%
    
batch_size =1
target_size = (150,150)


train_datagen = ImageDataGenerator(
        rotation_range=0,
        width_shift_range=0.05,
        height_shift_range=0.05,
        rescale=1./255,
        shear_range=0.05,
        zoom_range=0.05,
        horizontal_flip=False,
        fill_mode='nearest')


train_generator = train_datagen.flow_from_directory(
        r'C:\Users\sodaus\Desktop\고려대학교 과정\작성한 코드\dataset\train',  
        target_size=target_size,  
        batch_size=batch_size,
        class_mode='binary') 
    
    
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        r'C:\Users\sodaus\Desktop\고려대학교 과정\작성한 코드\dataset\test',
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')
validation_generator = test_datagen.flow_from_directory(
        r'C:\Users\sodaus\Desktop\고려대학교 과정\작성한 코드\dataset\valid',
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary')



#%%


model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
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
model.add(Dropout(0.5))
model.add(Dense(2))
model.add(Activation('sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',# 혹은 adam?
              metrics=['accuracy'])





#%%
model.fit(
        train_generator,
        steps_per_epoch=1000,
        epochs=50,
        validation_data=validation_generator,
        validation_steps=800)

model.save_weights('model {}.h5'.format(datetime.datetime.now().strftime("%y%m%d_%H%M%S")))
#%%






    
#%%
    

    
    