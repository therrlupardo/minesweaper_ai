from math import floor
from Minesweeper.Board import Board
from Minesweeper.Field import Field
import time


class MatrixSolver:
    game_board: Board

    def __init__(self, game_board):
        self.game_board = game_board  # needed only if playing only this strategy

    def play(self):
        time0 = time.time()
        self.game_board.send_left_click(floor(self.game_board.height / 2), floor(self.game_board.width / 2))

        while self.matrix_method(self.game_board):
            self.game_board.update_fields()
            if self.game_board.game.find_element_by_id("face").get_attribute("class") == "facewin":
                break

        if self.game_board.mines_counter == 0:
            blanks = self.game_board.game.find_elements_by_class_name("square.blank")
            for elem in blanks:
                if elem.get_attribute("style") != "display: none;":
                    elem.click()

        return self.game_board.update_fields() and self.game_board.mines_counter == 0

    def matrix_method(self, game_board):
        changed_anything = False
        matrix = []
        matrix_columns = []
        # stwórz wektor pól, w których może być mina, które sąsiadują z polami ze znaną wartością
        for elem in game_board.neighbours_of_mines:
            for neighbour in elem.neighbours:
                if neighbour.game_class == "square blank":
                    if neighbour not in matrix_columns:
                        matrix_columns.append(neighbour)

        # uzupełnij macierz
        for elem in game_board.neighbours_of_mines:
            matrix_row = []
            for column in matrix_columns:
                if column in elem.neighbours:
                    matrix_row.append(1)
                else:
                    matrix_row.append(0)
            matrix.append(matrix_row)

        # stwórz wektor rozwiązań
        solutions = []
        for elem in game_board.neighbours_of_mines:
            value = 0
            for neighbour in elem.neighbours:
                if neighbour.game_class == "square bombflagged":
                    value += 1

            solutions.append(int(elem.mine_neighbours) - value)

        for i in range(len(matrix)):
            matrix[i].append(solutions[i])

        matrix = self.eliminate(matrix)

        for row in matrix:
            sum_abs = 0
            sum = 0
            for elem in row:
                sum_abs += abs(elem)
                sum += elem
            sum_abs -= abs(row[-1])
            sum -= row[-1]
            if sum_abs == abs(row[-1]):
                for i in range(len(row) - 1):
                    if row[i] != 0:
                        elem: Field = matrix_columns[i]
                        game_board.send_right_click(elem.y, elem.x)
                        changed_anything = True
            elif abs(sum) == sum_abs and row[-1] == 0:
                for i in range(len(row) - 1):
                    if row[i] != 0:
                        elem: Field = matrix_columns[i]
                        game_board.send_left_click(elem.y, elem.x)
                        changed_anything = True
        return changed_anything

    def eliminate(self, matrix):
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
