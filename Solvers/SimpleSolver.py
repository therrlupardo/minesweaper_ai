import time
from math import floor

from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
from Minesweeper.Field import Field


class SimpleSolver:
    game_board: Board

    def __init__(self,driver: WebDriver, game: WebDriver, height, width, mines_counter):
        print("SimpleSolver initialized")
        self.game_board = Board(driver, game, height, width, mines_counter) # needed only if playing only this strategy

    def play(self):
        time0 = time.time()
        self.game_board.send_left_click(floor(self.game_board.height/2), floor(self.game_board.width/2))

        while self.simple_method(self.game_board):
            self.game_board.update_fields()

        print("Game time: " + str(time.time() - time0))
        print("Mines left: ", self.game_board.mines_counter)
        return (self.game_board.update_fields() and self.game_board.mines_counter == 0)

    def simple_method(self, game_board):
        changed_anyhing = False

        for elem in game_board.neighbours_of_mines:
            if elem.mine_neighbours != 0 and elem.neighbours_solved == False:

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
                    game_board.neighbours_of_mines.remove(elem)
                    elem.neighbours_solved = True
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            game_board.game.find_element_by_id(neighbour.game_id).click()
                    changed_anyhing = True

                # wszystkie pola sąsiadujące to miny
                elif possibilities == elem.mine_neighbours:
                    elem.neighbours_solved = True
                    game_board.neighbours_of_mines.remove(elem)

                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            game_board.send_right_click(neighbour.y, neighbour.x)

                    changed_anyhing = True
        return changed_anyhing
