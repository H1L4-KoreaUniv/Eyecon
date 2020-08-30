# -*- coding: utf-8 -*-
# title           : data_generator.py
# description     : Generate dataset
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

from sklearn.model_selection import train_test_split
import cv2
import tensorflow as tf
from data_utils import DataPreprocessing
import constants

class DataGenerator:
    """
    Generate dataset. 
    """
    def __init__(self, path_img):
        """
        - Parameters
        
        path_img: str
            path that contains whole image(face, eyeleft, eyeright)
        """
        self.path_img = path_img

    def split_df(self, dataframe):
        """
        Split dataframe into train and validation
        ----------
        - Parameters
        
        dataframe: DataFrame
            dataframe with seven columns.
        ----------
        - Returns
        
        dataframe_train: DataFrame
            train dataframe.
        dataframe_valid: DataFrame
            valid dataframe.
        """
        dataframe_train, dataframe_valid = train_test_split(dataframe, test_size=constants.VALID_PROP)
        dataframe_train.reset_index(drop=True, inplace=True)
        dataframe_valid.reset_index(drop=True, inplace=True)
        
        return dataframe_train, dataframe_valid

    # load image and yield data
    def gen(self, dataframe, is_y=False):
        """
        Generate image array from image's path and generate headpose and label from dataframe.
        ----------
        - Parameters
        
        dataframe: DataFrame
            dataframe with seven columns.
        is_y: bool
            determine which yield X(three image, headpose) or y(label)
        """
        if bool(is_y) == False:
            for i in range(len(dataframe)):
                img_face = cv2.cvtColor(cv2.imread(self.path_img + dataframe['img_face'][i]), 
                                        cv2.COLOR_BGR2RGB)
                img_eyeleft = cv2.cvtColor(cv2.imread(self.path_img + dataframe['img_eyeleft'][i]), 
                                           cv2.COLOR_BGR2RGB)
                img_eyeright = cv2.cvtColor(cv2.imread(self.path_img + dataframe['img_eyeright'][i]), 
                                            cv2.COLOR_BGR2RGB)
                vec_headpose = dataframe['vec_headpose'][i]
                
                yield (img_face, img_eyeleft, img_eyeright, vec_headpose)
        else:
            for i in range(len(dataframe)):
                label = dataframe['label'][i]
                
                yield (label)

    def make_dataset(self, dataframe, is_y=False,
                     output_types=constants.INPUT_TYPE,
                     output_shapes=constants.INPUT_TENSOR_SHAPE):
        """
        Make X or y dataset that has tensor by `gen` function.
        ----------
        - Parameters
        
        dataframe: DataFrame
            dataframe with seven columns.
        is_y: bool
            determine which return X dataset or y dataset
        output_types: tuple
            tensor types
        output_shapes: tuple
            tensor shapes
        ----------
        - Returns
        
        dataset: FlatMapDataset
            X or y dataset.
        """
        dataset = tf.data.Dataset.from_generator(
            lambda : self.gen(dataframe, is_y),
            output_types,
            output_shapes
            )
        
        return dataset

    def make_prefecth_dataset(self, dataset, preprocessing):
        """
        We use prefetch dataset to reduce training time. 
        Prefetching overlaps the preprocessing and model execution of a 
        training step. While the model is executing training step s, the input 
        pipeline is reading the data for step s+1. Doing so reduces the step 
        time to the maximum (as opposed to the sum) of the training and the time
        it takes to extract the data.
        ----------
        - Parameters
        
        dataset: dataset
            X or y dataset.
        preprocessing: function
            preprocessing function.
        ----------
        - Returns
        
        dataset: PrefetchDataset
            prefetch dataset that reduce training time. 
            This dataset have preprocessed input.
        """
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        prefetch_dataset = (tf.data.Dataset.zip((dataset[0].cache().map(preprocessing, num_parallel_calls=AUTOTUNE), 
                                                 dataset[1]))
                            .batch(constants.BATCH_SIZE)
                            .prefetch(AUTOTUNE)
                            )
        
        return prefetch_dataset

def data_generator(path_img, dataframe):
    """
    Generate train and valid prefetch dataset 
    ----------
    - Parameters
    
    path_img: str
        path that contains whole image(face, eyeleft, eyeright)
    dataframe: DataFrame
        train or validation dataframe
    ----------
    - Returns

    train_dataset: PrefetchDataset
        train dataset
    valid_dataset: PrefetchDataset
        valid dataset
    """
    dg = DataGenerator(path_img)
    dp = DataPreprocessing()
    
    dataframe = dp.normalize_headpose(dataframe)
    
     # split dataframe into train and valid
    df_train, df_valid = dg.split_df(dataframe)
    
    # flatten dataset
    x_train_dataset = dg.make_dataset(df_train)
    y_train_dataset = dg.make_dataset(df_train, is_y=True, output_types=constants.LABEL_TYPE, output_shapes=constants.LABEL_TENSOR_SHAPE)
    x_valid_dataset = dg.make_dataset(df_valid)
    y_valid_dataset = dg.make_dataset(df_valid, is_y=True, output_types=constants.LABEL_TYPE, output_shapes=constants.LABEL_TENSOR_SHAPE)
    
    # prefetch dataset
    train_dataset = dg.make_prefecth_dataset([x_train_dataset, y_train_dataset], dp.transform_img)
    valid_dataset = dg.make_prefecth_dataset([x_valid_dataset, y_valid_dataset], dp.resize_and_normalize)
    
    return train_dataset, valid_dataset
