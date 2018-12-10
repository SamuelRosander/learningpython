import pygame
from random import randint
from math import floor

class Snakehead(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.vx = 1 # velocity x axis
		self.vy = 0 # velocity y axis

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def changedir(self, vx, vy):
		self.vx = vx
		self.vy = vy

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY  = (80,80,80)

pygame.init()

(width, height) = (400,400)
(foodx, foody) = (0,0)
snake = Snakehead(2,9)
tail = [] # highest index are closest to head
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

		# listeners
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

			tail.append({"x" : snake.x, "y" : snake.y}) # add current head to tail to move the tail 1 step forward

			if snake.x == foodx and snake.y == foody: # if food gets eaten
				spawn_food()
				score += 1
			elif not checkcrash(snake, tail): # checkcrash to have the correct tail drawn when game is over
				del tail[0] # remove last tail piece to move the tail if no food is eaten

			if checkcrash(snake, tail): # if next frame will be a crash
				game_over = True
				draw_game_over_frame()
			else:
				snake.move() # move the head
				draw_frame()

		pygame.time.delay(80)

	pygame.quit()

def restart_game():
	global snake, tail, score

	spawn_food()
	snake = Snakehead(2,9)
	tail = []
	score = 0

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

def checkcrash(head, tail):
	""" returns true if head is outside windows or in tail next frame """
	if head.x + head.vx >= width / 20 or head.x + head.vx < 0 or head.y + head.vy >= height / 20 or head.y + head.vy < 0:
		return True
	for i,t in enumerate(tail):
		if head.x + head.vx == t["x"] and head.y + head.vy == t["y"] and i > 0: # i > 0 to prevent collision with the last tail piece that will move
			return True
	return False

def draw_frame():
	""" draws a normal game frame """
	win.fill(WHITE)

	pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10) # food
	for t in tail:
		pygame.draw.rect(win, BLACK, [t["x"]*20, t["y"]*20, 20, 20]) # tail
	pygame.draw.rect(win, BLACK, [snake.x*20, snake.y*20, 20, 20]) # head

	pygame.display.update()

def draw_game_over_frame():
	""" draws the frame when game is over """
	win.fill(WHITE)

	pygame.draw.circle(win, BLACK, (foodx*20+10,foody*20+10), 10) # food
	for t in tail:
		pygame.draw.rect(win, BLACK, [t["x"]*20, t["y"]*20, 20, 20]) # tail
	pygame.draw.rect(win, RED, [snake.x*20, snake.y*20, 20, 20]) # head

	gameover_label = font.render("Game over. Your score: {0}".format(score), 1, GRAY)
	restart_label = font.render("Press SPACE to restart", 1, GRAY)
	gameover_label_rect = gameover_label.get_rect(center=(width/2, 100)) # center the text
	restart_label_rect = restart_label.get_rect(center=(width/2,130)) # center the text
	win.blit(gameover_label, gameover_label_rect)
	win.blit(restart_label, restart_label_rect)

	pygame.display.update()

main()
