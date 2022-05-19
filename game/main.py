import sys, pygame
import time
from typing import List

pygame.init()

size = width, height = 1000, 500
screen = pygame.display.set_mode(size)

speed = [1, 0]
black = 255, 255, 255


class Zug:
    def __init__(self, id: int, grid: List, gridsize: int, start_x: int, start_y: int, starting_rotation:float = 0,
                 start_speed: list[int, int] = [1, 0]):
        self.id = id

        self.speed = start_speed

        self.train = pygame.transform.scale(pygame.image.load("assets/train_icon.png"), (64, 64 * 0.3))
        self.train = pygame.transform.rotate(self.train, starting_rotation)

        self.train_rect = self.train.get_rect()
        self.train_rect.x = start_x
        self.train_rect.y = start_y

        self.direction = "-"
        self.grid = grid
        self.gridsize = gridsize

    def change_speed(self):
        grid_coord_x = self.train_rect.x // self.gridsize
        grid_coord_y = self.train_rect.y // self.gridsize

        grid_item = self.grid[grid_coord_y][grid_coord_x]

        if grid_item == "<":
            if self.direction == "|":
                self.speed = [-1, 0]
                self.direction = "-"
                self.train = pygame.transform.rotate(self.train, 270)
        elif grid_item == ">":
            if self.direction == "|":
                self.speed = [1, 0]
                self.direction = "-"
                self.train = pygame.transform.rotate(self.train, 90)
        elif grid_item == "^":
            if self.direction == "-":
                self.speed = [0, -1]
                self.direction = "|"
                self.train = pygame.transform.rotate(self.train, 90)
        elif grid_item == "v":
            if self.direction == "-":
                self.speed = [0, 1]
                self.direction = "|"
                self.train = pygame.transform.rotate(self.train, 270)
                print("HERE")
        elif grid_item == "-":
            if self.direction == "0":
                self.speed = [1, 0]
                self.direction = "-"
        elif grid_item == "||":
            self.speed = [0, 0]
        print(f"ID: {self.id} | Grid Item: {grid_item} | Changed state: {self.direction} | X,Y = {self.train_rect.x, self.train_rect.y}")

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

grid_width = width // 100
grid_height = height // 100
grid = [["-", "-", "-", "-", "v", ">", "-", "-", "-", "||"],
        ["-", ">", "-", "-", "|", "|", "-", "||", "-", "-"],
        ["-", "|", "-", "-", ">", "|", "-", "v", "-", "-"],
        ["-", "^", "-", "-", "-", "|", "-", "<", "-", "-"],
        ["-", "-", "-", "-", "-", "^", "-", "-", "-", "-"]]

train1 = Zug(1, grid, 100, 0, 0)
train2 = Zug(2, grid, 100, 900, 300, 180, [-1, 0])
train3 = Zug(3, grid, 100, 0, 450)
trains = [train1, train2, train3]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for train in trains:
        train.render_frame()


    screen.fill(black)
    # screen.blit(bg, (0, 0))

    screen.blit(train1.train, train1.train_rect)
    screen.blit(train2.train, train2.train_rect)
    screen.blit(train3.train, train3.train_rect)
    screen.blits([[x.train, x.train_rect] for x in trains])
    pygame.display.flip()
    time.sleep(0.005)
