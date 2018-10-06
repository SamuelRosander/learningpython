import pygame
from pygame.locals import *
import tkinter as tk

class Ball(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = BLACK
        self.thickness = 1
        self.bounce = 0.7   # % of energy that will be preserved each bouce
        self.xslow = 0.01   # linear slow
        self.vy = 0.0
        self.vx = 2
        self.gravity = 0.3
        self.jump_speed = 15

    def draw(self):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        # set new values
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

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
                self.vy *= self.bounce
            else:
                self.vy = 0

        # x linear slow
        if self.vx > 0:
            self.vx -= self.xslow
        elif self.vx < 0:
            self.vx += self.xslow
        
        # x max speed
        if self.vx > 5:
            self.vx = 5
        if self.vx < -5:
            self.vx = -5

BLACK = (0,0,0)
WHITE = (255,255,255)
(width, height) = (800, 500)

pygame.init()
win = pygame.display.set_mode((width, height), RESIZABLE)
font = pygame.font.Font(None, 20)
ball = Ball(width/4,height/2,10)

def main():
    global width, height
    running = True
    
    pygame.display.set_caption("Gravity")
    settings_label = font.render("Press S for settings. Arrows for movement", 1, BLACK)
    pygame.display.flip()

    while running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                win = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                (width,height) = pygame.display.get_surface().get_size()

        # key events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_LEFT]:
            ball.vx -= 0.05
        if keys[pygame.K_RIGHT]:
            ball.vx += 0.05
        if keys[pygame.K_UP]:
            if int(ball.y) == height - ball.size:
                ball.vy = -ball.jump_speed
        if keys[pygame.K_DOWN]:
            ball.vy += 0.3
        if keys[pygame.K_s]:
            settings(ball)

        # update the frame
        win.fill(WHITE)
        win.blit(settings_label, (10,10))
        ball.move()
        ball.draw()
        pygame.display.update()

    pygame.quit()

def settings(ball):
    """ Creates a window for the user to change the attributes for the ball """
    settings = tk.Tk()
    settings.title("Settings")

    label_bounce = tk.Label(settings, text="Bounciness", fg="black")
    label_bounce.grid(row=0, column=0, padx=2, pady=2, sticky="E")
    entry_bounce = tk.Entry(settings)
    entry_bounce.insert(0,ball.bounce)
    entry_bounce.grid(row=0, column=1, padx=2, pady=2)

    #label_xslow = tk.Label(settings, text="Resistance X", fg="black")
    #label_xslow.grid(row=1, column=0, padx=2, pady=2, sticky="E")
    #entry_xslow = tk.Entry(settings)
    #entry_xslow.insert(0,ball.xslow)
    #entry_xslow.grid(row=1, column=1, padx=2, pady=2)

    label_gravity = tk.Label(settings, text="Gravity", fg="black")
    label_gravity.grid(row=2, column=0, padx=2, pady=2, sticky="E")
    entry_gravity = tk.Entry(settings)
    entry_gravity.insert(0,ball.gravity)
    entry_gravity.grid(row=2, column=1, padx=2, pady=2)

    label_ballsize = tk.Label(settings, text="Ball size", fg="black")
    label_ballsize.grid(row=3, column=0, padx=2, pady=2, sticky="E")
    entry_ballsize = tk.Entry(settings)
    entry_ballsize.insert(0,ball.size)
    entry_ballsize.grid(row=3, column=1, padx=2, pady=2)

    label_jump_speed = tk.Label(settings, text="Jump speed", fg="black")
    label_jump_speed.grid(row=4, column=0, padx=2, pady=2, sticky="E")
    entry_jump_speed = tk.Entry(settings)
    entry_jump_speed.insert(0,ball.jump_speed)
    entry_jump_speed.grid(row=4, column=1, padx=2, pady=2)

    button_submit = tk.Button(settings, text="Save", command=lambda: submit(settings, entry_bounce.get(), entry_gravity.get(), entry_ballsize.get(), entry_jump_speed.get()), width=20)
    button_submit.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    settings.mainloop()

def submit(settings,b,g,bs,js):
    """ Sets the new values from settings """
    global ball
    ball.bounce = float(b)
    #ball.xslow = float(xs)
    ball.gravity = float(g)
    ball.size = int(bs)
    ball.jump_speed = float(js)    

    settings.destroy()

main()