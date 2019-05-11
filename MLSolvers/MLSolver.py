import copy
from math import floor

from MLSolvers.Model import Model
from Minesweeper.Board import Board
from selenium.webdriver.firefox.webdriver import WebDriver
import numpy as np


class MLSolver:

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter, model):
        self.game_board = Board(driver, game, height, width, mines_counter)
        # self.expected_game_board = [[0 for _ in range(height)] for _ in range(width)]
        # self.update_expected_game_board()
        self.model = Model()

    # def update_expected_game_board(self):
    #     for i in range(len(self.expected_game_board)):
    #         for j in range(len(self.expected_game_board[0])):
    #             self.expected_game_board[i][j] = self.game_board.board[i][j].mine_neighbours

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))
        self.game_board.update_fields()

        while self.game_board.game.find_element_by_id('face').get_attribute("class") == 'facesmile':
            self.search_outline_fields()

        return True if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facewin' else False

    def search_outline_fields(self):
        # self.update_expected_game_board()
        prediction_board = np.zeros([self.game_board.height, self.game_board.width], dtype=float)
        outline_fields = self.game_board.neighbours_of_mines
        mines_coordinates = [list(), list()]

        # for field in outline_fields:
        for i in range(len(outline_fields)):
            prediction_board = self.generate_prediction_board(outline_fields[i].y, outline_fields[i].x,
                                                              prediction_board)

        # lub z indent
        coord = np.where(prediction_board == np.amax(prediction_board))
        mines_coordinates[0].extend(coord[0])
        mines_coordinates[1].extend(coord[1])
        # where zwraca array zw wsp. y i drugi array ze wsp. x

        # prediction_board[mines_coordinates[0][i]][mines_coordinates[1][i]] = 0
        prediction_board[mines_coordinates[0][0]][mines_coordinates[1][0]] = 0

        # self.expected_game_board[mines_coordinates[0][i]][mines_coordinates[1][i]] = 10
        # self.expected_game_board[mines_coordinates[0][0]][mines_coordinates[1][0]] = 10

        # gdyby byly dwa pola o takiej samej wartosci:
        for i in range(len(mines_coordinates[0])):
            if self.game_board.board[mines_coordinates[0][i]][mines_coordinates[1][i]].game_class == 'square blank':
                self.game_board.send_right_click(mines_coordinates[0][i], mines_coordinates[1][i])

            # self.game_board.update_fields()

        for field in outline_fields:
            self.game_board.check_field_neighbours(field.y, field.x)

    def generate_prediction_board(self, y, x, prediction_board):
        matrix_size = 4
        predict_data = []
        coord = []

        for y_shift in range(matrix_size):
            for x_shift in range(matrix_size):
                vector = []
                for j in range(y - y_shift, y + matrix_size - y_shift):
                    if 0 <= j < len(self.game_board.board):
                        for i in range(x - x_shift, x + matrix_size - x_shift):
                            if 0 <= i < len(self.game_board.board[0]):
                                vector.append(copy.copy(self.game_board.board[j][i].mine_neighbours))
                                # vector.append(copy.copy(self.expected_game_board[j][i]))

                if len(vector) == matrix_size * matrix_size:
                    predict_data.append(vector)
                    coord.append([y - y_shift, x - x_shift])

        # y_mine, x_mine = self.predict_mine(predict_data)
        #
        # for i in range(len(coord)):
        #     if y_mine[i] != -1:
        #         prediction_board[y_mine[i] + coord[i][0]][x_mine[i] + coord[i][1]] += 1

        self.predict_mines_probabilities(predict_data, coord, prediction_board)

        return prediction_board

    def predict_mine(self, data):
        labels = self.model.make_prediction(data)

        matrix_size = 4
        # jak sie uda to szybciej na numpy elementwise
        x = [label % matrix_size if label != 16 else -1 for label in labels]  # TODO ???
        y = [int(label / matrix_size) if label != 16 else -1 for label in labels]

        return np.asarray(y), np.asarray(x)

    def predict_mines_probabilities(self, data, coord, prediction_board):
        probabilities = self.model.make_probabilities_prediction(data)

        matrix_size = 4

        for i in range(len(probabilities)):
            # for j in range(len(probabilities)):
            for k in range(len(probabilities[0]) - 1):  # na ostatniej pozycji prawdopodobienstwo braku miny
                prediction_board[int(k / matrix_size) + coord[i][0]][k % matrix_size + coord[i][1]] += probabilities[i][
                    k]

        return prediction_board
