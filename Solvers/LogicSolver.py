from math import floor

from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
import time

from Solvers.MatrixSolver import MatrixSolver
from Solvers.SimpleSolver import SimpleSolver


class LogicSolver:
    game_board: Board
    simple_solver: SimpleSolver
    matrix_solver: MatrixSolver

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)
        self.simple_solver = SimpleSolver(driver, game, height, width, mines_counter)
        self.matrix_solver = MatrixSolver(driver, game, height, width, mines_counter)

    def play(self):
        time0 = time.time()
        self.game_board.send_left_click(floor(self.game_board.height/2), floor(self.game_board.width/2))
        self.matrix_solver.matrix_method(self.game_board)

        repeat = True
        while repeat:
            self.matrix_solver.matrix_method(self.game_board)
            self.game_board.update_fields()
            if self.simple_solver.simple_method(self.game_board):
                self.game_board.update_fields()
            else:
                repeat = False

        print("Game time: " + str(time.time() - time0))
        print("Mines left: ", self.game_board.mines_counter)
        return (self.game_board.update_fields() and self.game_board.mines_counter == 0)

