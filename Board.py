import time

from selenium.webdriver.firefox.webdriver import WebDriver
from Field import Field

class Board:
    __height = 0
    __width = 0
    __board = []
    __game: WebDriver
    __field_values = ["square open0", "square open1", "square open2", "square open3", "square open4", "square open5",
                      "square open6", "square open7", "square open8", "square bombflagged", "square bombrevealed"]

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

        for name in self.__field_values:
            fields = self.__game.find_elements_by_class_name(name.replace(' ', '.'))
            if name == "square bombsrevealed" and fields.size() != 0:
                return False
            for field in fields:
                field_id = field.get_attribute("id")
                y, x = field_id.split("_")
                elem = self.__board[int(y)-1][int(x)-1]
                if (elem.getGameClass() != name):
                    elem.setGameClass(name)
        print(time.time() - time0)

    def sendClick(self, y, x):
        elem:Field = self.__board[y][x]
        self.__game.find_element_by_id(elem.getGameId()).click()
        return self.updateFields()