# -*- coding: utf-8 -*-
# title           : main.py
# description     : Fit the model.
# date            : 20200830
# python_version  : 3.8.3
# ==============================================================================

from json_to_df import make_df
import constants
from data_generator import data_generator
from model import multimodal_multistream_model, plot_model
import tensorflow as tf
from tensorflow.keras.models import Model

def main():

    df = make_df(constants.PATH_JSON)
    train_ds, valid_ds = data_generator(constants.PATH_IMG, df)
    input_main, output_main = multimodal_multistream_model()

    model = Model(inputs=input_main, outputs=output_main)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=constants.LEARNING_RATE),
                  loss=tf.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])
    model.summary()

    checkpoint_path = constants.PATH_MODEL_SAVE
    cb_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                       monitor='val_loss',
                                                       save_weights_only=False,
                                                       save_best_only=True,
                                                       verbose=2)
    cb_earlystopper = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                       patience=10)
    with tf.device('/device:GPU:0'):
        fit_history = model.fit(
            train_ds,
            epochs=100,
            validation_data=valid_ds,
            callbacks=[cb_earlystopper, cb_checkpoint]
        )
        
    plot_model(fit_history)
    
    # model.save(constants.PATH_MODEL_SAVE)

if __name__ == '__main__':
   main()
    
   
