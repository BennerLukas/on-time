import sys, pygame
import time
from typing import List

pygame.init()

size = width, height = 1000, 500
screen = pygame.display.set_mode(size)

speed = [1, 0]
black = 255, 255, 255


class Zug:
    def __init__(self, grid: List, gridsize: int):
        self.speed = [1, 0]
        self.train = pygame.transform.scale(pygame.image.load("assets/train_icon.png"), (64, 64 * 0.3))
        self.train_rect = self.train.get_rect()
        self.direction = "0"
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
            print("HERE", self.speed)
        print(f"Grid Item: {grid_item} | Changed state: {self.direction} | Neuer Speed: {self.speed}")


bg = pygame.image.load("assets/bg_map.png").convert()

grid_width = width // 100
grid_height = height // 100
flipped = False

grid = [["-", "-", "-", "-", "v", "-", "-", "-", "-", "-"],
        ["-", ">", "-", "||", "|", "-", "-", "-", "-", "-"],
        ["-", "|", "-", "-", ">", "-", "-", "v", "-", "-"],
        ["-", "^", "-", "-", "-", "-", "-", "<", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]]

train = Zug(grid, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    train.change_speed()
    train.train_rect = train.train_rect.move(train.speed)

    screen.fill(black)
    # screen.blit(bg, (0, 0))
    screen.blit(train.train, train.train_rect)

    pygame.display.flip()
    time.sleep(0.01)
