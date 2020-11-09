import numpy as np
import os
import json
import pickle as pkl
import tensorflow as tf
from tensorflow.keras import layers

class OnsetModel(tf.keras.Model):

    def __init__(self, name=None, **kwargs):
        super.__init__(**kwargs)
        self.layers = [layers.Conv2D(10, (7, 3), activation='relu',
                                     input_shape=(15, 80, 3)),
                       layers.MaxPooling1D(pool_size=3, strides=3),
                       layers.Conv2D(20, (3, 3), activation='relu'),
                       layers.MaxPooling1D(pool_size=3, strides=3),
                       layers.Dense(256, activation='relu'),
                       layers.Dense(128, activation='relu'),
                       layers.Dense(2)]

    def call(self, inputs):
        for layer in self.layers:
            inputs = layer(inputs)
        return inputs
