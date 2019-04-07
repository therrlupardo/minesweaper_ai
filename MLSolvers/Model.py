import csv
import tensorflow as tf
from tensorflow import keras
import numpy as np


class Model:

    def __init__(self):
        print(tf.__version__)
        train_data = self.import_data('data.csv')
        train_labels = self.import_data('labels.csv')

        print(train_data.shape)
        print(train_labels.shape)
        train_labels = self.reformat_labels(train_data, train_labels)
        print(train_labels)
        print(train_labels.shape)

    @staticmethod
    def import_data(filename):
        with open(filename, 'r') as file:
            data_iterator = csv.reader(file, delimiter=',')
            data = [data_vector for data_vector in data_iterator]
        return np.asarray(data, dtype=float)  # TODO

    @staticmethod
    def reformat_labels(data, labels):
        reformatted_labels = []

        for row in range(len(labels)):
            tmp = np.subtract(labels[row], data[row])
            tmp = np.where(tmp == 1)
            reformatted_labels.extend(tmp[0])

        return np.asarray(reformatted_labels)
