import sys


class Signal:
    def __init__(self):
        self.status = 1

    def change_status(self):
        if self.status == 1:
            self.status = 0
        else:
            self.status = 1


class Switch:
    def __init__(self, alternative):
        self.status = 0
        self.status_switched = alternative

    def change_status(self):
        if self.status == 0:
            self.status = self.status_ausschlag
        else:
            self.status = 0


class Grid:
    def __init__(self):
        self.grid = None
        self.signal_grid = None
        self.switch_grid = None
        self.init_grid()

    def init_grid(self):
        self.grid = grid_poc = [  # Ausfahrt Kurpfalzbrücke
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, "/", "-", 10, "-", "-", 10, "-", "-", "-", 10, "-", "-", "-", "-", "-", "|", "|", "-", "-",
             "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, "/", "/", "-", 10, "-", "-", 10, "-", "-", "-", 10, "-", "-", "-", "-", "-", "|", "|", "-", "-",
             "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", "\\", 0, 0, 0, 0, 0, 0],
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "\\", "\\", 0, 0, 0, 0, 0],
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, "\\", "\\", 0, 0, 0, 0],
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, "|", "|", "-", "-", "-", "-"],  # Ausfahrt Nationaltheater
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, "|", "|", "-", "-", "-", "-"],  # Ausfahrt Nationaltheater
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, "|", "|", 0, 0, 0, 0],
            [0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, "|", "|", 0, 0, 0, 0],
            ["-", "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", "-", "|", "|", "-",
             "-", "-", 10, "-", "-", "-", "-", "-", "-", 10, "-", "-", "|", "|", 0, 0, 0, 0],  # Ausfahrt Handelshafen
            ["-", "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", 10, "-", "-", "-", "-", "-", "-", "-", "|", "|", "-",
             "-", "-", 10, "-", "-", "-", "-", "-", "-", 10, "-", "-", "|", "|", 0, 0, 0, 0],  # Ausfahrt Handelshafen
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", "-", "-", "-", "-"],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", "-", "-", "-", "-"],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "|", "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             "/", "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "\\", 0, "\\", "-", "-", "-", "-", "-", 10, "-",
             "-", "-", "-", "-", 10, 0, "|", 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-", "-", "-", "-", "-", "-", "-", 10, "-",
             "-", "-", "-", "-", 10, "/", 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "|", "|", 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0]
        ]  # Ausfahrt K-A-Brücke (LU)
        self.signal_grid = [[]]


class Zug:
    def __int__(self, start_x:int, start_y:int, direction:str, grid:Grid, delay:int=0):
        super().__init__()
        self.x = start_x
        self.y = start_y
        self.direction = direction
        self.grid = grid
        self.delay = delay

    def move(self):
        grid_symbol = self.grid[self.y][self.x]
        # left / right horizontal
        if grid_symbol == "-":
            if self.direction == "<":
                new_x = self.x - 1
            elif self.direction == ">":
                new_x = self.x + 1

        # up / down vertical
        elif grid_symbol == "|":
            if self.direction == "^":
                new_y = self.y - 1
            elif self.direction == "v":
                new_y = self.y + 1

        # station / reward tile
        elif grid_symbol == "10":
            if self.direction == "^":
                new_y = self.y - 1
            elif self.direction == "v":
                new_y = self.y + 1
            elif self.direction == "<":
                self. x -= 1
            elif self.direction == ">":
                new_x = self.x + 1
            reward = min(10-self.delay, 10)

        # curve left
        elif grid_symbol == "/":
            if self.direction == "<":
                new_x = self.x - 1
                new_y = self.y + 1
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y - 1
            elif self.direction == "^":
                new_x = self.x + 1
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x - 1
                new_y = self.y - 1

        #curve right
        elif grid_symbol == "\\":
            if self.direction == "<":
                new_x = self.x - 1
                new_y = self.y - 1
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y + 1
            elif self.direction == "^":
                new_x = self.x - 1
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x + 1
                new_y = self.y + 1

    
    
