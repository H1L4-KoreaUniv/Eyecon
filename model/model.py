# -*- coding: utf-8 -*-
# title           : model.py
# description     : Define model structure.
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout, Flatten, LocallyConnected2D
import constants
import matplotlib.pyplot as plt

class ControlModel:
    def layer_concat(self, inputs, name):
        output = tf.keras.layers.concatenate(inputs, name=name)            
        return output

class ImageNetModel:
    def __init__(self):
        pass
    
    def use_VGG16(self):
        """
        Define VGG16 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Returns
        
        x: Functional
            VGG16 model.
        """
        from tensorflow.keras.applications import VGG16
        base_model = VGG16(input_shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                           include_top=False,
                           weights='imagenet',
                           pooling='avg')
        for layer in base_model.layers:
            layer.trainable = False
        return base_model
    
    def use_ResNet50(self):
        """
        Define ResNet50 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Returns
        
        x: Functional
            ResNet50 model.
        """
        from tensorflow.keras.applications import ResNet50
        base_model = ResNet50(input_shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                              include_top=False,
                              weights='imagenet',
                              pooling='avg')
        for layer in base_model.layers:
            layer.trainable = False
        return base_model

    def use_MobileNetV2(self):
        """
        Define MobileNetV2 model. Load and freeze pre-trained weights.
        Change model's name and layers' name.
        ----------
        - Returns
        
        base_model: Functional
            MobileNetV2 model.
        """
        from tensorflow.keras.applications import MobileNetV2
        base_model = MobileNetV2(input_shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3),
                                 include_top=False,
                                 weights='imagenet',
                                 pooling='avg')
        for layer in base_model.layers:
            layer.trainable = False
        return base_model

class FaceModel:
    """
    Define and get face model.
    """
    def __init__(self):
        self.input_face = Input(shape=(constants.IMAGE_SIZE_FACE, constants.IMAGE_SIZE_FACE, 3))

    def use_deepface(self):
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
        layer_ = self.use_deepface()
        layer_.load_weights(constants.PATH_WEIGHTS_DeepFace)
        for layer in layer_.layers:
            layer.trainable = False
        self.input_face = layer_.input
        
        output = self.get_fc_layer(layer_.layers[-4].output)

        return output

class EyeModel:
    def __init__(self):
        self.input_eyeleft = Input(shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3))
        self.input_eyeright = Input(shape=(constants.IMAGE_SIZE_EYES, constants.IMAGE_SIZE_EYES, 3))

    def get_fc_layer(self, layer):
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
        eyes = Dense(64, activation='relu', name='eyes_fc_1')(layer)
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
            layer = ImageNetModel().use_ResNet50()
            eyeleft = layer(self.input_eyeleft)
            eyeright = layer(self.input_eyeright)
            eyes = ControlModel().layer_concat([eyeleft, eyeright], name='eyes_Concat')
            
        elif model_name == 'ResNet50':
            layer = ImageNetModel().use_ResNet50()
            eyeleft = layer(self.input_eyeleft)
            eyeright = layer(self.input_eyeright)
            eyes = ControlModel().layer_concat([eyeleft, eyeright], name='eyes_Concat')
        
        elif model_name =='MobileNetV2':
            layer = ImageNetModel().use_MobileNetV2()
            eyeleft = layer(self.input_eyeleft)
            eyeright = layer(self.input_eyeright)
            eyes = ControlModel().layer_concat([eyeleft, eyeright], name='eyes_Concat')
        
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
    def get_fc_layer(self, layer):
        main = Dense(128, activation='relu', name='main_Fc_1')(layer)
        output_main = Dense(1, activation='sigmoid', name='main_Fc_2')(main)
        return output_main

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
    cm = ControlModel()
    mf = MainFCLayer()
    face_output = fm.get_model()
    eye_output = em.get_model(model_name=constants.MODEL_EYES)
    headpose_input = Input(shape=(3), name='headpose_Input')
    input_main = [fm.input_face, em.input_eyeleft, em.input_eyeright, headpose_input]
    output = cm.layer_concat([face_output, eye_output, headpose_input], name='main_Concat')
    output_main = mf.get_fc_layer(output)
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
