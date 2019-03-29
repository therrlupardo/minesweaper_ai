import time

from selenium.webdriver.firefox.webdriver import WebDriver
from Field import Field

class Board:
    __height = 0
    __width = 0
    __board = []
    __game: WebDriver

    def __init__(self, game: WebDriver, height, width):
        self.__game = game
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Field(j, i))
            self.__board.append(row)

    def print(self):
        for row in self.__board:
            for elem in row:
                print(elem, end=" ")
            print()

    def updateFields(self):
        time0 = time.time()
        for row in self.__board:
            for elem in row:
                elemClass = self.__game.find_element_by_id(elem.getGameId()).get_attribute('class')
                if elem.getGameClass() != elemClass:
                    elem.setGameClass(elemClass)
        print(time.time() - time0)

    def sendClick(self, y, x):
        elem:Field = self.__board[y][x]
        self.__game.find_element_by_id(elem.getGameId()).click()
        self.updateFields()