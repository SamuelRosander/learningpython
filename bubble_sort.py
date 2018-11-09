import pygame
from random import randint

pygame.init()
nums = []
size = 100
win = pygame.display.set_mode((size*10,600))

def main():
    global nums
    pygame.display.set_caption("Sorting")

    for i in range(size):
        nums.append(randint(0,599))

    draw_frame()

    for i in range(size-1):
        for j in range(size-i-1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
            draw_frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    pygame.time.delay(2000)
    pygame.quit()

def draw_frame():
    win.fill((0,0,0))
    for i in range(size):
        pygame.draw.rect(win, (255,255,255), [i*10,600-nums[i],10,nums[i]])
    pygame.display.update()

main()
