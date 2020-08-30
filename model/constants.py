# -*- coding: utf-8 -*-
# title           : constants.py
# description     : Assign parameters to train. Change some parameters if you need.
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

import tensorflow as tf

# ==============================================================================
PATH_JSON = 'C:/Users/sodaus/Desktop/data_final/data_final.json'
PATH_IMG = 'C:/Users/sodaus/Desktop/data_final/img/'
PATH_WEIGHTS_DeepFace = 'C:/Users/sodaus/Desktop/1stmodel/VGGFace2_DeepFace_weights_val-0.9034.h5'
# ==============================================================================
VALID_PROP = 0.3
# ==============================================================================
MODEL_EYES = 'MobileNetV2'  # VGG16, ResNet50, MobileNetV20
# ==============================================================================
IMAGE_SIZE_FACE = 152
IMAGE_SIZE_EYES = 224
# ==============================================================================
BATCH_SIZE = 32
LEARNING_RATE = 0.0001
# ==============================================================================
INPUT_TENSOR_SHAPE = (tf.TensorShape([224, 224, 3]), tf.TensorShape([224, 224, 3]), tf.TensorShape([224, 224, 3]), tf.TensorShape([3]))
INPUT_TYPE = (tf.float32, tf.float32, tf.float32, tf.float32)
LABEL_TENSOR_SHAPE = (tf.TensorShape([]))
LABEL_TYPE = (tf.int32)
# ==============================================================================