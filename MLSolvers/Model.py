from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import datetime

import tensorflow as tf
import numpy as np


class Model:

    def __init__(self):
        print(tf.__version__)
        # tf.debugging.set_log_device_placement(True)

        # self.model = self.train_model()
        # self.save_model(self.model)

        self.model = self.load_model()
        # train_data, train_labels = self.import_train_data('data/data.csv', 'data/labels.csv')
        # x_val_2 = train_data[:30000]        #first 30000 elemsents
        # y_val_2 = train_labels[:30000]
        # x_val = train_data[-30000:]
        # y_val = train_labels[-30000:]

        # print(self.model.evaluate(x_val, y_val))
        # print(self.model.evaluate(x_val_2, y_val_2))
        # print(self.make_prediction(x_val))
        # print(y_val)

    def train_model(self):
        train_data, train_labels = self.import_train_data('data/data.csv', 'data/labels.csv')

        print(train_data.shape)
        print(train_labels.shape)

        model = tf.keras.Sequential([
            # tf.keras.layers.GaussianDropout(0.2),
            tf.keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(16,)),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            # tf.keras.layers.Dense(256, activation=tf.nn.relu),
            # tf.keras.layers.Dense(256, activation=tf.nn.relu),
            # tf.keras.layers.GaussianDropout(0.2),
            tf.keras.layers.Dense(17, activation=tf.nn.softmax)
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(),  # keras.optimizers.SGD(lr=0.2)
                      loss='sparse_categorical_crossentropy',
                      # loss='categorical_crossentropy',
                      metrics=['accuracy'])

        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        x_val = train_data[:30000]
        y_val = train_labels[:30000]
        x_val2 = np.concatenate((x_val, train_data[-30000:]))
        y_val2 = np.concatenate((y_val, train_labels[-30000:]))

        # with tf.device('/device:GPU:0'):
        model.fit(train_data,
                  train_labels,
                  epochs=20,
                  batch_size=512,
                  shuffle=True,
                  validation_data=(x_val2, y_val2),
                  callbacks=[tensorboard_callback])

        model.summary()
        return model

    def make_prediction(self, data):
        prediction = self.model.predict(np.asarray(data, dtype=float))
        label = np.argmax(prediction, axis=1)
        return np.asarray(label, dtype=int)

    def make_probabilities_prediction(self, data):
        prediction = self.model.predict(np.asarray(data, dtype=float))
        return np.asarray(prediction, dtype=float)

    @staticmethod
    def save_model(model):
        model.save('models/model2.h5')

    @staticmethod
    def load_model():
        model = tf.keras.models.load_model('models/model2.h5')
        return model

    def import_train_data(self, data_filename, labels_filename):
        train_data = self.import_data(data_filename)
        train_labels = self.import_data(labels_filename)
        train_labels = self.reformat_labels(train_data, train_labels)

        return train_data, train_labels

    @staticmethod
    def import_data(filename):
        with open(filename, 'r') as file:
            data_iterator = csv.reader(file, delimiter=',')
            data = [data_vector for data_vector in data_iterator]

        return np.asarray(data, dtype=float)

    @staticmethod
    def reformat_labels(data, labels):
        reformatted_labels = []

        for row in range(len(labels)):
            tmp = np.subtract(labels[row], data[row])
            tmp = np.where(tmp != 0)
            reformatted_labels.extend(tmp[0])

        tmp = len(labels) - len(reformatted_labels)

        for _ in range(len(labels) - len(reformatted_labels)):  # TODO !!!!
            tmp = [16]
            reformatted_labels.extend(tmp)

        return np.asarray(reformatted_labels)
