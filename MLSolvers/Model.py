import csv
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Model:

    def __init__(self):
        print(tf.__version__)
        train_data = self.import_data('data.csv')
        train_labels = self.import_data('labels.csv')

        train_labels = self.reformat_labels(train_data, train_labels)
        train_data = train_data

        print(train_data.shape)
        print(train_labels.shape)

        model = keras.Sequential([
            # keras.layers.GaussianDropout(0.4), #,  input_shape=(16,)),
            keras.layers.Dense(256, activation=tf.nn.relu, input_shape=(16,)),
            # input_shape=(len(train_labels), 16, )),
            keras.layers.Dense(256, activation=tf.nn.relu),  # use_bias=True,),
            keras.layers.Dense(256, activation=tf.nn.relu),
            keras.layers.Dense(256, activation=tf.nn.relu),
            keras.layers.Dense(256, activation=tf.nn.relu),
            keras.layers.Dense(256, activation=tf.nn.relu),
            keras.layers.GaussianDropout(0.2),
            keras.layers.Dense(16, activation=tf.nn.softmax)
        ])

        model.compile(optimizer=tf.train.AdamOptimizer(),  # GradientDescent
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # x_val = train_data[:8000]
        # partial_x_train = train_data[8000:]
        #
        # y_val = train_labels[:8000]
        # partial_y_train = train_labels[8000:]
        #
        # model.fit(partial_x_train,
        #           partial_y_train,
        #           epochs=20,
        #           batch_size=128,
        #           validation_data=(x_val, y_val),
        #           shuffle=True)
        #
        model.fit(train_data,
                  train_labels,
                  epochs=20,
                  batch_size=128,
                  shuffle=True)

        # model.fit(partial_x_train,
        #           partial_y_train,
        #           epochs=20,
        #           batch_size=128,
        #           shuffle=True)
        #
        # model.evaluate(x_val, y_val)
        model.summary()

    @staticmethod
    def import_data(filename):
        with open(filename, 'r') as file:
            data_iterator = csv.reader(file, delimiter=',')
            data = [data_vector for data_vector in data_iterator]
        return np.asarray(data, dtype=float)  # TODO type

    @staticmethod
    def reformat_labels(data, labels):
        reformatted_labels = []

        for row in range(len(labels)):
            tmp = np.subtract(labels[row], data[row])
            tmp = np.where(tmp != 0)
            reformatted_labels.extend(tmp[0])

        return np.asarray(reformatted_labels)
