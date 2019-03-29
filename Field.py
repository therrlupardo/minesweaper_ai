class Field:
    __isBomb = False        # pole jest bombą
    __bombNeighbours = 0    # ile bomb na sąsiednich polach
    __bombChance = 1.0      # szansa na obecność bomby na tym polu
    __x = 0                 # (x,y) - lokacja bomby na planszy
    __y = 0
    __gameId = ""
    __gameClass = ""
    __clicked = False

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__gameId = str(y+1)+"_"+str(x+1)

    def setBomb(self):
        self.__isBomb = True

    def setGameClass(self, gameClass:""):
        self.__gameClass = gameClass
        if gameClass != "square blank":
            self.__clicked = True
            print(gameClass)
            if gameClass == "square bombrevealed":
                print("BOMB DETECTED! YOU LOOSE!")
            elif gameClass == "square bombflagged":
                self.setBomb()
            elif gameClass == "square open0":
                self.__bombNeighbours = 0
            elif gameClass == "square open1":
                self.__bombNeighbours = 1
            elif gameClass == "square open2":
                self.__bombNeighbours = 2
            elif gameClass == "square open3":
                self.__bombNeighbours = 3
            elif gameClass == "square open4":
                self.__bombNeighbours = 4
            elif gameClass == "square open5":
                self.__bombNeighbours = 5
            elif gameClass == "square open6":
                self.__bombNeighbours = 6
            elif gameClass == "square open7":
                self.__bombNeighbours = 7
            elif gameClass == "square open8":
                self.__bombNeighbours = 8

    def getGameClass(self):
        return self.__gameClass

    def getGameId(self):
        return self.__gameId

    def __str__(self):
        if self.__isBomb:
            return "B"
        elif self.__clicked == False and self.__bombNeighbours == 0:
            return "-"
        else:
            return str(self.__bombNeighbours)
