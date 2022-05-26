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
        self.train_grid = None
        self.step = 0
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
        ]
        self.signal_grid = [[]]
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
             0, 0, 0, 0]
        ]

    def add_train_to_grid(self, x, y, train):
        self.train_grid[y][x] = train
        return self.step

    def update_train(self, *args):
        new_x, new_y, reward = args
        expected_new_tile = self.train_grid[new_y][new_y]
        if type(expected_new_tile) == Zug and expected_new_tile.step != self.step:
            reward += self.update_train(expected_new_tile)
            expected_new_tile.move(new_x, new_y)
            return reward
        elif type(expected_new_tile) == Zug and expected_new_tile.step == self.step:
            return -1
        else:
            return 0

    def update_world(self):
        self.step += 1
        for tile in self.train_grid:
            if type(tile) == Zug and tile.step != self.step:
                reward = reward + self.update_train(tile.read_track())
        return reward

    def change_world_state(self, action_list):
        for i in action_list:
            if self.switch_grid[i.get("x")][i.get("y")].status != i.get("status"):
                self.switch_grid[i.get("x")][i.get("y")] = self.switch_grid[i.get("x")][i.get("y")].change_status


class Zug:
    def __int__(self, start_x: int, start_y: int, direction: str, grid: Grid, delay: int = 0):
        super().__init__()
        self.x = start_x
        self.y = start_y
        self.direction = direction
        self.grid = grid
        self.delay = delay
        self.step = self.grid.add_train_to_grid(self.x, self.y, self)

    def read_track(self):
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
                self.x -= 1
            elif self.direction == ">":
                new_x = self.x + 1
            reward = min(10 - self.delay, 10)

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

        reward = 0

        return new_x, new_y, reward

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.step += 1


def step(grid, actions, *args):
    for train in args:
        grid.add_train_to_grid(train.get("x"), train.get("y"), train.get("train"))
    # grid.change_world_state(actions)
    reward = grid.update_world()
    return grid.grid, reward, False


if __name__ == "__main__":
    gridworld = Grid()
