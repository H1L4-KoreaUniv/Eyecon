# pip install tensorflow-gpu==1.14.0 --user
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
from keras.models import Sequential
# from sklearn.model_selection import cross_val_score, train_test_split
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import plot_model
import matplotlib.pyplot as plt
import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# from numba import cuda

# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())
# tf.debugging.set_log_device_placement(True)


# tf.config.experimental.list_physical_devices('GPU')

src = r'C:\Users\sodaus\Desktop\TF'
os.chdir(src)

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True

#%%
import os, shutil
import random
labels = ['0', '1']

src = os.getcwd()
list1 = os.listdir(src+'\data')

for label in labels:
    os.makedirs(r'{}\input\train\{}' .format(src, label))
    os.makedirs(r'{}\input\test\{}' .format(src, label))
    os.makedirs(r'{}\input\valid\{}' .format(src, label))


for name in list1:
    for file in os.listdir(src+'\data\{}' .format(name)):
        if file[0] == '0':
            shutil.move(
                r'{}\data\{}\{}' .format(src, name,file),
                r'{}\input\train\{}\{}' .format(src, '0',file)
                )
            print(file+ ' .')
        elif file[0] != '0':
           shutil.move(
               r'{}\data\{}\{}' .format(src, name,file),
               r'{}\input\train\{}\{}' .format(src, '1',file)
               )
           print(file+ ' .')
       
        


frames = [str(_) for _ in range(1,61)]
sample_frame = random.sample(frames, 12)

# train / test 셋 나누기 (임의 프레임)
for label in labels:
    for file in os.listdir( r'{}\input\\train\\{}' .format(src, label)):
        if file.split('_')[-1].split('.')[0][5:] in sample_frame[:10]:    
            shutil.move(
                r'{}\input\\train\\{}\\{}' .format(src, label,file),
                r'{}\input\\test\\{}\\{}' .format(src, label,file)
                )
        elif file.split('_')[-1].split('.')[0][5:] in sample_frame[10:]:    
            shutil.move(
                r'{}\input\\train\\{}\\{}' .format(src, label,file),
                r'{}\input\\valid\\{}\\{}' .format(src, label,file)
                )
         


for label in labels:
    print('train {} : {}' .format( label, len(os.listdir( r'{}\input\train\{}' .format(src,label) ) ) ) )
    print('test {} : {}' .format( label, len(os.listdir( r'{}\input\test\{}' .format(src,label) ) ) ) )
    print('valid {} : {}' .format( label, len(os.listdir( r'{}\input\valid\{}' .format(src,label) ) ) ) )


#%%


target_size = (400,300)

train = ImageDataGenerator(
        rotation_range=0,
        width_shift_range=0.05,
        height_shift_range=0.05,
        rescale=1./255,
        shear_range=0.05,
        zoom_range=0.05,
        horizontal_flip=False,
        fill_mode='nearest')

train_data = train.flow_from_directory(
    directory= src+ "/input/train",
    target_size=target_size,
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=None
    )

test = ImageDataGenerator(rescale=1./255)

test_data = test.flow_from_directory(
    directory= src + "/input/test",
    target_size=target_size,
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=None)

valid_data = test.flow_from_directory(
    directory= src + "/input/valid",
    target_size=target_size,
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=None)


# real_data = test.flow_from_directory(
#     directory= src + "/input/real",
#     target_size=target_size,
#     class_mode='categorical',
#     batch_size=32,
#     shuffle=True,
#     seed=None)


train_data.image_shape
train_data.filenames
#%%
# with tf.device('/GPU:0'):
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
model.add(Dense(2))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

    

plot_model(model)
    

#%%

#%%


checkpoint = ModelCheckpoint("tf_model1({}).h5" .format(str(target_size)), monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')

# sess = tf.Session()
# sess.run(tf.initialize_all_variables() )

model.fit(train_data, epochs=100)


len(train_data.filenames)
train_data.classes


# with tf.device('/GPU:0'):
    hist = model.fit_generator(
        steps_per_epoch=250,
        generator=train_data,
        validation_data= test_data,
        validation_steps=10,
        epochs=40,
        callbacks=[checkpoint,early])


cuda.close()
#%%
model.predict(valid_data)    
model.evaluate(valid_data)    
 



cuda.close()
#%%

plt.plot(hist.history["acc"])
plt.plot(hist.history['val_acc'])
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss \n"])
plt.show()
plt.savefig('ahmoo_model({}).png" .format(str(target_size))', dpi=500)