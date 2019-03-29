import time

from selenium import webdriver
from Board import Board

def send_some_clicks(board):
    for i in range(29):
        if board.send_click(0, i) == False:
            board.print()
            return False
        board.print()
    return True

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

    if send_some_clicks(board):
        print("YOU WON!")
    else:
        print("YOU LOST")

    time.sleep(10.0)
    driver.close()
