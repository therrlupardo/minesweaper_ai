from Minesweeper.Board import Board
from math import floor
from random import randrange
import pyDatalog
from pyDatalog import pyDatalog # pip install pydatalog   // pydatalog-0.17.1

# prologowe zmienne
pyDatalog.create_terms('counting,A,B,A1,B1,squareVector') # od razu wiedziałem, że to trzeba wywołać poza funkcją

class LogicRuleSolver:
    def __init__(self, game_board):
        self.game_board = game_board

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))

        while True:
            if self.logic_rule_method(self.game_board):
                self.game_board.update_fields()
            else:
                self.game_board.send_left_click(randrange(self.game_board.height), randrange(self.game_board.width))
            if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facewin':
                break

        if self.game_board.mines_counter == 0:
            blanks = self.game_board.game.find_elements_by_class_name('square.blank')
            for elem in blanks:
                if elem.get_attribute('style') != 'display: none;':
                    elem.click()

        return self.game_board.update_fields() and self.game_board.mines_counter == 0

    def logic_rule_method(self, game_board):
        whatToCount = ['square bombflagged', 'square blank']
        for countOption in whatToCount:
            (counting(countOption, A, B)) <= ((counting(countOption, A1, B1)) & (A == A1 + 1) &
                                              (B == B1 + 1) & (squareVector[A] == countOption) & (A <= 8) & (
                                                      B <= 8))
            (counting(countOption, A, B)) <= ((counting(countOption, A1, B)) & (A == A1 + 1) &
                                              (~(squareVector[A] == countOption)) & (A <= 8) & (B <= 8))
            (counting(countOption, A, B)) <= ((A == -1) & (B == 0))
        didSolveAnything = 0
        didMove = 1
        while didMove:
            didMove = 0
            for elem in game_board.neighbours_of_mines:
                print("checking elem (", elem.x, elem.y, ")")
                # rzutowanie kawałka 3x3 z głównej planszy na tablicę prologową
                for i in range(9):
                    if elem.x + i % 3 > 0 and elem.y + floor(i / 3) > 0 and \
                            elem.x + i % 3 <= game_board.width and elem.y + floor(i / 3) <= game_board.height:
                        +(squareVector[i] == self.game_board.board[elem.y + floor(i / 3) - 1][elem.x + i % 3 - 1].game_class)
                    else:
                        +(squareVector[i] == 'BORDER')
                # zapytanie wyrzuca listę tupli
                countedFlagged = pyDatalog.ask('counting(\'square bombflagged\',8, B)').answers[0][0]
                countedBlank = pyDatalog.ask('counting(\'square blank\',8, B)').answers[0][0]
                if countedBlank != 0:
                    blankSquaresIndexes = pyDatalog.ask('squareVector[A]==\'square blank\'').answers
                else:
                    blankSquaresIndexes = []
                # zaznacz flagi jeśli dookoła pola flagowane i puste sumują się do danej cyfry
                if int(elem.game_class[11], 10) == countedBlank + countedFlagged:
                    for blankIndex in blankSquaresIndexes:
                        didSolveAnything = 1
                        didMove = 1
                        print("Clicking right at (" ,elem.x + blankIndex[0] % 3 - 1, elem.y + floor(blankIndex[0] / 3) - 1, ")", end='')
                        self.game_board.send_right_click(elem.y + floor(blankIndex[0] / 3) - 1,
                                                         elem.x + blankIndex[0] % 3 - 1)
                        print("Clicked")
                # odkryj puste jeśli dookoła jest n oznaczonych flagą
                elif int(elem.game_class[11], 10) == countedFlagged:
                    for blankIndex in blankSquaresIndexes:
                        didSolveAnything = 1
                        didMove = 1
                        print("Clicking left at (",elem.x + blankIndex[0] % 3 - 1, elem.y + floor(blankIndex[0] / 3) - 1, ")", end='')
                        self.game_board.send_left_click(elem.y + floor(blankIndex[0] / 3) - 1,
                                                        elem.x + blankIndex[0] % 3 - 1)
                        print("Clicked")
        return didSolveAnything
