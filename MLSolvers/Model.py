import csv
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Model:

    def __init__(self):
        print(tf.__version__)
        self.model = self.train_model()
        self.save_model(self.model)

        model = self.load_model()
        train_data, train_labels = self.import_train_data('data/data.csv', 'data/labels.csv')
        x_val = train_data[:8000]
        y_val = train_labels[:8000]

        print(model.evaluate(x_val, y_val))

    # TODO
    @staticmethod
    def make_predictions(data):
        data_tf = tf.convert_to_tensor(data, float)
        # data_tf = tf.placeholder(float, (1, 16))
        x = tf.placeholder('float')
        with tf.Session() as sess:
            print(data)
            o = sess.run(data_tf, feed_dict={x: data})
            print(o)
        return o

    def train_model(self):
        train_data, train_labels = self.import_train_data('data/data.csv', 'data/labels.csv')

        print(train_data.shape)
        print(train_labels.shape)

        with tf.Session() as sess:
            model = keras.Sequential([
                # keras.layers.GaussianDropout(0.4), #,  input_shape=(16,)),
                keras.layers.Dense(256, activation=tf.nn.relu, input_shape=(16,)),
                keras.layers.Dense(256, activation=tf.nn.relu),
                keras.layers.Dense(256, activation=tf.nn.relu),
                keras.layers.Dense(256, activation=tf.nn.relu),
                keras.layers.Dense(256, activation=tf.nn.relu),
                keras.layers.GaussianDropout(0.2),
                keras.layers.Dense(16, activation=tf.nn.softmax)
            ])

            model.compile(optimizer=tf.keras.optimizers.Adam(),
                          loss='sparse_categorical_crossentropy',
                          metrics=['accuracy'])

            x_val = train_data[:8000]
            partial_x_train = train_data[8000:]

            y_val = train_labels[:8000]
            partial_y_train = train_labels[8000:]

            # model.fit(partial_x_train,
            #           partial_y_train,
            #           epochs=25,
            #           batch_size=128,
            #           validation_data=(x_val, y_val),
            #           shuffle=True)

            model.fit(partial_x_train,
                      partial_y_train,
                      epochs=20,
                      batch_size=512,
                      shuffle=True)

            # print(model.evaluate(x_val, y_val))
            model.summary()

        return model

    @staticmethod
    def save_model(model):
        model.save('models/model.h5')

    @staticmethod
    def load_model():
        model = keras.models.load_model('models/model.h5')
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

        return np.asarray(reformatted_labels)
