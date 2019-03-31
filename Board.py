import time
import numpy as np
from scipy.linalg import lu
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
                    if elem.game_class == "square bombflagged":
                        self.mines_counter += 1                     # gdzieś jest bug, nie oznaczało bomb,
                        # self.send_right_click(elem.y, elem.x)     # mimo iż w kodzie były oznaczone.
                        action_chains = ActionChains(self.driver)   # chyba naciska 2 razy, trzeba +1 by wyrównać
                        action_chains.context_click(self.game.find_element_by_id(elem.game_id)).perform()
                        print("Error checker")
                    else:
                        elem.set_game_class(name)
                        if name not in ("square open0", "square blank", "square bombflagged", "square bombsreaveled"):
                            self.neighbours_of_mines.append(elem)

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
        action_chains = ActionChains(self.driver)
        action_chains.context_click(self.game.find_element_by_id(elem.game_id)).perform()
        elem.set_game_class("square bombflagged")
        self.mines_counter -= 1
        return self.update_fields()

    def play(self):
        time0 = time.time()
        self.send_left_click(0, 0)
        self.matrix_method()

        repeat = True
        while repeat:
            self.matrix_method()
            self.update_fields()
            if self.simple_method():
                self.update_fields()
            else:
                repeat = False

        self.check_errors()

        print("Game time: " + str(time.time() - time0))
        print("Mines left: ", self.mines_counter)
        return (self.update_fields() and self.mines_counter == 0)

    def simple_method(self):
        time0 = time.time()
        changed_anyhing = False

        for elem in self.neighbours_of_mines:
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
                    self.neighbours_of_mines.remove(elem)
                    elem.neighbours_solved = True
                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            self.game.find_element_by_id(neighbour.game_id).click()
                    changed_anyhing = True

                # wszystkie pola sąsiadujące to miny
                elif possibilities == elem.mine_neighbours:
                    elem.neighbours_solved = True
                    self.neighbours_of_mines.remove(elem)

                    for neighbour in elem.neighbours:
                        if neighbour.game_class == "square blank":
                            self.send_right_click(neighbour.y, neighbour.x)

                    changed_anyhing = True
        return changed_anyhing

    # zwraca sąsiadów danego pola
    def get_field_neighbours(self, elem):
        x, y = elem.x, elem.y
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

    def matrix_method(self):
        changed_anything = False
        matrix = []
        matrix_columns = []
        # stwórz wektor pól, w których może być mina, które sąsiadują z polami ze znaną wartością
        for elem in self.neighbours_of_mines:
            for neighbour in elem.neighbours:
                if neighbour.game_class == "square blank":
                    if neighbour not in matrix_columns:
                        matrix_columns.append(neighbour)

        # uzupełnij macierz
        for elem in self.neighbours_of_mines:
            matrix_row = []
            for column in matrix_columns:
                if column in elem.neighbours:
                    matrix_row.append(1)
                else:
                    matrix_row.append(0)
            matrix.append(matrix_row)

        # stwórz wektor rozwiązań
        solutions = []
        for elem in self.neighbours_of_mines:
            value = 0
            for neighbour in elem.neighbours:
                if neighbour.game_class == "square bombflagged":
                    value += 1
            solutions.append(int(elem.mine_neighbours) - value)

        for i in range(len(matrix)):
            matrix[i].append(solutions[i])

        matrix = self.eliminate(matrix)

        for row in matrix:
            sumAbs = 0
            sum = 0
            for elem in row:
                sumAbs += abs(elem)
                sum += elem
            sumAbs -= abs(row[-1])
            sum -= row[-1]
            if sumAbs == abs(row[-1]):
                for i in range(len(row) - 1):
                    if row[i] != 0:
                        elem: Field = matrix_columns[i]
                        self.send_right_click(elem.y, elem.x)
                        changed_anything = True
            elif abs(sum) == sumAbs and row[-1] == 0:
                for i in range(len(row) - 1):
                    if row[i] != 0:
                        elem: Field = matrix_columns[i]
                        self.send_left_click(elem.y, elem.x)
                        changed_anything = True
        return changed_anything

    def eliminate(self, copy):
        matrix = copy
        cols = len(matrix[0])
        for i in range(0, min(cols - 1, len(matrix))):
            for j in range(i, len(matrix)):
                if matrix[j][i] == 1:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
                elif matrix[j][i] == -1:
                    for k in range(len(matrix[j])):
                        matrix[j][k] *= -1
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            for j in range(0, len(matrix)):
                if j != i:
                    if matrix[j][i] == 1:
                        for elem in range(cols):
                            matrix[j][elem] -= matrix[i][elem]
                    elif matrix[j][i] == -1:
                        for elem in range(cols):
                            matrix[j][elem] += matrix[i][elem]

        return matrix

    def check_errors(self):
        not_clicked = self.game.find_elements_by_class_name("square.blank")
        for field in not_clicked:
            y, x = field.get_attribute("id").split("_")
            elem: Field
            elem = self.board[int(y)-1][int(x)-1]
            if elem.game_class == "square bombflagged":
                action_chains = ActionChains(self.driver)
                action_chains.context_click(self.game.find_element_by_id(elem.game_id)).perform()