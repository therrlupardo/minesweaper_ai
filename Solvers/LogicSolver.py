from math import floor
from random import randrange
from selenium.webdriver.firefox.webdriver import WebDriver
from Minesweeper.Board import Board
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
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))

        self.game_board.update_fields()
        # self.matrix_solver.matrix_method(self.game_board)

        while self.game_board.game.find_element_by_id('face').get_attribute("class") == 'facesmile':
            if self.game_board.mines_counter == 0:
                self.game_board.click_all_square_blanks()
            else:
                self.game_board.update_fields()
                if self.simple_solver.simple_method(self.game_board):
                    self.game_board.update_fields()
                else:
                    blanks = self.game_board.game.find_elements_by_class_name('square.blank')
                    elems = []
                    for elem in blanks:
                        if elem.get_attribute('style') != 'display: none;':
                            elems.append(elem)
                    if len(elems) > 0:
                        i = int(randrange(len(elems)))
                        elems[i].click()

        out = True if self.game_board.game.find_element_by_id('face').get_attribute("class") == 'facewin' else False
        del self.game_board
        del self.simple_solver
        del self.matrix_solver
        del self.probability_solver

        return out
