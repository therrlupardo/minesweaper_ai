import time

from selenium.webdriver.firefox.webdriver import WebDriver
from Minesweeper.Field import Field


class Board:
    height = 0
    width = 0
    mines_counter = 0
    board = []
    game: WebDriver
    driver: WebDriver
    field_values = ["square open0", "square open1", "square open2", "square open3", "square open4", "square open5",
                    "square open6", "square open7", "square open8", "square bombflagged", "square bombrevealed"]
    neighbours_of_mines = []

    def __init__(self, driver: WebDriver, game: WebDriver, height, width, mines_counter):
        self.driver = driver
        self.game = game
        self.width = width
        self.height = height
        self.mines_counter = mines_counter
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Field(j, i))
            self.board.append(row)
        time0 = time.time()
        for row in self.board:
            for elem in row:
                elem.neighbours = self.get_field_neighbours(elem)
        print("Time of setting neighbours: ", (time.time() - time0))

    def print(self):
        for row in self.board:
            for elem in row:
                print(elem, end=" ")
            print()

    def update_fields(self):
        for name in self.field_values:
            fields = self.game.find_elements_by_class_name(name.replace(' ', '.'))

            for field in fields:
                field_id = field.get_attribute("id")
                y, x = field_id.split("_")
                elem = self.board[int(y) - 1][int(x) - 1]
                if elem.game_class != name:
                    elem.set_game_class(name)
                    if name not in ("square open0", "square blank", "square bombflagged", "square bombsreaveled"):
                        self.neighbours_of_mines.append(elem)

            if name == self.field_values[-1]:
                if len(fields) != 0:
                    return False

        return True

    def send_click(self, y, x):
        elem: Field = self.board[y][x]
        self.game.find_element_by_id(elem.game_id).click()
        return self.update_fields()

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
