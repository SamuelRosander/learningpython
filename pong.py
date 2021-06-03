import pygame
import random
import math

class Ball(object):
    def __init__(self):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.vx = 5 * random.choice([-1,1])
        self.vy = 0 #random.randint(-3,3)
        self.radius = 10
        self.color = BLACK


    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy *= -1


    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)


class Player(object):
    def __init__(self, player_nr):
        self.player_nr = player_nr
        self.y = HEIGHT/2
        self.height = 60
        self.width = 10
        self.move_speed = 5
        if player_nr == 1:
            self.x = 1
        else:
            self.x = WIDTH - self.width - 1


    def draw(self):
        pygame.draw.rect(win, BLACK, [self.x, self.y, self.width, self.height])


    def move(self, vy):
        self.y += vy * self.move_speed

        if self.y <= 1:
            self.y = 1

        if self.y + self.height >= HEIGHT - 1:
            self.y = HEIGHT - self.height - 1


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
FPS = 60
(WIDTH, HEIGHT) = (600,400)

pygame.init()
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

ball = Ball()
player_one = Player(1)
player_two = Player(2)

def main():
    reset_game()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_over = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if not game_over:
            if keys[pygame.K_UP]:
                player_two.move(-1)
            if keys[pygame.K_DOWN]:
                player_two.move(1)
            if keys[pygame.K_w]:
                player_one.move(-1)
            if keys[pygame.K_s]:
                player_one.move(1)

        ball.move()
        if check_collision():
            game_over = True
        draw_frame()
        pygame.time.delay(int(1000/60))
        print(ball.vx)


def check_collision():
    if ball.x <= player_one.width:
        if player_one.y < ball.y < player_one.y + player_one.height:

            cell_size = player_one.height / 5

            if player_one.y + cell_size > ball.y:
                ball.vy -= 2
            elif player_one.y + cell_size * 2 > ball.y:
                ball.vy -= 1
            elif player_one.y + cell_size * 3 > ball.y:
                pass
            elif player_one.y + cell_size * 4 > ball.y:
                ball.vy += 1
            elif player_one.y + cell_size * 5 > ball.y:
                ball.vy += 2


            ball.vx *= -1
            if ball.vx > 0:
                ball.vx += 0.1
            else:
                ball.vx -= 0.1

            return False
        else:
            ball.color = RED
            ball.vx = 0
            ball.vy = 0
            return True

    if ball.x >= WIDTH - player_two.width:
        if player_two.y < ball.y < player_two.y + player_two.height:

            cell_size = player_two.height / 5

            if player_two.y + cell_size > ball.y:
                ball.vy -= 2
            elif player_two.y + cell_size * 2 > ball.y:
                ball.vy -= 1
            elif player_two.y + cell_size * 3 > ball.y:
                pass
            elif player_two.y + cell_size * 4 > ball.y:
                ball.vy += 1
            elif player_two.y + cell_size * 5 > ball.y:
                ball.vy += 2


            ball.vx *= -1
            if ball.vx > 0:
                ball.vx += 0.1
            else:
                ball.vx -= 0.1

            return False
        else:
            ball.color = RED
            ball.vx = 0
            ball.vy = 0
            return True


def reset_game():
    global ball, player_one, player_two
    ball = Ball()
    player_one = Player(1)
    player_two = Player(2)


def draw_frame():
    win.fill(WHITE)
    ball.draw()
    player_one.draw()
    player_two.draw()
    pygame.display.update()

main()
