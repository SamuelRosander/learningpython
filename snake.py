import pygame
from random import randint
from math import floor

class Snake(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.vx = 1
		self.vy = 0

	def draw(self, color):
		pygame.draw.rect(win, color, [self.x*20,self.y*20,20,20])

	def move(self):
		self.x = self.x + self.vx
		self.y = self.y + self.vy

	def changedir(self,vx,vy):
		self.vx = vx
		self.vy = vy

	def checkwalls(self,w,h):
		""" returns true if next move puts head outside window """
		return self.x + self.vx >= w / 20 or self.x + self.vx < 0 or self.y + self.vy >= h / 20 or self.y + self.vy < 0
			
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

framecount = 0
(width,height) = (400,400)
(foodx, foody) = (50,50)

pygame.init()
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake")
snake = Snake(2,int(height/20//2))
tail = []

pygame.display.flip()

def main():
	global framecount
	running = True
	game_over = False
	spawn_food()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and snake.vx != 1:
			snake.changedir(-1,0)
		if keys[pygame.K_RIGHT] and snake.vx != -1:
			snake.changedir(1,0)
		if keys[pygame.K_UP] and snake.vy != 1:
			snake.changedir(0,-1)
		if keys[pygame.K_DOWN] and snake.vy != -1:
			snake.changedir(0,1)

		if framecount % 10 == 0 and not game_over:
			if snake.checkwalls(width, height):
				game_over = True
				win.fill(WHITE)
				snake.draw(RED)
				for tailpart in tail:
					pygame.draw.rect(win, BLACK, [tailpart["x"]*20, tailpart["y"]*20, 20, 20])
				pygame.display.update()
			else:
				if snake.x == foodx and snake.y == foody:
					spawn_food()
					grow(snake.x, snake.y)

				for i, tailpart in enumerate(tail):
					if i < len(tail)-1:
						tail[i] = tail[i+1]
					else:
						tail[i] = {"x" : snake.x, "y" : snake.y}

				win.fill(WHITE)
				snake.move()
				snake.draw(BLACK)

				for tailpart in tail:
					pygame.draw.rect(win, BLACK, [tailpart["x"]*20, tailpart["y"]*20, 20, 20])

				pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10)
				pygame.display.update()

		framecount += 1
		#print(tail)
		pygame.time.delay(10)

	pygame.quit()

def spawn_food():
	global foodx, foody

	foodx = floor(randint(0,width/20-1))
	foody = floor(randint(0,height/20-1))

def grow(x, y):
	global tail
	tail.append({"x" : x, "y" : y})
		
main()