import copy

from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from Minesweeper.Field import Field


class Board:
    # class variable:
    field_values = ['square open0', 'square open1', 'square open2', 'square open3', 'square open4', 'square open5',
                    'square open6', 'square open7', 'square open8', 'square bombflagged', 'square bombrevealed']

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        # instance variables:
        self.driver = driver
        self.game = game
        self.width = width
        self.height = height
        self.mines_counter = mines_counter

        self.board = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Field(j, i))
            self.board.append(row)

        for row in self.board:
            for elem in row:
                elem.neighbours = self.get_field_neighbours(elem)

        self.neighbours_of_mines = []
        self.mines = []
        self.train_data = []
        self.validation_data = []

    def print(self):
        i = 0
        for row in self.board:
            print(str(i), end=" ")
            for elem in row:
                print(elem, end="")
            print()
            i = i + 1

    def update_fields(self):
        for name in self.field_values:
            fields = self.game.find_elements_by_class_name(name.replace(' ', '.'))

            for field in fields:
                field_id = field.get_attribute('id')
                y, x = field_id.split('_')
                elem = self.board[int(y) - 1][int(x) - 1]
                if elem.game_class != name:
                    elem.set_game_class(name)
                    if name not in ('square open0', 'square blank', 'square bombflagged', 'square bombsreaveled'):
                        self.neighbours_of_mines.append(elem)

            for elem in self.neighbours_of_mines:
                if elem.game_class in ('square open0', 'square blank', 'square bombflagged', 'square bombsreaveled'):
                    self.neighbours_of_mines.remove(elem)
                elif elem.mine_neighbours == 11 or elem.mine_neighbours == 10:
                    self.neighbours_of_mines.remove(elem)

            if name == self.field_values[-1]:
                if len(fields) != 0:
                    return False

        return True

    def send_left_click(self, y, x):
        elem: Field = self.board[y][x]
        self.game.find_element_by_id(elem.game_id).click()
        return self.update_fields()

    def send_right_click(self, y, x):
        elem: Field = self.board[y][x]
        if elem.game_id not in self.mines:
            self.train_data.extend(self.generate_learning_data(y, x))
            elem.set_game_class('square bombflagged')
            self.validation_data.extend(self.generate_learning_data(y, x))

            action_chains = ActionChains(self.driver)
            action_chains.context_click(self.game.find_element_by_id(elem.game_id)).perform()

            self.mines_counter -= 1
            self.mines.append(elem.game_id)
            return self.update_fields()

    def click_all_square_blanks(self):
        blanks = self.game.find_elements_by_class_name('square.blank')
        for elem in blanks:
            if elem.get_attribute('style') != 'display: none;':
                elem.click()

    # zwraca sąsiadów danego pola
    def get_field_neighbours(self, elem):
        x, y = elem.x, elem.y
        # zwraca sąsiadów danego pola
        neighbours = []
        if y == 0:
            if x == 0:
                neighbours = [self.board[y + 1][x], self.board[y + 1][x + 1], self.board[y][x + 1]]
            elif x == self.width - 1:
                neighbours = [self.board[y + 1][x], self.board[y + 1][x - 1], self.board[y][x - 1]]
            else:
                neighbours = [self.board[y + 1][x], self.board[y + 1][x - 1], self.board[y][x - 1],
                              self.board[y + 1][x + 1], self.board[y][x + 1]]
        elif y == self.height - 1:
            if x == 0:
                neighbours = [self.board[y - 1][x], self.board[y - 1][x + 1], self.board[y][x + 1]]
            elif x == self.width - 1:
                neighbours = [self.board[y - 1][x], self.board[y - 1][x - 1], self.board[y][x - 1]]
            else:
                neighbours = [self.board[y - 1][x], self.board[y - 1][x - 1], self.board[y][x - 1],
                              self.board[y - 1][x + 1], self.board[y][x + 1]]
        elif x == 0:
            neighbours = [self.board[y][x + 1], self.board[y - 1][x + 1], self.board[y - 1][x],
                          self.board[y + 1][x + 1], self.board[y + 1][x]]
        elif x == self.width - 1:
            neighbours = [self.board[y][x - 1], self.board[y - 1][x - 1], self.board[y - 1][x],
                          self.board[y + 1][x - 1], self.board[y + 1][x]]
        else:
            neighbours = [self.board[y - 1][x - 1], self.board[y - 1][x], self.board[y - 1][x + 1],
                          self.board[y][x - 1], self.board[y][x + 1],
                          self.board[y + 1][x - 1], self.board[y + 1][x], self.board[y + 1][x + 1]]
        return neighbours

    def generate_learning_data(self, y, x):
        matrix_size = 4
        data = []

        for y_shift in range(matrix_size):
            for x_shift in range(matrix_size):
                vector = []
                for j in range(y - y_shift, y + matrix_size - y_shift):
                    if 0 <= j < len(self.board):
                        for i in range(x - x_shift, x + matrix_size - x_shift):
                            if 0 <= i < len(self.board[0]):
                                vector.append(copy.copy(self.board[j][i]))
                if len(vector) == matrix_size * matrix_size:
                    data.append(vector)
        return data
