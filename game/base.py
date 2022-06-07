import random
import sys


class Signal:
    """A signal allows the train to be stopped on the current segment for ordering and preventing crashes."""

    def __init__(self):
        """
        Defines the default state of a signal as being red
        """
        self.status = 1

    def change_status(self):
        """
        Switches the status of the signal between on (1 = red light) and off (0 = green light)
        :return:
        """
        if self.status == 1:
            self.status = 0
        else:
            self.status = 1


class Weiche:
    """A switch that replaces a track segment and allows the train to move in different directions."""

    def __init__(self, alternative: str, default: str):
        """
        Initializes a switch that has two states. The default state is given by what the track would be if no switching
        would be allowed i.e. straight. The alternative state is always a directional state i.e. diagonally up and right.
        :param alternative:
        :param default:
        """
        self.status = default
        self.status_switched = alternative
        self.default = default

    def change_status(self):
        """
        Switches Status between the default state and the activated state
        :return: None
        """
        if self.status == self.default:
            self.status = self.status_switched
        else:
            self.status = self.default


class Stop:
    """A stop is defined as a station on the network."""

    def __init__(self, name: str):
        """
        Initializes the stop with a given name. The name can be used in downstream task to check if a train should be
        there.
        :param name:
        """
        self.name = name


class Zug:
    def __init__(self, start_x: int, start_y: int, direction: str, line: int, grid, stops: list[str],
                 delay: int = 0):
        """
        :param start_x:
        :param start_y:
        :param direction:
        :param grid:
        :param stops:
        :param delay:
        :return:
        """
        self.x = start_x
        self.y = start_y
        self.direction = direction
        self.grid = grid
        self.delay = delay
        self.step = self.grid.add_train_to_grid(self.x, self.y, self)
        self.stops = stops
        self.line_number = line

    def read_track(self):

        grid_symbol = self.grid.grid[self.y][self.x]

        if type(grid_symbol) == Weiche:
            grid_symbol = grid_symbol.status
        elif type(grid_symbol) == Signal:
            grid_symbol = grid_symbol.status
        elif type(grid_symbol) == Stop:
            grid_symbol = "10"
        # left / right horizontal
        if grid_symbol == "-":
            if self.direction == "<":
                new_x = self.x - 1
                new_y = self.y
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y
            elif self.direction == "^":
                new_x = self.x
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x
                new_y = self.y + 1

        # up / down vertical
        elif grid_symbol == "|":
            if self.direction == "^":
                new_x = self.x
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x
                new_y = self.y + 1
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y
            elif self.direction == "<":
                new_x = self.x - 1
                new_y = self.y

        # station / reward tile
        elif grid_symbol == "10":
            if self.direction == "^":
                new_x = self.x
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x
                new_y = self.y + 1
            elif self.direction == "<":
                new_x = self.x - 1
                new_y = self.y
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y

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

        # curve right
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

        elif grid_symbol == 1:  # Signal == rot
            new_x = self.x
            new_y = self.y
            self.delay += 0.5
        elif grid_symbol == 0:  # Signal == grün
            if self.direction == "^":
                new_x = self.x
                new_y = self.y - 1
            elif self.direction == "v":
                new_x = self.x
                new_y = self.y + 1
            elif self.direction == "<":
                new_x = self.x - 1
                new_y = self.y
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y

        reward = min(round(10 - self.delay ** 1.5, 1), 10) if grid_symbol == "10" else 0

        return new_x, new_y, reward, self

    def move(self, new_x, new_y):
        self.grid.train_grid[self.y][self.x] = 0
        self.grid.train_grid[new_y][new_x] = self

        self.x = new_x
        self.y = new_y

        self.step += 1


class Grid:
    """The schematic of Mannheim's central metro system. It is simplified into a gridworld and slightly altered."""

    def __init__(self):
        """
        Initializes all grid components with automatically generated components. Also sets the world steps to 0 as
        initial value.
        """
        self.grid = None
        self.signal_grid = None
        self.switch_grid = None
        self.train_grid = None
        self.step = 0
        self.init_grid()

    def init_grid(self):
        """
        Sets all grids to their respective default.

        :param: grid
        The grid is defined as a 2-dimensional list of element.
        A empty spot where no tracks exist is represented as 0. Vertical tracks - allowing vertical travel are
        represented by the string |.
        Horizontal tracks are given by '-'. Diagonal travel is represented by either \\ or /.
        Signals, stops and switches are integrated as objects of their respective data types.

        :param: train_grid
        The train grid is used to track the individual train objects on their path through the tracks. It has to be off
        the same dimensionality as the default grid.

        :return: None
        """
        self.grid = [  # Ausfahrt Kurpfalzbrücke
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Weiche('/', '|'), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, '/', '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-',
             '|', '|',
             Weiche('/', '-'), Signal(), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', 0, 0, 0, 0, 0, 0, 0],
            [0, 0, '|', 0, '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-',
             '|', '|',
             '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', '\\', 0, 0, 0, 0, 0, 0],
            [0, 0, '|', '/', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '\\', '\\', 0, 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, '\\', '\\', 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, '|', Weiche('/', '|'), Weiche('\\', '-'), Signal(), '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, '|', '|', '-', '-', '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, '|', Weiche('/', '|'), 0, 0, 0, 0],
            ['-', '-', Weiche('\\', '-'), '-', Weiche('\\', '-'), Signal(), '-', Stop(""), '-', '-', '-', Stop(""), '-',
             '-', '-', '-', '-', '-', '-', Weiche('\\', '|'), '|', Weiche('\\', '-'), Signal(), '-', Stop(""), '-', '-',
             '-', '-', '-', '-', Stop(""), '-', '-', '|', Signal(), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            ['-', Signal(), '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-',
             Signal(), '|', '|', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', Stop(""), '-', '-', '|',
             Weiche('\\', '|'), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Signal(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, Signal(), Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             Weiche('\\', '|'), Weiche('/', '|'), Weiche('\\', '-'), Signal(), Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', '-', '-', Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Weiche('/', '|'), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '/', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '\\', 0, '\\', '-', '-', Weiche('/', '-'),
             Signal(), '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), 0, '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-', Signal(), Weiche('\\', '-'), '-',
             Weiche('\\', '-'), '-', '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), '/', 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Weiche('/', '-'), 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Stop(""), Signal(), 0, 0, 0, 0, 0, 0,
             0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0]
        ]
        self.train_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0]
        ]

    def add_train_to_grid(self, x: int, y: int, train: Zug):
        """
        Adds a train based on initial coordinates into the world by adding it to the train_grid. It has no logic to check
        if a train already occupies the coordinate.
        :param x: integer between 0 and the length of a grid row
        :param y: integer between 0 and the height of the grid
        :param train: train object that is to be placed
        :return: current grid step
        """
        self.train_grid[y][x] = train
        return self.step

    def update_train(self, *args):
        """
        Recursive function to update all subsequent trains. It checks if there is a train object on the proposed new
        coordinate, and it already moved on this grid step. If it hasn't moved the function update_train is called for
        this train. The exit conditions are either there being no train on the track segment where the original train
        object wants to move to or the train on the tile "ahead" already moved this step.
        :param args: new x & y value of the train, the calculated reward in move function and the train object
        :return: float reward
        """
        # list unpacking of args
        new_x, new_y, reward, tile = args[0]
        # calculates the new position of the train
        expected_new_tile = self.train_grid[new_y][new_y]

        # check which condition applies to the new position
        # Condition 1: Train on new position that hasn't moved on this step
        if type(expected_new_tile) == Zug and expected_new_tile.step != self.step:
            # recursive call for the train on new position
            reward += self.update_train(expected_new_tile)
            # move the original out of recursion train
            expected_new_tile.move(new_x, new_y)
            return reward
        # Condition 2: Train on new position that has already moved this step
        elif type(expected_new_tile) == Zug and expected_new_tile.step == self.step:
            return -1
        # Condition 3: Nothing on the new position
        else:
            tile.move(new_x, new_y)
            return 0

    def update_world(self):
        self.step += 1
        reward = 0
        for row in self.train_grid:
            for tile in row:
                if type(tile) == Zug and tile.step != self.step:
                    reward = 0 + self.update_train(tile.read_track())
        return reward

    def update_signal_switches(self, action_list):
        """
        Uses a list of 0 and 1s to switch the respective signal or switch. The list is split by index: The first half
        is used for signals and the second half is used for switches. In the default grid there are 18 signals and 18
        switches.
        :param action_list: list of 36 binary integers
        :return:
        """
        amount_switches = 0
        amount_signals = 0

        # iterate over all rows in the grid
        for row in self.grid:
            # iterate over all items in the row
            for item in row:
                # if the item is a signal
                if type(item) == Signal:
                    # check if it's supposed to be changed
                    if action_list[amount_signals] == 1:
                        # change the item's status
                        item.change_status()
                    amount_signals += 1
                # if the item is a switch
                elif type(item) == Weiche:
                    # check if it's supposed to be changed
                    if action_list[16 + amount_switches] == 1:
                        # change the item's status
                        item.change_status()
                    amount_switches += 1

    def __str__(self):
        """
        Alternative print function to enable a proper view into the grid world.
        :return: fancy output string
        """
        output = ""
        # iterate over all rows
        for y, row in enumerate(self.grid):
            # iterate over all elements in the row
            for x, col in enumerate(row):
                # if there is no train on the grid coordinate look into the normal grid
                if self.train_grid[y][x] == 0:
                    if col == 0:
                        output += "  "
                    elif col in ["-", "|", "/"]:
                        output += 2 * col
                    elif col == "\\":
                        output += col * 2
                    elif type(col) == Signal:
                        output += "S" + str(col.status)
                    elif type(col) == Weiche:
                        output += "W" + col.status_switched
                    elif type(col) == Stop:
                        output += "SP"  # col.name[:2]
                # if there is a train on this grid coordinate print the train instead
                else:
                    output += "<" + str(self.train_grid[y][x].line_number)
            output += "\n"
        return output


def create_line(line_number: int, reverse: bool, grid: Grid):
    """
    Creates a train line based on the line number and its tracking direction.
    :param line_number:
    :param reverse:
    :param grid:
    :return:
    """
    delay = random.randint(0, 3)
    if line_number == 1:
        stops = ["T", "B", "U", "P", "M", "A"]
        if reverse is False:
            line = Zug(start_x=39, start_y=13, direction="<", grid=grid, stops=stops, delay=delay, line=1)
        else:
            line = Zug(start_x=19, start_y=0, direction="v", grid=grid, stops=stops, delay=delay, line=1)
    return line


def step(grid, actions, *args):
    if grid.step % 10 == 0:
        trains.append(create_line(1, False, grid))
    reward = grid.update_world()
    print(f"Step: {grid.step}, {reward}")
    print(grid)
    # grid.update_signal_switches()
    return grid.grid, reward, False


if __name__ == "__main__":
    gridworld = Grid()
    trains = list()
    for i in range(1):
        step(gridworld, None)
