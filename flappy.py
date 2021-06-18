import pygame
from random import randint

(width, height) = (400, 600)
gravity = 0.3
jump_speed = 7
player_radius = 16
pipe_hole_size = 120
pipe_width = 32
pipe_freq = 150
pipes = []
score = 0


class Player(object):
    def __init__(self):
        self.x = 50
        self.y = height / 2
        self.vy = 0
        self.color = (0, 0, 0)

    def update(self):
        self.y += self.vy
        self.vy += gravity

        if self.y < player_radius:
            self.y = player_radius

        if self.y > height - player_radius:
            self.y = height - player_radius


class Pipe(object):
    def __init__(self, y1, y2):
        self.x = width
        self.y1 = y1
        self.y2 = y2

    def update(self):
        self.x -= 2


pygame.init()
win = pygame.display.set_mode((width, height))
font = pygame.font.Font(None, 25)

player = Player()


def main():
    global score
    running = True
    game_over = False
    frame_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_UP]:
                player.vy = -jump_speed
            if keys[pygame.K_SPACE] and game_over:
                game_over = False
                for p in reversed(pipes):
                    pipes.remove(p)
                score = 0
                player.y = height / 2
                player.vy = 0

        if not game_over:
            if frame_count % pipe_freq == 0:
                create_pipes()

            player.update()
            for p in pipes:
                p.update()

        if collision():
            player.color = (255, 0, 0)
            game_over = True
        else:
            player.color = (0, 0, 255)

        draw_frame()
        frame_count += 1

        for p in pipes:
            if p.x < 0 - pipe_width:
                pipes.remove(p)
                score += 0.5

        pygame.time.delay(10)

    pygame.quit()


def create_pipes():
    y = randint(0, height - pipe_hole_size)
    pipes.append(Pipe(0, y))
    pipes.append(Pipe(y + pipe_hole_size, height))


def check_collision():
    for p in pipes:
        if p.x - player_radius < player.x < p.x + pipe_width + player_radius \
                and p.y1 - player_radius <= player.y <= p.y2 + player_radius:
            return True
    return False


def collision():
    for p in pipes:
        delta_x = player.x - max(p.x, min(player.x, p.x + pipe_width))
        delta_y = player.y - max(p.y1, min(player.y, p.y1 + p.y2))
        if delta_x * delta_x + delta_y * delta_y < player_radius * player_radius:
            return True
    return False


def draw_frame():
    win.fill((255, 255, 255))
    for p in pipes:
        pygame.draw.rect(win, (0, 0, 0), [p.x, p.y1, pipe_width, p.y2])
        # pygame.draw.line(win, (0, 255, 0), (player.x, player.y),
        #                  (max(p.x, min(player.x, p.x + pipe_width)), max(p.y1, min(player.y, p.y1 + p.y2))))
    pygame.draw.circle(win, player.color, (int(player.x), int(player.y)), player_radius)

    label = font.render(str(int(score)), 1, (0, 0, 0))
    win.blit(label, (10, 10))

    pygame.display.update()


main()
