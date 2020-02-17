import pygame
import time
import math
pygame.init()
win = pygame.display.set_mode((800, 800))
image = pygame.image.load('2018-07-15_mh_0012.jpg')
frame = pygame.Surface((300, 200)) 
running = True
clock = pygame.time.Clock()
angle = 0

print image.get_rect()

def rotate(surface, x, y, image, angle):
    rotated = pygame.transform.rotate(image, angle)
    win.blit(rotated, (400, 400))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.fill((255, 255, 255))
    rotate(win, 400, 400, image, 10)
    win.blit(image, (400, 400))
    pygame.display.update()
    angle += 1%360
    clock.tick(60)
pygame.quit()
