import pygame
import math
import time

pygame.init()

#globals
winsize = (1800, 900)
win = pygame.display.set_mode(winsize)#use idsplaysize
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(30)
    

pygame.quit()
