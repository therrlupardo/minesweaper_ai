class Field:

    def __init__(self, x, y):
        # (x,y) - lokacja miny na planszy
        self.x = x
        self.y = y

        # pole jest mina
        self.is_mine = False

        # ile min na sąsiednich polach
        self.mine_neighbours: int = 0

        # szansa na obecność miny na tym polu
        # self.is_mine_chance = 0.0

        self.game_id = str(y + 1) + '_' + str(x + 1)
        self.game_class = 'square blank'
        self.clicked = False
        self.neighbours_solved = False
        self.neighbours = []

    def set_mine(self):
        self.is_mine = True

    def set_game_class(self, game_class: ""):
        self.game_class = game_class
        if game_class != 'square blank':
            self.clicked = True

            # self.mine_neighbours = {
            #     'square bombrevealed': 'M',
            #     'square bombflagged': 'F',
            #     'square open0': 0,
            #     'square open1': 1,
            #     'square open2': 2,
            #     'square open3': 3,
            #     'square open4': 4,
            #     'square open5': 5,
            #     'square open6': 6,
            #     'square open7': 7,
            #     'square open8': 8,
            # }[game_class]

            self.mine_neighbours = {
                'square bombrevealed': 11,
                'square bombflagged': 10,
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

            if self.mine_neighbours == 10:
                self.set_mine()

    def __str__(self):
        # if self.is_mine:
        #       return 'M'
        # elif self.clicked is False and self.mine_neighbours == 0:
        #     return '-'

        if self.clicked is False and self.mine_neighbours == 0:
            # gdy game_class == 'square blank' (moze dodac
            # mine_neighbours = 9
            # w inicie?)
            # wtedy return str(self.mine_neighbours)
            return '9'
        else:
            return str(self.mine_neighbours)
