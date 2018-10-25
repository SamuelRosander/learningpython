import pygame
from random import randint
from math import floor

class Snakehead(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.vx = 1
		self.vy = 0

	def draw(self, color):
		pygame.draw.rect(win, color, [self.x*20, self.y*20, 20, 20])

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def changedir(self, vx, vy):
		self.vx = vx
		self.vy = vy

	def checkcrash(self, w, h, tail):
		""" returns true if next move puts head outside window or in tail """
		if self.x + self.vx >= w / 20 or self.x + self.vx < 0 or self.y + self.vy >= h / 20 or self.y + self.vy < 0:
			return True
		for i,t in enumerate(tail):
			if self.x + self.vx == t["x"] and self.y + self.vy == t["y"] and i > 0: # i > 0 to prevent collision with the last tail piece that will move 
				return True
		return False
			
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARKRED  = (128,0,0)

pygame.init()

(width, height) = (400,400)
(foodx, foody) = (0,0)
snake = Snakehead(2,9)
tail = []
score = 0
win = pygame.display.set_mode((width,height))
font = pygame.font.Font(None, 30)

def main():
	running = True
	game_over = False
	keys_locked = False # to prevent going backwards by tapping two keys fast in sequence

	pygame.display.set_caption("Snake")
	spawn_food()

	# main loop
	while running:
		global score

		#key listeners
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

			# had to do the if blocks this way to get the scoring correct if you die just after eating near a wall
			if snake.x == foodx and snake.y == foody: # if food gets eaten
				spawn_food()
				tail.append({"x" : snake.x, "y" : snake.y}) # add current head to tail
				score += 1
				if snake.checkcrash(width, height, tail):
					game_over = True
					draw_game_over_frame()
				else:
			 		snake.move()
			 		draw_frame()
			else:
				if snake.checkcrash(width, height, tail):
					game_over = True
					draw_game_over_frame()
				else:
					for i, t in enumerate(tail):
						if i < len(tail)-1:
							tail[i] = tail[i+1] # move the tail by shifting the pieces one position in the list
						else:
							tail[i] = {"x" : snake.x, "y" : snake.y} # last tail piece (closest to head) gets the value of the head
					snake.move()
					draw_frame()

		pygame.time.delay(100)

	pygame.quit()

def restart_game():
	global snake, tail, score

	spawn_food()
	snake = Snakehead(2,9)
	tail = []
	score = 0

#
def spawn_food():
	""" generates a new random location for the food, checking if its already been occupied by the tail """
	global foodx, foody

	while 1:
		randx = randint(0,width/20-1)
		randy = randint(0,height/20-1)

		if {"x" : randx, "y" : randy} not in tail:
			foodx = randx
			foody = randy
			break

def draw_frame():
	win.fill(WHITE)

	snake.draw(BLACK) # head
	for t in tail:
		pygame.draw.rect(win, BLACK, [t["x"]*20, t["y"]*20, 20, 20]) # tail
	pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10) # food

	pygame.display.update()

def draw_game_over_frame():
	win.fill(WHITE)

	pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10)
	for t in tail:
		pygame.draw.rect(win, BLACK, [t["x"]*20, t["y"]*20, 20, 20])
	snake.draw(RED)
	
	gameover_label = font.render("Game over. Your score: {0}".format(score), 1, DARKRED)
	restart_label = font.render("Press SPACE to restart", 1, DARKRED)
	gameover_label_rect = gameover_label.get_rect(center=(width/2, 100))
	restart_label_rect = restart_label.get_rect(center=(width/2,130))
	win.blit(gameover_label, gameover_label_rect)
	win.blit(restart_label, restart_label_rect)
	
	pygame.display.update()

main()