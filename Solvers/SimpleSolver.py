import time

from selenium.webdriver.firefox.webdriver import WebDriver

from Minesweeper.Board import Board
from Minesweeper.Field import Field


class SimpleSolver:

    def __init__(self, board):
        print("SimpleSolver initialized")


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
