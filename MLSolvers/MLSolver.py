from MLSolvers.Model import Model
from Minesweeper.Board import Board
from selenium.webdriver.firefox.webdriver import WebDriver


class MLSolver:

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.model = Model()
        self.game_board = Board(driver, game, height, width, mines_counter)
