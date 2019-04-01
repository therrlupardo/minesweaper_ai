import itertools
import time
from math import floor

from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board


class ProbabilitySolver:
    game_board: Board

    # def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
    #     self.game_board = Board(driver, game, height, width, mines_counter) # needed only if playing only this strategy

    def __init__(self, game_board):
        self.game_board = game_board # needed only if playing only this strategy

    def play(self):
        time0 = time.time()
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))

        while self.probability_method(self.game_board):
            self.game_board.update_fields()
            if self.game_board.game.find_element_by_id("face").get_attribute("class") == "facewin":
                break

        if self.game_board.mines_counter == 0:
            blanks = self.game_board.game.find_elements_by_class_name("square.blank")
            for elem in blanks:
                if elem.get_attribute("style") != "display: none;":
                    elem.click()

        return (self.game_board.update_fields() and self.game_board.mines_counter == 0)

    def probability_method(self, game_board):
        changed_anything = False
        matrix_columns = []
        # stwórz wektor pól, w których może być mina, które sąsiadują z polami ze znaną wartością
        for elem in game_board.neighbours_of_mines:
            for neighbour in elem.neighbours:
                if neighbour.game_class == "square blank":
                    if neighbour not in matrix_columns:
                        matrix_columns.append(neighbour)

        return changed_anything
