from math import floor
from Minesweeper.Field import Field


class SimpleSolver:

    def __init__(self, game_board):
        self.game_board = game_board  # needed only if playing only this strategy

    def play(self):
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))

        while self.simple_method(self.game_board):
            self.game_board.update_fields()
            if self.game_board.game.find_element_by_id('face').get_attribute('class') == 'facewin':
                break
        if self.game_board.mines_counter == 0:
            blanks = self.game_board.game.find_elements_by_class_name('square.blank')
            for elem in blanks:
                if elem.get_attribute('style') != 'display: none;':
                    elem.click()
        return self.game_board.update_fields() and self.game_board.mines_counter == 0

    @staticmethod
    def simple_method(game_board):
        changed_anything = False

        for elem in game_board.neighbours_of_mines:
            if elem.mine_neighbours != 0 and elem.neighbours_solved is False:

                possibilities = 0
                flagged = 0
                neighbour: Field

                for neighbour in elem.neighbours:
                    if neighbour.game_class == 'square blank':
                        possibilities += 1
                    elif neighbour.game_class == 'square bombflagged':
                        possibilities += 1
                        flagged += 1

                # wszystkie miny już były oznaczone
                if flagged == elem.mine_neighbours:
                    game_board.neighbours_of_mines.remove(elem)
                    elem.neighbours_solved = True
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == 'square blank':
                            game_board.send_left_click(neighbour.y, neighbour.x)
                    changed_anything = True

                # wszystkie pola sąsiadujące to miny
                elif possibilities == elem.mine_neighbours:
                    elem.neighbours_solved = True
                    game_board.neighbours_of_mines.remove(elem)

                    for neighbour in elem.neighbours:
                        if neighbour.game_class == 'square blank':
                            game_board.send_right_click(neighbour.y, neighbour.x)

                    changed_anything = True
        return changed_anything
