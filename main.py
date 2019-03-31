import time
import numpy as np
from selenium import webdriver
from Board import Board

# def eliminate( copy):
#     matrix = copy
#     cols = len(matrix[0])
#     print(np.array(matrix))
#     for i in range(0, min(cols - 1, len(matrix))):
#         found = False
#         while not found:
#             print()
#             print("Next loop")
#             for j in range(i, len(matrix)):
#                 print(matrix[j])
#                 print(matrix[j][i], i, j)
#                 if matrix[j][i] == 1:
#                     print("swap r[",i+1,"], r[",j+1,"]")
#                     matrix[i], matrix[j] = matrix[j], matrix[i]
#                     found = True
#                     break
#                 elif matrix[j][i] == -1:
#                     print("r[",j+1,"] * -1")
#                     for k in range(len(matrix[j])):
#                         matrix[j][k] *= -1
#                     print("swap r[",i+1,"], r[",j+1,"]")
#                     matrix[i], matrix[j] = matrix[j], matrix[i]
#                     found = True
#                     break
#             if not found:
#                 i += 1
#                 print("go next")
#         for j in range(0, len(matrix)):
#             if j != i:
#                 if matrix[j][i] == 1:
#                     print("r[",j+1,"] - r[",i+1,"]")
#                     for elem in range(cols):
#                         matrix[j][elem] -= matrix[i][elem]
#                 elif matrix[j][i] == -1:
#                     print("r[",j+1,"] + r[",i+1,"]")
#                     for elem in range(cols):
#                         matrix[j][elem] += matrix[i][elem]
#
#         print(np.array(matrix))
#         print()
#     return matrix


if __name__ == "__main__":

    wins = 0

    # for i in range(10000):

    driver = webdriver.Firefox()

    # driver.get("http://minesweeperonline.com/#beginner")
    # driver.get("http://minesweeperonline.com/#intermediate")
    driver.get("http://minesweeperonline.com")

    assert "Minesweeper Online" in driver.title

    game = driver.find_element_by_id("game")
    height = int(len(game.find_elements_by_class_name('borderlr')) / 2)
    width = int(len(game.find_elements_by_class_name('bordertb')) / 3)

    mines_counter = int(game.find_element_by_id("mines_hundreds").get_attribute("class")[-1]) * 100
    mines_counter += int(game.find_element_by_id("mines_tens").get_attribute("class")[-1]) * 10
    mines_counter += int(game.find_element_by_id("mines_ones").get_attribute("class")[-1])

    board = Board(driver, game, height, width, mines_counter)

    if board.play():
        wins += 1

    # board.print()

    time.sleep(20.0)
    driver.close()
    #
    # matrix = [[1,1,0,0,0,0,1],
    #           [1,1,1,0,0,0,1],
    #           [1,1,1,0,0,1,1],
    #           [0,0,0,0,1,1,1],
    #           [0,0,0,1,1,0,1]]
    #
    # print(np.array(eliminate(matrix)))

    # print("Won:", wins," /10000 games!")
