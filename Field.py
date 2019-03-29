class Field:
    __is_mine = False       # pole jest mina
    __mine_neighbours = 0   # ile min na sąsiednich polach
    __is_mine_chance = 1.0  # szansa na obecność miny na tym polu
    __x = 0                 # (x,y) - lokacja miny na planszy
    __y = 0
    __game_id = ""
    __game_class = ""
    __clicked = False

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__game_id = str(y + 1) + "_" + str(x + 1)

    def set_mine(self):
        self.__is_mine = True

    def set_game_class(self, game_class: ""):
        self.__game_class = game_class
        if game_class != "square blank":
            self.__clicked = True

            self.__mine_neighbours = {
                'square bombrevealed' : 'M',
                'square bombflagged': 'F',
                'square open0': 0,
                'square open1': 1,
                'square open2': 2,
                'square open3': 3,
                'square open4': 4,
                'square open5': 5,
                'square open6': 6,
                'square open7': 7,
                'square open8': 8,
            }[game_class]

            if self.__mine_neighbours == 'F':
                self.set_mine()

    def get_game_class(self):
        return self.__game_class

    def get_game_id(self):
        return self.__game_id

    def __str__(self):
        if self.__is_mine:
            return "M"
        elif self.__clicked is False and self.__mine_neighbours == 0:
            return "-"
        else:
            return str(self.__mine_neighbours)
