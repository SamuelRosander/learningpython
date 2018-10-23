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

	def checkcrash(self,w,h,tail):
		""" returns true if next move puts head outside window """
		if self.x + self.vx >= w / 20 or self.x + self.vx < 0 or self.y + self.vy >= h / 20 or self.y + self.vy < 0:
			return True
		for i,t in enumerate(tail):
			if self.x + self.vx == t["x"] and self.y + self.vy == t["y"] and i > 0:
				return True
		return False
			
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

(width, height) = (400, 400)
(foodx, foody) = (0, 0)

pygame.init()
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake")

snake = Snake(2,9)
tail = []

pygame.display.flip()

def main():
	global snake, tail
	running = True
	game_over = False
	keys_locked = False # to prevent going backwards by tapping two keys fast in sequence
	spawn_food()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and game_over == True:
					game_over = False
					restart_game()
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_LEFT and snake.vx != 1 and not keys_locked:
					keys_locked = True
					snake.changedir(-1,0)
				if event.key == pygame.K_RIGHT and snake.vx != -1 and not keys_locked:
					keys_locked = True
					snake.changedir(1,0)
				if event.key == pygame.K_UP and snake.vy != 1 and not keys_locked:
					keys_locked = True
					snake.changedir(0,-1)
				if event.key == pygame.K_DOWN and snake.vy != -1 and not keys_locked:
					keys_locked = True
					snake.changedir(0,1)

		if not game_over:
			keys_locked = False # activates movement key presses again

			if snake.checkcrash(width, height, tail): # if crash, draw a game over frame
				game_over = True
				win.fill(WHITE)
				snake.draw(RED)
				for t in tail:
					pygame.draw.rect(win, BLACK, [t["x"]*20, t["y"]*20, 20, 20])
				pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10)
				pygame.display.update()
			else: # draw a normal frame
				if snake.x == foodx and snake.y == foody: # spawn new food when it gets eaten and add current square to tail
					spawn_food()
					tail.append({"x" : snake.x, "y" : snake.y})
				else: # shift the tail pieces on position in the list
					for i, tailpart in enumerate(tail):
						if i < len(tail)-1:
							tail[i] = tail[i+1]
						else:
							tail[i] = {"x" : snake.x, "y" : snake.y}

				win.fill(WHITE)
				snake.move()
				snake.draw(BLACK)

				for tailpart in tail: #draw the tail
					pygame.draw.rect(win, BLACK, [tailpart["x"]*20, tailpart["y"]*20, 20, 20]) 

				pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10) # draw the food
				pygame.display.update()

		pygame.time.delay(100)

	pygame.quit()

def restart_game():
	global snake, tail

	spawn_food()
	snake = Snake(2,9)
	tail = []

def spawn_food():
	global foodx, foody

	while 1: # generate a new x and y value if it's already occupied by the tail
		randx = floor(randint(0,width/20-1))
		randy = floor(randint(0,height/20-1))

		if {"x" : randx, "y" : randy} not in tail:
			foodx = randx
			foody = randy
			break

main()