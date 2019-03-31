import time

from selenium import webdriver

from Solvers.LogicSolver import LogicSolver
from Solvers.SimpleSolver import SimpleSolver


class BrowserHandler:
    def __init__(self):
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

        logic_solver = LogicSolver(driver, game, height, width, mines_counter)
        # simple_solver = SimpleSolver(driver, game, height,width,mines_counter)
        # matrix_solver = SimpleSolver(driver, game, height,width,mines_counter)

        if logic_solver.play():
            wins += 1
        else:
            print("YOU LOST")
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
