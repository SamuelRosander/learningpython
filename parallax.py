import pygame
from random import randint

class BackgroundHouse(object):
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height
        self.x = WIDTH
        self.y = GROUND_LEVEL-self.height

    def draw(self):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.width, self.height])

    def move(self, vx):
        self.x += vx


class Player(object):
    def __init__(self):
        self.radius = 30
        self.x = 200
        self.y = GROUND_LEVEL - self.radius
        self.gravity = 4
        self.jump_speed = 60
        self.vy = 0


    def draw(self):
        pygame.draw.circle(win, BLACK, (self.x, int(self.y)), self.radius)


    def move(self):
        self.vy += self.gravity
        self.y += self.vy

        if self.y + self.radius >= GROUND_LEVEL:
            self.y = GROUND_LEVEL - self.radius
            self.vy = 0

FPS = 60
(WIDTH, HEIGHT) = (1920,1080) #(2560, 1440)
GROUND_LEVEL = int(HEIGHT * 0.85)
HOUSE_BASE_HEIGHT = 150
HOUSE_BASE_WIDTH = 250
COLOR_GROUND = pygame.Color("#0d040d")
COLOR_BG = pygame.Color("#842884")
COLOR_BG_LAYER = [pygame.Color("#210a21"), pygame.Color("#421442"), pygame.Color("#631e63")]
BLACK = (0,0,0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parallax!")

player = Player()
bg_layer = [[],[],[]]


def main():
    running = True
    frame = 0

    for i in range(3):
        bg_layer[i].append(BackgroundHouse(COLOR_BG_LAYER[i], randint(HOUSE_BASE_WIDTH - i * 50, HOUSE_BASE_WIDTH + 100 - i * 50), randint(HOUSE_BASE_HEIGHT + i * 150 , HOUSE_BASE_HEIGHT + 350 + i * 150)))

    next_layer = [50,30,80]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            if player.y + player.radius == GROUND_LEVEL:
                player.vy = -player.jump_speed

        for i in range(3):
            pass

        for i, layer_list in enumerate(bg_layer):
            for house in reversed(layer_list):
                house.move(-10 + i * 1)
                if house.x <= 0 - house.width:
                    layer_list.remove(house)
            if WIDTH - (layer_list[-1].x + layer_list[-1].width) >= next_layer[i]:
                layer_list.append(BackgroundHouse(COLOR_BG_LAYER[i], randint(HOUSE_BASE_WIDTH - i * 50, HOUSE_BASE_WIDTH + 100 - i * 50), randint(HOUSE_BASE_HEIGHT + i * 150 , HOUSE_BASE_HEIGHT + 350 + i * 150)))
                next_layer[i] = randint(10,300)

        player.move()
        draw_frame()
        pygame.time.delay(int(1000/FPS))
        print(frame)
        print(len(bg_layer[0])+len(bg_layer[1])+len(bg_layer[2]))
        print(player.y)
        print(player.vy)
        frame += 1

    pygame.quit()


def draw_frame():
    win.fill(COLOR_BG)

    for layer in reversed(bg_layer):
        for house in layer:
            house.draw()

    pygame.draw.rect(win, COLOR_GROUND, [0, GROUND_LEVEL, WIDTH, HEIGHT-GROUND_LEVEL])
    player.draw()

    pygame.display.update()


main()
