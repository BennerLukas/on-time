from base import Grid
from helper import Switch, Signal, Stop

class Train:
    def __init__(self, start_x: int, start_y: int, direction: str, line: int, grid: Grid, switches: list[str],
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
