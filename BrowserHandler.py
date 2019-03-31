import time

from selenium import webdriver
from SimpleSolver import SimpleSolver


class BrowserHandler:
    def __init__(self):
        driver = webdriver.Firefox()
        driver.get("http://minesweeperonline.com")
        # driver.get("http://minesweeperonline.com/#beginner")
        assert "Minesweeper Online" in driver.title

        game = driver.find_element_by_id("game")
        height = int(len(game.find_elements_by_class_name('borderlr')) / 2)
        width = int(len(game.find_elements_by_class_name('bordertb')) / 3)

        mines_counter = int(game.find_element_by_id("mines_hundreds").get_attribute("class")[-1]) * 100
        mines_counter += int(game.find_element_by_id("mines_tens").get_attribute("class")[-1]) * 10
        mines_counter += int(game.find_element_by_id("mines_ones").get_attribute("class")[-1])

        simple_solver = SimpleSolver(driver, game, height, width, mines_counter)
        simple_solver.game_board.print()
        print()

        if simple_solver.play():
            print("YOU WON!")
        else:
            print("YOU LOST")

        simple_solver.game_board.print()

        time.sleep(10.0)
        driver.close()
