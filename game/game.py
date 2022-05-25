import sys, pygame
import time
from more_itertools import distinct_combinations

pygame.init()

size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)

speed = [1, 0]
black = 255, 255, 255


class Zug:
    def __init__(self, id: int, grid: list, grid_signal: list, gridsize: int, start_x: int, start_y: int,
                 starting_rotation: float = 0,
                 starting_direction: str = ">"):
        self.grid_coord_y = None
        self.grid_coord_x = None
        self.id = id

        self.speed = None

        self.train = pygame.transform.scale(pygame.image.load("assets/train_icon.png"), (64, 20))
        self.train = pygame.transform.rotate(self.train, starting_rotation)

        self.train_rect = self.train.get_rect()
        self.train_rect.x = start_x
        self.train_rect.y = start_y

        self.direction = starting_direction
        self.grid = grid
        self.signal_grid = grid_signal
        self.gridsize = gridsize

        self.previous_symbol = "-"

    def change_speed(self):
        """
        self.direction = forwards momentum
        self.previous_item = seen track (-;|;<;>;^;v)
        self.speed = pixel change
        :return:
        """
        self.grid_coord_x = self.train_rect.x // self.gridsize
        self.grid_coord_y = self.train_rect.y // self.gridsize

        grid_item = self.grid[self.grid_coord_y][self.grid_coord_x]
        signal_item = self.signal_grid[self.grid_coord_y][self.grid_coord_y]
        if type(signal_item) == dict:
            if signal_item.get("current") == "||":
                self.speed = [0, 0]
                return None

        if grid_item == "-":
            if self.direction == ">":
                self.speed = [1, 0]
            elif self.direction == "<":
                self.speed = [-1, 0]

        elif grid_item == "|":
            if self.direction == "^":
                self.speed = [0, 1]
                print("up |")
            elif self.direction == "v":
                self.speed = [0, -1]
                print("down |")

        elif grid_item == ">":
            "Turning eastbound"
            if self.direction == "^":
                self.speed = [1, 0]
                self.train = pygame.transform.rotate(self.train, -90)
                self.direction = ">"
            elif self.direction == "v":
                self.speed = [1, 0]
                self.train = pygame.transform.rotate(self.train, 90)
                self.direction = ">"

        elif grid_item == "<":
            "Turning westbound"
            if self.direction == "^":
                self.speed = [-1, 0]
                self.train = pygame.transform.rotate(self.train, 90)
                self.direction = "<"
            elif self.direction == "v":
                self.speed = [-1, 0]
                self.train = pygame.transform.rotate(self.train, -90)
                self.direction = "<"

        elif grid_item == "^":
            "Turning northbound"
            if self.direction == ">":
                self.speed = [0, -1]
                self.train = pygame.transform.rotate(self.train, 90)
                self.direction = "^"
            elif self.direction == "<":
                self.speed = [0, -1]
                self.train = pygame.transform.rotate(self.train, -90)
                self.direction = "^"

        elif grid_item == "v":
            "Turning southbound"
            if self.direction == ">":
                self.speed = [0, 1]
                self.train = pygame.transform.rotate(self.train, -90)
                self.direction = "v"
            elif self.direction == "<":
                self.speed = [0, 1]
                self.train = pygame.transform.rotate(self.train, 90)
                self.direction = "v"

            elif grid_item == "|":
                self.speed = [0, 0]

        if self.previous_symbol != grid_item:
            print(
                f"ID: {self.id} | Current Grid Item: {grid_item} | Prev Item: {self.previous_symbol} | \n"
                f"X,Y = {self.train_rect.x, self.train_rect.y} | New Speed: {self.speed} | Direction: {self.direction}")
            self.previous_symbol = grid_item

    def move_train(self):
        self.train_rect = self.train_rect.move(self.speed)

    def render_frame(self):
        self.change_speed()
        self.move_train()


def draw_screen():
    height = 64
    width = 64
    for cnt_row, x in enumerate(grid):
        for cnt_col, y in enumerate(x):
            if y == "-":
                image = pygame.image.load("assets/schiene_horizontal.png").convert()
                screen.blit(image, (cnt_row*64, cnt_col*64))
            elif y == "|":
                image = pygame.image.load("assets/schiene_vertikal.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == "^":
                image = pygame.image.load("assets/schiene_weiche_hoch.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == "^":
                image = pygame.image.load("assets/schiene_weiche_hoch.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == "v":
                image = pygame.image.load("assets/schiene_weiche_runter.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == "<":
                image = pygame.image.load("assets/schiene_weiche_links.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == ">":
                image = pygame.image.load("assets/schiene_weiche_rechts.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))
            elif y == "||":
                image = pygame.image.load("assets/signal.png").convert()
                screen.blit(image, (cnt_row * 64, cnt_col * 64))

    pygame.display.flip()




bg = pygame.image.load("assets/bg_map.png").convert()

grid_width = width // 64
grid_height = height // 64
# print(grid_width, grid_height)
grid = [
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', 'v', '-', '-', '-', '-', '<', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '0', '0', '0', '0', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '>', '-', '-', '-', '^', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', 'v', '-', '-', '-', '-', '-', '-', '|', '|', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '<', '0'],
    ['0', '|', '0', '0', '0', '0', '0', '0', '|', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '|', '0'],
    ['0', '>', '-', '-', '-', '-', '-', '-', '|', '|', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '^', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '^', '-', '-', '-', '<', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '|', '0', '0', '0', '0', '|', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '>', '-', '-', '-', '-', '^', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
]

grid_signal = [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '*', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', {"current": "|", "actions": ["|", "||"]}, '', '', '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['', '', '*', '', '', '', '', '', '', '', {"current": "-", "actions": ["-", "||"]}, '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', {"current": "-", "actions": ["-", "||"]}, '', '', '', '', '', '', '', '', '', '', '',
     '*', '', '', ''],
    ['', '', '', '', '', '', '', '', '', {"current": "||", "actions": ["|", "||"]}, '', '', '', '', '', '', '', '', '',
     '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '*', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
]

# train1 = Zug(1, grid, grid_signal, gridsize=64, start_x=3 * 64, start_y=7 * 64 + 63, starting_rotation=0,
#              starting_direction=">")
# train2 = Zug(2, grid, grid_signal, gridsize=64, start_x=20 * 64, start_y=5 * 64 + 63, starting_rotation=180,
#              starting_direction="<")
train3 = Zug(3, grid, grid_signal, gridsize=64, start_x=12 * 64, start_y=1 * 64, starting_rotation=180,
             starting_direction="<")
trains = [train3]
# trains = [train1, train2, train3]


def eval_crash(train_obj_1: Zug, train_obj_2: Zug):
    if train_obj_1.grid_coord_x == train_obj_2.grid_coord_x and train_obj_1.grid_coord_y == train_obj_2.grid_coord_y:
        print(
            f"CRASH! Train {train_obj_1.id} collided with {train_obj_2.id} on Grid-Coordinate {train_obj_1.grid_coord_x, train_obj_1.grid_coord_y}")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for train in trains:
        train.render_frame()

    for permuation in distinct_combinations(trains, 2):
        eval_crash(permuation[0], permuation[1])

    screen.fill(black)
    # screen.blit(bg, (0, 0))

    # screen.blit(train1.train, train1.train_rect)
    # screen.blit(train2.train, train2.train_rect)
    screen.blit(train3.train, train3.train_rect)
    screen.blits([[x.train, x.train_rect] for x in trains])
    pygame.display.flip()
    time.sleep(0.005)
