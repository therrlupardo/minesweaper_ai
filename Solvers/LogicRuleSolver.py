from Minesweeper.Board import Board
from math import floor
from random import randrange
import pyDatalog
from pyDatalog import pyDatalog # pip install pydatalog   // pydatalog-0.17.1

class LogicRuleSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))
        while True:
            didMove = 0
            for coordY in range(self.game_board.height):
                for coordX in range(self.game_board.width):
                    if self.game_board.board[coordY][coordX].clicked:
                        #prologowe zmienne
                        pyDatalog.create_terms('counting,A,B,A1,B1,squareVector')\
                        #rzutowanie kawałka 3x3 z głównej planszy na tablicę prologową
                        for i in range(9):
                            +(squareVector[i] == self.game_board.board[coordY + floor(i/3) - 1][coordX + i%3 - 1].game_class)

                        whatToCount = ['square bombflagged', 'square blank']
                        for countOption in whatToCount:
                            (counting(countOption, A, B)) <= ( (counting(countOption, A1, B1)) & (A == A1 + 1) &
                                                            (B == B1 + 1) & (squareVector[A] == ' ') & (A <= 8) & (B <= 8))
                            (counting(countOption, A, B)) <= ((counting(countOption, A1, B)) & (A == A1 + 1) &
                                                            (~(squareVector[A] == ' ')) & (A <= 8) & (B <= 8))
                            (counting(countOption, A, B)) <= ((A == -1) & (B == 0))

                        #zapytanie wyrzuca listę tupli
                        countedFlagged = pyDatalog.ask('counting(whatToCount[0],8, B)').answers[0][0]
                        countedBlank = pyDatalog.ask('counting(whatToCount[1],8, B)').answers[0][0]
                        blankSquaresIndexes = pyDatalog.ask('squareVector[A]==whatToCount[1]').answers

                        #zaznacz flagi jeśli dookoła pola flagowane i puste sumują się do danej cyfry
                        if self.game_board.board[coordY][coordX].game_class.liczba == countedBlank + countedFlagged:
                            for blankIndex in blankSquaresIndexes:
                                didMove = 1
                                self.game_board.send_right_click(coordY + floor(blankIndex/3) - 1, coordX + blankIndex%3 - 1)
                        #odkryj puste jeśli dookoła jest n oznaczonych flagą
                        elif self.game_board.board[coordY][coordX].game_class.liczba == countedFlagged:
                            for blankIndex in blankSquaresIndexes:
                                didMove = 1
                                self.game_board.send_left_click(coordY + floor(blankIndex/3) - 1, coordX + blankIndex%3 - 1)
            if didMove == 0:
                self.game_board.send_left_click(randrange(self.game_board.board.height), randrange(self.game_board.board.width))
