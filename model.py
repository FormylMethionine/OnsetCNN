import numpy as np
import os
import json
import pickle as pkl
import tensorflow as tf
from tensorflow.keras import layers


class OnsetModel(tf.Module):

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.layers = [layers.Conv2D(10, (7, 3), activation='relu',
                                     input_shape=(15, 80, 3),
                                     data_format='channels_last'),
                       layers.MaxPool2D(pool_size=(1, 3), strides=3),
                       layers.Conv2D(20, (3, 3), activation='relu',
                                     data_format='channels_last'),
                       layers.MaxPool2D(pool_size=(1, 3), strides=3),
                       layers.Flatten(),
                       layers.Dense(256, activation='relu'),
                       layers.Dense(128, activation='relu'),
                       layers.Dense(1),
                       layers.ReLU(max_value=1.0)]

    def convert(self, song):
        ret = []
        for i in range(15, len(song) - 15):
            ret.append(song[i-15:i+15])
        ret = np.array(ret)
        return tf.constant(ret)

    def __call__(self, inputs):
        inputs = self.convert(inputs)
        for layer in self.layers:
            inputs = layer(inputs)
        return inputs

    def train(self, x, y, lr=1):
        y = tf.constant(y)
        with tf.GradientTape() as t:
            current_loss = loss(y, model(x))
        grad = t.gradient(current_loss, self.trainable_variables)
        for dvar, var in zip(grad, self.trainable_variables):
            var.assign_sub(lr * dvar)
        return current_loss

    def fit(self, x, y, epochs, lr=1):
        loss = []
        for epoch in range(epochs):
            current_loss = self.train(x, y, lr)
            loss.append(current_loss)
            print(f"epoch: {epoch}\tloss: {current_loss}")
        return loss


def loss(target_y, pred_y):
    return tf.reduce_mean(tf.square(target_y - pred_y))


if __name__ == "__main__":

    name = "Anti the Holic"
    audio = pkl.load(open(f"./dataset_ddr/{name}.pkl", "rb"))
    chart = json.load(open(f"./dataset_ddr/{name}.chart", "r"))
    metadata = json.load(open(f"./dataset_ddr/{name}.metadata", "r"))

    model = OnsetModel()
    inputs = tf.constant(audio)
    print(model(inputs))
    loss = model.fit(audio, chart, 10)
    #for i in loss:
        #print(i)
