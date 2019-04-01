from math import floor
from random import randrange

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
            if self.game_board.game.find_element_by_id("face").get_attribute("class") == "facewin":
                break
            else:
                self.matrix_solver.matrix_method(self.game_board)
                self.game_board.update_fields()
                if self.game_board.game.find_element_by_id("face").get_attribute("class") == "facewin":
                    break
                else:
                    if self.simple_solver.simple_method(self.game_board):
                        self.game_board.update_fields()
                    else:
                        repeat = False

        if self.game_board.mines_counter == 0:
            blanks = self.game_board.game.find_elements_by_class_name("square.blank")
            for elem in blanks:
                if elem.get_attribute("style") != "display: none;":
                    elem.click()
        else:
            print("No ideas, fire in the hole!")
            blanks = self.game_board.game.find_elements_by_class_name("square.blank")
            elems = []
            for elem in blanks:
                if elem.get_attribute("style") != "display: none;":
                    elems.append(elem)
            i = int(randrange(len(elems)))
            elems[i].click()
            if self.game_board.game.find_element_by_id("face").get_attribute("class") == "facedead":
                repeat = False
            else:
                repeat = True

        print("Game time: " + str(time.time() - time0))
        print("Mines left: ", self.game_board.mines_counter)
        return (self.game_board.update_fields() and self.game_board.mines_counter == 0)

