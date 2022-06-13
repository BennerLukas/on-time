import random
import time
from collections import deque
import sys


# TODO: Signal-Cluster (Kreuzungen) --> Observation Space: Signal-Cluster 1: {1: 5, 2: -1, 3: None}
#                                      Action Space: Signal-Cluster 1: [1,2] => 1: Signal oben grün, Signal rechts rot
# TODO: Maybe fancier console update


class Signal:
    """A signal allows the train to be stopped on the current segment for ordering and preventing crashes."""

    def __init__(self):
        """
        Defines the default state of a signal as being red
        """
        self.status = 0

    def change_status(self):
        """
        Switches the status of the signal between on (1 = red light) and off (0 = green light)
        :return:
        """
        if self.status == 1:
            self.status = 0
        else:
            self.status = 1


class Switch:
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

    def change_status(self, status_updated):
        """
        Switches Status between the default state and the activated state
        :param status_updated: new state for switch, is validated against base values
        :return: None
        """
        if status_updated not in [self.default, self.status_switched]:
            raise Exception(f"Switch forced to switch to wrong status! Was given {status_updated} but can only accept "
                            f"{self.default, self.status_switched}")
        self.status = status_updated


class Stop:
    """A stop is defined as a station on the network."""

    def __init__(self, name: str):
        """
        Initializes the stop with a given name. The name can be used in downstream task to check if a train should be
        there.
        :param name:
        """
        self.name = name


class Train:
    def __init__(self, start_x: int, start_y: int, direction: str, line: int, grid, switches: list[str],
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
        self.switches = switches
        self.line_number = line

    def read_track(self):

        grid_symbol = self.grid.grid[self.y][self.x]

        if type(grid_symbol) == Switch:
            grid_symbol.change_status(self.switches.popleft())
            print(self.y, self.x)
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
            direction = self.direction

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
            direction = self.direction

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
            self.delay += random.randint(0, 2)
            direction = self.direction

        # curve left
        elif grid_symbol == "/":
            if self.direction == "<":
                new_x = self.x - 1
                new_y = self.y + 1
                direction = "v"
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y - 1
                direction = "^"
            elif self.direction == "^":
                new_x = self.x + 1
                new_y = self.y - 1
                direction = ">"
            elif self.direction == "v":
                new_x = self.x - 1
                new_y = self.y + 1
                direction = "<"

        # curve right
        elif grid_symbol == "\\":
            if self.direction == "<":
                new_x = self.x - 1
                new_y = self.y - 1
                direction = "^"
            elif self.direction == ">":
                new_x = self.x + 1
                new_y = self.y + 1
                direction = "v"
            elif self.direction == "^":
                new_x = self.x - 1
                new_y = self.y - 1
                direction = "<"
            elif self.direction == "v":
                new_x = self.x + 1
                new_y = self.y + 1
                direction = ">"

        elif grid_symbol == 1:  # Signal == rot
            new_x = self.x
            new_y = self.y
            self.delay += 1
            direction = self.direction
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
            direction = self.direction

        if grid_symbol == "10":
            reward = min(round(10 - (abs(1 / 3 * self.delay ** 3) + abs(5 / 8 * self.delay)), 1), 10)
        else:
            reward = 0

        return new_x, new_y, direction, reward, self

    def move(self, new_x, new_y, new_direction):
        self.grid.train_grid[self.y][self.x] = 0
        self.grid.train_grid[new_y][new_x] = self

        self.x = new_x
        self.y = new_y
        self.direction = new_direction

        print(f"Train {self.line_number} \n From {new_x} | {new_y} to {self.x} | {self.y}")

        self.step += 1


class Grid:
    """The schematic of Mannheim's central metro system. It is simplified into a gridworld and slightly altered."""

    def __init__(self):
        """
        Initializes all grid components with automatically generated components. Also sets the world steps to 0 as
        initial value.
        """
        self.grid = None
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Switch('/', '|'), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, '/', '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-',
             '|', Switch('/', '|'), Signal(), '-', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', 0, 0, 0, 0, 0,
             0, 0],
            [0, 0, '|', 0, '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', Signal(),
             Switch('/', '-'), '|', '|', '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '\\', '\\',
             0, 0, 0, 0, 0, 0],
            [0, 0, '|', '/', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Switch("/", "|"), 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0,
             '\\', '\\', 0, 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Signal(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0,
             0, Signal, '\\', 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, Switch('\\', '|'), Switch('/', '|'), Switch('\\', '-'), Signal(), '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, '|', '|', '-', '-', '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, Switch('/', '|'), Switch('/', '|'), 0, 0, 0, 0],
            ['-', '-', Switch('\\', '-'), '-', Switch('\\', '-'), Signal(), '-', Stop(""), '-', '-', '-', Stop(""), '-',
             '-', '-', '-', '-', '-', '-', Switch('\\', '|'), '|', Switch('\\', '-'), Signal(), '-', Stop(""), '-', '-',
             '-', '-', '-', '-', Stop(""), '-', '-', '|', Signal(), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            ['-', Signal(), '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-',
             Signal(), '|', '|', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', Stop(""), Signal(),
             Switch("\\", "-"), Switch('/', '|'),
             Switch('\\', '|'), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Signal(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, Signal(), Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             Switch('\\', '|'), Switch('/', '|'), Switch('\\', '-'), Signal(), Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', '-', '-', Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Switch('/', '|'), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '/', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '\\', 0, '\\', '-', '-', Switch('/', '-'),
             Signal(), '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), 0, '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-', Signal(), Switch('\\', '-'), '-',
             Switch('\\', '-'), '-', '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), '/', 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Switch('/', '-'), 0, 0, 0, 0, 0,
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

    def add_train_to_grid(self, x: int, y: int, train: Train):
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

        if type(args[0]) == tuple:
            # list unpacking of args
            new_x, new_y, new_direction, reward, tile = args[0]
        else:
            new_x, new_y, new_direction, reward, tile = args[0].read_track()

        # check if train goes out-of-bounds and deletes it
        if new_x > 39 or new_x < 0 or new_y < 0 or new_y > 23:
            # remove train from train_grid
            tile.grid.train_grid[tile.y][tile.x] = 0
            # delete train object
            del tile
            return reward
        else:
            # calculates the new position of the train
            expected_new_tile = self.train_grid[new_y][new_x]

        # check which condition applies to the new position
        # Condition 1: Train on new position that hasn't moved on this step
        if type(expected_new_tile) == Train and expected_new_tile.step != self.step:
            # recursive call for the train on new position
            reward += self.update_train(expected_new_tile)
            # move the original out of recursion train
            expected_new_tile.move(new_x, new_y, new_direction)
            return reward
        # Condition 2: Train on new position that has already moved this step
        elif type(expected_new_tile) == Train and expected_new_tile.step == self.step:
            return reward - 1
        # Condition 3: Nothing on the new position
        else:
            tile.move(new_x, new_y, new_direction)
            return reward + 0

    def update_world(self):
        self.step += 1
        reward = 0
        for row in self.train_grid:
            for tile in row:
                if type(tile) == Train and tile.step != self.step:
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
                elif type(item) == Switch:
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
                    elif type(col) == Switch:
                        output += "W" + col.status_switched
                    elif type(col) == Stop:
                        output += "SP"  # col.name[:2]
                # if there is a train on this grid coordinate print the train instead
                else:
                    output += str(self.train_grid[y][x].line_number) + self.train_grid[y][x].direction
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
    delay = random.randint(-3, 3)
    if line_number == 1:
        if reverse is False:
            # from TAT
            switches = deque(["-", "/", "-", "|", "|"])
            line = Train(start_x=39, start_y=13, direction="<", grid=grid, switches=switches, delay=delay, line=1)
        else:
            # from KUB
            switches = deque(["|", "|", "-", "-", "/"])
            line = Train(start_x=19, start_y=0, direction="v", grid=grid, switches=switches, delay=delay, line=1)

    elif line_number == 2:
        if reverse is False:
            # from NAT
            switches = deque(["-", "/", "/", "-", "-", "\\", "/"])
            line = Train(start_x=39, start_y=8, direction="<", grid=grid, switches=switches, delay=delay, line=2)
        else:
            # from KUB
            switches = deque(["/", "\\", "-", "/", "/"])
            line = Train(start_x=19, start_y=0, direction="v", grid=grid, switches=switches, delay=delay, line=2)

    # Line 3 skipped because of grid architecture

    elif line_number == 4:
        if reverse is False:
            # from KAB
            switches = deque(["/", "|", "|", "\\", "\\", "|", "|"])
            line = Train(start_x=24, start_y=23, direction="^", grid=grid, switches=switches, delay=delay, line=4)
        else:
            # from KUB
            switches = deque(["|", "|", "\\"])
            line = Train(start_x=19, start_y=0, direction="v", grid=grid, switches=switches, delay=delay, line=4)

    elif line_number == 5:
        if reverse is False:
            # from KUB
            switches = deque(["|", "|", "|", "-", "-", "|", "|", "|", "/"])
            line = Train(start_x=19, start_y=0, direction="v", grid=grid, switches=switches, delay=delay, line=5)
        else:
            # from NAT
            switches = deque(["-", "/", "|", "|", "|", "-", "|"])
            line = Train(start_x=39, start_y=8, direction="<", grid=grid, switches=switches, delay=delay, line=5)

    elif line_number == 6:
        if reverse is False:
            # from TAT
            switches = deque(["\\", "\\", "-", "|", "-", "-", "-"])
            line = Train(start_x=39, start_y=13, direction="<", grid=grid, switches=switches, delay=delay, line=6)
        else:
            # from HHF
            switches = deque(["\\", "\\"])
            line = Train(start_x=0, start_y=11, direction=">", grid=grid, switches=switches, delay=delay, line=6)

    elif line_number == 7:
        if reverse is False:
            # from NAT
            switches = deque(["\\", "/", "|", "|", "\\"])
            line = Train(start_x=39, start_y=8, direction="<", grid=grid, switches=switches, delay=delay, line=7)
        else:
            # from KAB
            switches = deque(["|", "\\", "/", "\\"])
            line = Train(start_x=24, start_y=23, direction="^", grid=grid, switches=switches, delay=delay, line=7)

    else:
        raise NotImplemented("Line number is not implemented! Only lines 1,2,4,5,6,7 are implemented.")

    return line


def step(grid, actions, *args):
    if grid.step % 10 == 0:
        pass

    elif grid.step % 10 == 1:
        trains.append(create_line(6, False, grid))

    elif grid.step % 120 == 2:
        trains.append(create_line(4, False, grid))
        trains.append(create_line(4, True, grid))

    elif grid.step % 120 == 3:
        trains.append(create_line(1, True, grid))

    elif grid.step % 120 == 4:
        trains.append(create_line(1, False, grid))

    elif grid.step % 10 == 8:
        trains.append(create_line(2, True, grid))
        trains.append(create_line(7, True, grid))

    elif grid.step % 10 == 9:
        trains.append(create_line(6, True, grid))

    reward = grid.update_world()
    print(f"Step: {grid.step}, {reward}")
    print(grid)
    # grid.update_signal_switches()
    return grid.grid, reward, False


if __name__ == "__main__":
    gridworld = Grid()
    trains = list()
    for i in range(80):
        step(gridworld, None)
        time.sleep(.5)
