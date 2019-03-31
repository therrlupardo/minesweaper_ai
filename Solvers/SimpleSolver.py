import time

from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
from Minesweeper.Field import Field


class SimpleSolver:
    game_board: Board

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.game_board = Board(driver, game, height, width, mines_counter)

    def play(self):
        time0 = time.time()
        self.game_board.send_click(5, 5)
        while self.simple_method():
            self.game_board.update_fields()

        print("Game time: " + str(time.time() - time0))
        return self.game_board.update_fields() and self.game_board.mines_counter == 0

    def simple_method(self):
        time0 = time.time()
        changed_anything = False

        for elem in self.game_board.neighbours_of_mines:
            if elem.mine_neighbours != 0 and elem.neighbours_solved is False:

                possibilities = 0
                flagged = 0
                neighbour: Field
                for neighbour in elem.neighbours:
                    if neighbour.game_class == "square blank":
                        possibilities += 1
                    elif neighbour.game_class == "square bombflagged":
                        possibilities += 1
                        flagged += 1

                # wszystkie miny już były oznaczone
                if flagged == elem.mine_neighbours:
                    self.game_board.neighbours_of_mines.remove(elem)
                    elem.neighbours_solved = True
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            self.game_board.game.find_element_by_id(neighbour.game_id).click()
                    changed_anything = True

                # wszystkie pola sąsiadujące to miny
                elif possibilities == elem.mine_neighbours:
                    elem.neighbours_solved = True
                    self.game_board.neighbours_of_mines.remove(elem)
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            action_chains = ActionChains(self.game_board.driver)
                            action_chains.context_click(
                                self.game_board.game.find_element_by_id(neighbour.game_id)).perform()
                            neighbour.set_game_class("square bombflagged")
                            self.game_board.mines_counter -= 1
                    changed_anything = True

        return changed_anything

    def simple_method2(self):
        changed_anyhing = False
        for row in self.game_board.board:
            elem: Field
            for elem in row:
                if elem.mine_neighbours != 0 and elem.neighbours_solved is False:

                    possibilities = 0
                    flagged = 0
                    neighbour: Field
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            possibilities += 1
                        if neighbour.game_class == "square bombflagged":
                            possibilities += 1
                            flagged += 1
                    # wszystkie miny już były oznaczone
                    if flagged == elem.mine_neighbours:
                        elem.neighbours_solved = True
                        for neighbour in elem.neighbours:
                            if neighbour.game_class != "square bombflagged":
                                self.game_board.game.find_element_by_id(neighbour.game_id).click()
                                changed_anyhing = True

                    # wszystkie pola sąsiadujące to miny
                    elif possibilities == elem.mine_neighbours:
                        elem.neighbours_solved = True
                        for neighbour in elem.neighbours:
                            if neighbour.game_class == "square blank":
                                action_chains = ActionChains(self.game_board.driver)
                                action_chains.context_click(
                                    self.game_board.game.find_element_by_id(neighbour.game_id)).perform()
                                neighbour.set_game_class("square bombflagged")
                                changed_anyhing = True
        return changed_anyhing
