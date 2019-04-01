from math import floor
from random import randrange

from numpy.distutils.fcompiler import none
from numpy.matlib import rand
from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
import time

from Solvers.MatrixSolver import MatrixSolver
from Solvers.ProbabilitySolver import ProbabilitySolver
from Solvers.SimpleSolver import SimpleSolver


class LogicSolver:
    game_board: Board
    simple_solver: SimpleSolver
    matrix_solver: MatrixSolver
    probability_solver: ProbabilitySolver


    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)
        self.simple_solver = SimpleSolver(driver, game, height, width, mines_counter)
        self.matrix_solver = MatrixSolver(driver, game, height, width, mines_counter)
        self.probability_solver = ProbabilitySolver(driver, game, height, width, mines_counter)




    def play(self):
        time0 = time.time()
        self.game_board.send_left_click(floor(self.game_board.height/2), floor(self.game_board.width/2))

        self.game_board.update_fields()
        # self.matrix_solver.matrix_method(self.game_board)

        repeat = True
        while repeat:
            if self.game_board.game.find_element_by_id('face').get_attribute("class") == 'facewin':
                break
            else:
                if self.game_board.mines_counter == 0:
                    self.game_board.click_all_square_blanks()
                else:
                    self.game_board.update_fields()
                    if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facewin':
                        break
                    else:
                        if self.game_board.mines_counter == 0:
                            self.game_board.click_all_square_blanks()
                        elif self.simple_solver.simple_method(self.game_board):
                            self.game_board.update_fields()
                        else:
                            repeat = False

        if self.game_board.mines_counter == 0:
            self.game_board.click_all_square_blanks()
        else:
            blanks = self.game_board.game.find_elements_by_class_name('square.blank')
            elems = []
            for elem in blanks:
                if elem.get_attribute('style') != 'display: none;':
                    elems.append(elem)
            if len(elems) > 0:
                i = int(randrange(len(elems)))
                elems[i].click()
                if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facedead':
                    repeat = False
                else:
                    repeat = True

        out = self.game_board.update_fields() and self.game_board.mines_counter == 0
        del self.game_board
        del self.simple_solver
        del self.matrix_solver
        del self.probability_solver

        return out

