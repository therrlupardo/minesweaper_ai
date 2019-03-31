from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
from Minesweeper.Field import Field


class AISolver:
    game_board: Board

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)
