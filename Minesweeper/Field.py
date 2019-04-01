class Field:
    is_mine = False  # pole jest mina
    mine_neighbours: int = 0  # ile min na sąsiednich polach
    is_mine_chance = 0.0  # szansa na obecność miny na tym polu
    x = 0  # (x,y) - lokacja miny na planszy

    y = 0
    game_id = ""
    game_class = ""
    clicked = False
    neighbours_solved = False
    neighbours = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.game_id = str(y + 1) + "_" + str(x + 1)
        self.game_class = "square blank"

    def set_mine(self):
        self.is_mine = True

    def set_game_class(self, game_class: ""):
        self.game_class = game_class
        if game_class != "square blank":
            self.clicked = True

            self.mine_neighbours = {
                'square bombrevealed': 'M',
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

            if self.mine_neighbours == 'F':
                self.set_mine()

    def __str__(self):
        if self.is_mine:
            return "M"
        elif self.clicked is False and self.mine_neighbours == 0:
            return "-"
        else:
            return str(self.mine_neighbours)
