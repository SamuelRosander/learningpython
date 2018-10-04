import pygame
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
(width, height) = (800, 500)

pygame.init()
win = pygame.display.set_mode((width, height))

def main():
    running = True
    
    pygame.display.set_caption("Gravity")
    win.fill(WHITE)

    p = Particle(randint(20,width-20),randint(20,height-20),10)
    p.draw()

    pygame.display.flip()

    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p.vx -= 0.05
        if keys[pygame.K_RIGHT]:
            p.vx += 0.05
        if keys[pygame.K_UP]:
            if int(p.y) == height - p.size:
                p.vy = 15
        if keys[pygame.K_DOWN]:
            p.vy += 0.05

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
        self.vy = 0.0
        self.vx = 2
        self.ay = 0.1  # gravity

    def draw(self):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        # x right bounce
        if self.x >= width - self.size:
            self.x = width - self.size
            self.vx *= -1

        # x left bounce
        if self.x <= 0 + self.size:
            self.x = 0 + self.size
            self.vx *= -1

        # x stop threshold
        if abs(self.vx) < 0.05:
            self.vx = 0

        # y top bounce
        if self.y <= 0 + self.size:
            self.y = 0 + self.size
            self.vy *= -1

        # y bottom bounce
        if self.y >= height - self.size:
            self.y = height - self.size
            self.vy *= -1
            if self.vy < -0.3:  # threshold before stopping
                self.vy *= 0.6  # % of energy that will be preserved each bouce
            else:
                self.vy = 0

        # x linear slow
        if self.vx > 0:
            self.vx -= 0.01
        elif self.vx < 0:
            self.vx += 0.01
        
        # x max speed
        if self.vx > 5:
            self.vx = 5
        if self.vx < -5:
            self.vx = -5

        # set new values
        self.x += self.vx
        self.vy += self.ay
        self.y += self.vy
 
main()