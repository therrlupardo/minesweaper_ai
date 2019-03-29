import time

from selenium import webdriver
from Board import Board


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("http://minesweeperonline.com")
    assert "Minesweeper Online" in driver.title

    game = driver.find_element_by_id("game")
    height = int(len(game.find_elements_by_class_name('borderlr')) / 2)
    width = int(len(game.find_elements_by_class_name('bordertb')) / 3)

    board = Board(game, height, width)
    board.print()
    print()
    board.updateFields()
    board.sendClick(0, 0)
    board.print()

    board.sendClick(0, 29)
    board.print()
    time.sleep(10.0)
    driver.close()