from Minesweeper.Board import Board
from math import floor
from random import randrange
from selenium.webdriver.firefox.webdriver import WebDriver
from pyDatalog import pyDatalog  # pip install pydatalog   // pydatalog-0.17.1


class LogicRuleSolver:
    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))
        while True:
            did_move = 0
            for coordY in range(self.game_board.height):
                for coordX in range(self.game_board.width):
                    if self.game_board.board[coordY][coordX].clicked:
                        # prologowe zmienne
                        pyDatalog.create_terms('counting,A,B,A1,B1,squareVector') \
                            # rzutowanie kawałka 3x3 z głównej planszy na tablicę prologową
                        for i in range(9):
                            +(squareVector[i] == self.game_board.board[coordY + floor(i / 3) - 1][
                                coordX + i % 3 - 1].game_class)

                        whatToCount = ['square bombflagged', 'square blank']
                        for countOption in whatToCount:
                            (counting(countOption, A, B)) <= ((counting(countOption, A1, B1)) & (A == A1 + 1) &
                                                              (B == B1 + 1) & (squareVector[A] == ' ') & (A <= 8) & (
                                                                      B <= 8))
                            (counting(countOption, A, B)) <= ((counting(countOption, A1, B)) & (A == A1 + 1) &
                                                              (~(squareVector[A] == ' ')) & (A <= 8) & (B <= 8))
                            (counting(countOption, A, B)) <= ((A == -1) & (B == 0))

                        # zapytanie wyrzuca listę tupli
                        counted_flagged = pyDatalog.ask('counting(whatToCount[0],8, B)').answers[0][0]
                        counted_blank = pyDatalog.ask('counting(whatToCount[1],8, B)').answers[0][0]
                        blank_squares_indexes = pyDatalog.ask('squareVector[A]==whatToCount[1]').answers

                        # zaznacz flagi jeśli dookoła pola flagowane i puste sumują się do danej cyfry
                        if self.game_board.board[coordY][coordX].game_class.liczba == counted_blank + counted_flagged:
                            for blank_index in blank_squares_indexes:
                                did_move = 1
                                self.game_board.send_right_click(coordY + floor(blank_index / 3) - 1,
                                                                 coordX + blank_index % 3 - 1)
                        # odkryj puste jeśli dookoła jest n oznaczonych flagą
                        elif self.game_board.board[coordY][coordX].game_class.liczba == counted_flagged:
                            for blank_index in blank_squares_indexes:
                                did_move = 1
                                self.game_board.send_left_click(coordY + floor(blank_index / 3) - 1,
                                                                coordX + blank_index % 3 - 1)
            if did_move == 0:
                self.game_board.send_left_click(randrange(self.game_board.board.height),
                                                randrange(self.game_board.board.width))
