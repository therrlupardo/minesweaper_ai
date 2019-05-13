from math import floor
from random import randrange
from pyDatalog import pyDatalog
from selenium.webdriver.firefox.webdriver import WebDriver
from Minesweeper.Board import Board

# prologowe zmienne
pyDatalog.create_terms('counting,A,B,A1,B1,squareVector')


class PrologSolver:
    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)

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
        what_to_count = ['square bombflagged', 'square blank']
        for count_option in what_to_count:
            (counting(count_option, A, B)) <= ((counting(count_option, A1, B1)) & (A == A1 + 1) &
                                               (B == B1 + 1) & (squareVector[A] == count_option) & (A <= 8) & (
                                                       B <= 8))
            (counting(count_option, A, B)) <= ((counting(count_option, A1, B)) & (A == A1 + 1) &
                                               (~(squareVector[A] == count_option)) & (A <= 8) & (B <= 8))
            (counting(count_option, A, B)) <= ((A == -1) & (B == 0))
        did_solve_anything = 0
        did_move = 1
        while did_move:
            did_move = 0
            for elem in game_board.neighbours_of_mines:
                print("checking elem (", elem.x, elem.y, ")")
                # rzutowanie kawałka 3x3 z głównej planszy na tablicę prologową
                for i in range(9):
                    if 0 < elem.x + i % 3 <= game_board.width and 0 < elem.y + floor(i / 3) <= game_board.height:
                        +(squareVector[i] == self.game_board.board[elem.y + floor(i / 3) - 1][
                            elem.x + i % 3 - 1].game_class)
                    else:
                        +(squareVector[i] == 'BORDER')
                # zapytanie wyrzuca listę tupli
                counted_flagged = pyDatalog.ask('counting(\'square bombflagged\',8, B)').answers[0][0]
                counted_blank = pyDatalog.ask('counting(\'square blank\',8, B)').answers[0][0]
                if counted_blank != 0:
                    blank_squares_indexes = pyDatalog.ask('squareVector[A]==\'square blank\'').answers
                else:
                    blank_squares_indexes = []
                # zaznacz flagi jeśli dookoła pola flagowane i puste sumują się do danej cyfry
                if int(elem.game_class[11], 10) == counted_blank + counted_flagged:
                    for blankIndex in blank_squares_indexes:
                        did_solve_anything = 1
                        did_move = 1
                        print("Clicking right at (", elem.x + blankIndex[0] % 3 - 1,
                              elem.y + floor(blankIndex[0] / 3) - 1, ")", end='')
                        self.game_board.send_right_click(elem.y + floor(blankIndex[0] / 3) - 1,
                                                         elem.x + blankIndex[0] % 3 - 1)
                        print("Clicked")
                # odkryj puste jeśli dookoła jest n oznaczonych flagą
                elif int(elem.game_class[11], 10) == counted_flagged:
                    for blankIndex in blank_squares_indexes:
                        did_solve_anything = 1
                        did_move = 1
                        print("Clicking left at (", elem.x + blankIndex[0] % 3 - 1,
                              elem.y + floor(blankIndex[0] / 3) - 1, ")", end='')
                        self.game_board.send_left_click(elem.y + floor(blankIndex[0] / 3) - 1,
                                                        elem.x + blankIndex[0] % 3 - 1)
                        print("Clicked")
        return did_solve_anything
