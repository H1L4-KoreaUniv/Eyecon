# -*- coding: utf-8 -*-
# title           : model.py
# description     : Define model structure.
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, LocallyConnected2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt
import constants


class FaceModel:
    """
    Define and get face model.
    """
    def __init__(self):
        self.input_face = Input(shape=(constants.IMAGE_SIZE_FACE, constants.IMAGE_SIZE_FACE, 3),
                                name='face_Input')

    def use_DeepFace(self):
        """
        Define DeepFace model.
        ----------
        - Returns
        
        face: Functional
            DeepFace model structure.
        """
        Input_1 = Input(shape=(152, 152, 3), name='face_Input')
        Conv_1 = Conv2D(32, (11, 11), activation='relu', name='face_Conv_1')(Input_1)
        MaxPool_1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same', name='face_MaxPool_1')(Conv_1)
        Conv_2 = Conv2D(16, (9, 9), activation='relu', name='face_Conv_2')(MaxPool_1)
        LC_1 = LocallyConnected2D(16, (9, 9), activation='relu', name='face_LC_1')(Conv_2)
        LC_2 = LocallyConnected2D(16, (7, 7), strides=(2, 2), activation='relu', name='face_LC_2')(LC_1)
        LC_3 = LocallyConnected2D(16, (5, 5), activation='relu', name='face_LC_3')(LC_2)  # output 21, 21, 16
        Flatten_1 = Flatten(name='face_Flatten')(LC_3)  # output 7056
        FC_1 = Dense(4096, activation='relu')(Flatten_1)
        Drop_1 = Dropout(0.5)(FC_1)
        FC_2 = Dense(8631, activation='softmax')(Drop_1)
        face = Model(inputs=Input_1, outputs=FC_2)
        return face

    def get_fc_layer(self, layer):
        """
        Add fully-connected layers.
        ----------
        - Parameters
        
        layer: Tensor
            Flatten layer's output
        ----------
        - Returns
        
        face: Tensor
            Dense layer's output
        """
        face = Dense(128, activation='relu', name='face_fc_1')(layer)
        face = Dense(64, activation='relu', name='face_fc_2')(face)
        
        return face

    def get_model(self):
        """
        Load and freeze pre-trained weights. Get complete face CNN.
        ----------
        - Returns
        
        output: Tenseor
            Dense layer's output
        """
        layer_ = self.use_DeepFace()
        layer_.load_weights(constants.PATH_WEIGHTS_DeepFace)
        for layer in layer_.layers:
            layer.trainable = False
        self.input_face = layer_.input
        output = self.get_fc_layer(layer_.layers[-4].output)
        
        return output

class EyeModel:
    def __init__(self):
        self.input_eyeleft = Input(shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                                   name='eyeleft_Input')
        self.input_eyeright = Input(shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                                    name='eyeright_Input')
    
    def use_VGG16(self, name):
        """
        Define VGG16 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Parameters
        name: str
            'left' or 'right'
        ----------
        - Returns
        
        x: Functional
            VGG16 model.
        """
        from tensorflow.keras.applications import VGG16
        x = VGG16(include_top=False,
                  weights='imagenet',
                  pooling='avg')
        
        for layer in x.layers:
            layer.trainable = False
            
        x._name = x._name + '_' + name
        for layer in x.layers:
            layer._name = layer._name + '_' + name
            
        return x
    
    def use_ResNet50(self, name):
        """
        Define ResNet50 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Parameters
        name: str
            'left' or 'right'
        ----------
        - Returns
        
        x: Functional
            ResNet50 model.
        """
        from tensorflow.keras.applications import ResNet50
        x = ResNet50(input_shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                     include_top=False,
                     weights='imagenet',
                     pooling='avg')
        
        # freeze all layers of base_model
        for layer in x.layers:
            layer.trainable = False
        
        # change model's name and layers' name
        x._name = x._name + '_' + name
        for layer in x.layers:
            layer._name = layer._name + '_' + name
            
        return x
    
    def use_MobileNetV2(self, name):
        """
        Define MobileNetV2 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Parameters
        name: str
            'left' or 'right'
        ----------
        - Returns
        
        x: Functional
            MobileNetV2 model.
        """
        from tensorflow.keras.applications import MobileNetV2
        x = MobileNetV2(input_shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                        include_top=False,
                        weights='imagenet',
                        pooling='avg')
        
        # freeze all layers of base_model
        for layer in x.layers:
            layer.trainable = False
            
        # change model's name and layers' name
        x._name = x._name + '_' + name
        for layer in x.layers:
            layer._name = layer._name + '_' + name
            
        return x

    def get_fc_layer(self, x):
        """
        Add fully-connected layers.
        ----------
        - Parameters
        
        layer: Tensor
            Concatenate layer's output
        ----------
        - Returns
        
        eyes: Tensor
            Dense layer's output
        """
        eyes = Dense(64, activation='relu', name='eyes_fc_1')(x)
        
        return eyes

    def get_model(self, model_name):
        """
        Get complete eyes CNN.
        ----------
        - Parameters
        
        model_name: str
            'VGG16', 'ResNet50' or 'MobileNetV2'
        ----------
        - Returns
        
        output: Tenseor
            Dense layer's output
        """
        if model_name == 'VGG16':
            share_use_VGG16 = self.use_VGG16(name='eyes')
            eyeleft = share_use_VGG16(self.input_eyeleft)
            eyeright = share_use_VGG16(self.input_eyeright)
            eyes = tf.keras.layers.concatenate([eyeleft, eyeright], name='eyes_Concat')
        elif model_name == 'ResNet50':
            share_use_ResNet50 = self.use_ResNet50(name='eyes')
            eyeleft = share_use_ResNet50(self.input_eyeleft)
            eyeright = share_use_ResNet50(self.input_eyeright)
            eyes = tf.keras.layers.concatenate([eyeleft, eyeright], name='eyes_Concat')
        elif model_name == 'MobileNetV2':
            share_use_MobileNetV2 = self.use_MobileNetV2(name='eyes')
            eyeleft = share_use_MobileNetV2(self.input_eyeleft)
            eyeright = share_use_MobileNetV2(self.input_eyeright)
            eyes = tf.keras.layers.concatenate([eyeleft, eyeright], name='eyes_Concat')
                
        output = self.get_fc_layer(eyes)

        return output

class MainFCLayer:
    """
    Add fully-connected layers.
    ----------
    - Parameters
    
    layer: Tensor
        Concatenate(face, eyes, headpose) layer's output
    ----------
    - Returns
    
    x: Tensor
        Dense layer's output
    """
    def get_fc_layer(self, x):
        x = Dense(128, activation='relu', name='main_Fc_1')(x)  # same with [Krafka]
        x = Dense(1, activation='sigmoid', name='main_Fc_2')(x)  # same with [Krafka]
        
        return x

def multimodal_multistream_model():
    """
    Get multimodal multistream model.
    ----------
    - Returns
    
    input_main: list
        face, eyeleft, eyeright, headpose inputs
    output_main = Tensor
        Dense layer's output
    """
    fm = FaceModel()
    em = EyeModel()
    mf = MainFCLayer()
    
    output_face = fm.get_model()
    output_eyes = em.get_model(model_name=constants.MODEL_EYES)
    input_headpose = Input(shape=(3), name='headpose_Input')
    input_main = [fm.input_face, em.input_eyeleft, em.input_eyeright, input_headpose]
    
    x = tf.keras.layers.concatenate([output_face, output_eyes, input_headpose], name='main_Concat')
    output_main = mf.get_fc_layer(x)
    
    return input_main, output_main

def plot_model(fit_history):
    """
    Plot learning curve.
    
    """
    plt.subplot(2, 1, 1)
    plt.plot(fit_history.history["accuracy"])
    plt.plot(fit_history.history['val_accuracy'])
    plt.title("Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend(["Accuracy", "Val Accuracy"])
    
    plt.subplot(2, 1, 2)
    plt.plot(fit_history.history["loss"])
    plt.plot(fit_history.history["val_loss"])
    plt.title("Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Binary CrossEntropy")
    plt.legend(["Loss", "Val Loss"])
    plt.show()
