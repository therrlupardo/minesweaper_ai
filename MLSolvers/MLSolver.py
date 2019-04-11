import copy
from math import floor

from MLSolvers.Model import Model
from Minesweeper.Board import Board
from selenium.webdriver.firefox.webdriver import WebDriver
import numpy as np


class MLSolver:

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.model = Model()
        self.game_board = Board(driver, game, height, width, mines_counter)

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))
        self.game_board.update_fields()

        # while self.game_board.game.find_element_by_id('face').get_attribute("class") == 'facesmile':
        #     TODO
        self.search_outline_fields()

        return True if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facewin' else False

    def search_outline_fields(self):
        prediction_board = np.zeros([self.game_board.height, self.game_board.width], dtype=int)
        outline_fields = self.game_board.neighbours_of_mines

        for field in outline_fields:
            prediction_board = self.generate_prediction_board(field.y, field.x, prediction_board)

        mines_coordinates = np.where(prediction_board == np.amax(prediction_board))
        # where zwraca array zw wsp. y i drugi array ze wsp. x

        for i in range(len(mines_coordinates[0])):
            if self.game_board.board[mines_coordinates[0][i]][mines_coordinates[1][i]].game_class == 'square blank':
                self.game_board.send_right_click(mines_coordinates[0][i], mines_coordinates[1][i])

    def generate_prediction_board(self, y, x, prediction_board):
        matrix_size = 4

        for y_shift in range(matrix_size):
            for x_shift in range(matrix_size):
                vector = []
                for j in range(y - y_shift, y + matrix_size - y_shift):
                    if 0 <= j < len(self.game_board.board):
                        for i in range(x - x_shift, x + matrix_size - x_shift):
                            if 0 <= i < len(self.game_board.board[0]):
                                vector.append(copy.copy(self.game_board.board[j][i].mine_neighbours))

                if len(vector) == matrix_size * matrix_size:
                    y_mine, x_mine = self.predict_mine(vector)
                    prediction_board[y_mine + y - y_shift][x_mine + x - x_shift] += 1

        return prediction_board

    def predict_mine(self, data):
        label = self.model.make_prediction(data)

        matrix_size = 4
        x = label % matrix_size
        y = int(label / matrix_size)
        return y, x
