import pygame
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
(width, height) = (500, 300)

pygame.init()
win = pygame.display.set_mode((width, height))

def main():
    running = True
    
    pygame.display.set_caption("Bouncy Ball")
    win.fill(WHITE)

    p = Particle(randint(10,490),randint(10,290),10)
    p.draw()

    pygame.display.flip()

    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if p.x >= width - p.size or p.x <= 0 + p.size:
            p.dx *= -1

        if p.y >= height - p.size or p.y <= 0 + p.size:
            p.dy *= -1

        win.fill(WHITE)
        p.move()
        p.draw()
        pygame.display.update()

    pygame.quit()

class Particle(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = BLACK
        self.thickness = 1
        self.dx = 2
        self.dy = 2

    def draw(self):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.size)

    def move(self):
        self.x += self.dx
        self.y += self.dy
 
main()