import time

from selenium import webdriver

from Solvers.LogicSolver import LogicSolver
from Solvers.ProbabilitySolver import ProbabilitySolver
from Solvers.SimpleSolver import SimpleSolver


class BrowserHandler:
    def __init__(self):
        wins = 0
        games = 20

        driver = webdriver.Firefox()
        driver.get("http://minesweeperonline.com/#beginner")
        # driver.get("http://minesweeperonline.com/#intermediate")
        # driver.get("http://minesweeperonline.com")
        assert "Minesweeper Online" in driver.title

        for i in range(games):
            game = driver.find_element_by_id('game')
            height = int(len(game.find_elements_by_class_name('borderlr')) / 2)
            width = int(len(game.find_elements_by_class_name('bordertb')) / 3)

            mines_counter = self.count_mines(game)

            logic_solver = LogicSolver(driver, game, height, width, mines_counter)

            if logic_solver.play():
                wins += 1
                # print("1")
            # else:
            #     print("0")

            time.sleep(2.0)
            print(str(i + 1) + ". test - winrate: " + str(wins / (i + 1) * 100) + "%")
            # driver.refresh()
            driver.find_element_by_id('face').click()

            # dla pewnosci
            if self.page_has_loaded(driver):
                continue

        driver.close()
        print('Winrate: ' + str(wins / games * 100) + '%')

    @staticmethod
    def page_has_loaded(driver):
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    @staticmethod
    def count_mines(game):
        mines_counter = int(game.find_element_by_id('mines_hundreds').get_attribute('class')[-1]) * 100
        mines_counter += int(game.find_element_by_id('mines_tens').get_attribute('class')[-1]) * 10
        mines_counter += int(game.find_element_by_id('mines_ones').get_attribute('class')[-1])
        return mines_counter
