# -*- coding: utf-8 -*-
# title           : data_utils.py
# description     : Preprocess input image and vector
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

import constants
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

class DataPreprocessing:
    """
    Preprocess input image and vector(headpose). 
    This class is used in 'data_generator.py' when we generate dataset.
    """
    def __init__(self):
        """
        `self.add_noise` is used in `transform_img` function to give random Gaussian color noise to image.
        """
        self.add_noise = tf.keras.Sequential([tf.keras.layers.GaussianNoise(0.08)])
        
    def normalize_headpose(self, dataframe):
        """
        Normalize(Standardization) headpose pitch, yaw, roll.
        ----------
        - Parameters
        
        dataframe: DataFrame
            dataframe with seven columns.
        ----------
        - Returns
        
        dataframe: DataFrame
            dataframe with seven columns which have three normalized headpose columns. 
        """
        pitch = [dataframe['vec_headpose'][i][0] for i in range(len(dataframe))]
        yaw = [dataframe['vec_headpose'][i][1] for i in range(len(dataframe))]
        roll = [dataframe['vec_headpose'][i][2] for i in range(len(dataframe))]

        mean_pitch, std_pitch = np.mean(pitch), np.std(pitch)
        mean_yaw, std_yaw = np.mean(yaw), np.std(yaw)
        mean_roll, std_roll = np.mean(roll), np.std(roll)
    
        for i in range(len(dataframe)):
            dataframe['vec_headpose'][i][0] = (dataframe['vec_headpose'][i][0] - mean_pitch) / std_pitch
            dataframe['vec_headpose'][i][1] = (dataframe['vec_headpose'][i][1] - mean_yaw) / std_yaw
            dataframe['vec_headpose'][i][2] = (dataframe['vec_headpose'][i][2] - mean_roll) / std_roll
    
        return dataframe

    def transform_img(self, img_face, img_eyeleft, img_eyeright, vec_headpose):
        """
        Transform train input image by random methods.
        We consider random brightness, contrast, hue, saturation, noise to make our image have more variance.
        ----------
        - Parameters
        
        img_face, img_eyeleft, img_eyeright: tensor
            image tensor with three dimensions.
        vec_headpose: tensor
            headpose tensor with one dimension.
        ----------
        - Returns
        
        img_face, img_eyeleft, img_eyeright: tensor
            image tensor with three dimensions.
        vec_headpose: tensor
            headpose tensor with one dimension.
        """
        # give same random transformation to image_set(face, eyeleft, eyeright) which is from one frame
        img_set = tf.image.random_brightness([img_face, img_eyeleft, img_eyeright], max_delta=0.15)
        img_set = tf.image.random_contrast(img_set, lower=0.7, upper=1.3)
        img_set = tf.image.random_hue(img_set, max_delta=0.05)
        img_set = tf.image.random_saturation(img_set, lower=0.7, upper=2.0)
        img_set = self.add_noise(img_set, training=True)
        img_face, img_eyeleft, img_eyeright = img_set[0], img_set[1], img_set[2]
        
        # resize and normalize image
        img_face = tf.image.resize(img_face, [constants.IMAGE_SIZE_FACE, constants.IMAGE_SIZE_FACE]) / 255.0
        img_eyeleft = tf.image.resize(img_eyeleft, [constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES]) / 255.0
        img_eyeright = tf.image.resize(img_eyeright, [constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES]) / 255.0
        
        return img_face, img_eyeleft, img_eyeright, vec_headpose

    def resize_and_normalize(self, img_face, img_eyeleft, img_eyeright, vec_headpose):
        """
        Resize and normalize(MinMax) validation input image.
        ----------
        - Parameters
        
        img_face, img_eyeleft, img_eyeright: tensor
            image tensor with three dimensions.
        vec_headpose: tensor
            headpose tensor with one dimension.
        ----------
        - Returns
        
        img_face, img_eyeleft, img_eyeright: tensor
            image tensor with three dimensions.
        vec_headpose: tensor
            headpose tensor with one dimension.
        """
        # resize and normalize image
        img_face = tf.image.resize(img_face, [constants.IMAGE_SIZE_FACE, constants.IMAGE_SIZE_FACE]) / 255.0
        img_eyeleft = tf.image.resize(img_eyeleft, [constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES]) / 255.0
        img_eyeright = tf.image.resize(img_eyeright, [constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES]) / 255.0
        
        return img_face, img_eyeleft, img_eyeright, vec_headpose

def plot_batch(self, zip_dataset, idx_batch, batch_size=16):
    batch = list(zip_dataset)[idx_batch][0]
    plt.figure(figsize=(6, 8))
    for frame in range(batch_size):
        for img_type in range(3):
            plt.subplot(batch_size / 2, 3 * 2, 3 * frame + img_type + 1)
            plt.imshow(batch[img_type][frame])
            plt.axis('off')
