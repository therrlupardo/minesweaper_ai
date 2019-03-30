import time

from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from Field import Field


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

    def __init__(self, driver: WebDriver,game: WebDriver, height, width, mines_counter):
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

    def play(self):
        time0 = time.time()
        self.send_click(5, 5)
        while self.simple_method():
            self.update_fields()

        print("Game time: " + str(time.time() - time0))
        return (self.update_fields() and self.mines_counter == 0)


    def simple_method2(self):
        changed_anyhing = False
        for row in self.board:
            elem: Field
            for elem in row:
                if elem.mine_neighbours != 0 and elem.neighbours_solved == False:
                    neighbours = self.get_field_neighbours(elem)

                    possibilities = 0
                    flagged = 0
                    neighbour: Field
                    for neighbour in neighbours:
                        if neighbour.game_class == "square blank":
                            possibilities += 1
                        if neighbour.game_class == "square bombflagged":
                            possibilities += 1
                            flagged += 1
                    # wszystkie miny już były oznaczone
                    if flagged == elem.mine_neighbours:
                        elem.neighbours_solved = True
                        for neighbour in neighbours:
                            if neighbour.game_class != "square bombflagged":
                                self.game.find_element_by_id(neighbour.game_id).click()
                                changed_anyhing = True

                    # wszystkie pola sąsiadujące to miny
                    elif possibilities == elem.mine_neighbours:
                        elem.neighbours_solved = True
                        for neighbour in neighbours:
                            if neighbour.game_class ==  "square blank":
                                action_chains = ActionChains(self.driver)
                                action_chains.context_click(self.game.find_element_by_id(neighbour.game_id)).perform()
                                neighbour.set_game_class("square bombflagged")
                                changed_anyhing = True
        return changed_anyhing

    def simple_method(self):
        time0 = time.time()
        changed_anyhing = False
        for elem in self.neighbours_of_mines:
            print(elem.game_id, end=" ")
        print()
        for elem in self.neighbours_of_mines:
            if elem.mine_neighbours != 0 and elem.neighbours_solved == False:
                neighbours = self.get_field_neighbours(elem)

                possibilities = 0
                flagged = 0
                neighbour: Field
                for neighbour in neighbours:
                    if neighbour.game_class == "square blank":
                        possibilities += 1
                    if neighbour.game_class == "square bombflagged":
                        possibilities += 1
                        flagged += 1
                # wszystkie miny już były oznaczone
                if flagged == elem.mine_neighbours:
                    self.neighbours_of_mines.remove(elem)
                    elem.neighbours_solved = True
                    for neighbour in neighbours:
                        if neighbour.game_class != "square bombflagged":
                            self.game.find_element_by_id(neighbour.game_id).click()
                    changed_anyhing = True

                # wszystkie pola sąsiadujące to miny
                elif possibilities == elem.mine_neighbours:
                    elem.neighbours_solved = True
                    self.neighbours_of_mines.remove(elem)
                    for neighbour in neighbours:
                        if neighbour.game_class == "square blank":
                            action_chains = ActionChains(self.driver)
                            action_chains.context_click(self.game.find_element_by_id(neighbour.game_id)).perform()
                            neighbour.set_game_class("square bombflagged")
                            self.mines_counter -= 1
                    changed_anyhing = True
        print("Loop time: " + str(time.time() - time0))
        return changed_anyhing



    def get_field_neighbours(self, field):
        # zwraca sąsiadów danego pola
        x, y = field.x, field.y
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