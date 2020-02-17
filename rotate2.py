import pygame

pygame.init()

#globals
clock = pygame.time.Clock()
dsize = (1800, 900)
win = pygame.display.set_mode(dsize)
graphsize = (800, 800)
graph = pygame.Surface(graphsize, 2)
running = True
white = (255, 255, 255)
gray = (200, 200, 200)
line = pygame.image.load('line.png')
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.fill(gray)
    graph.fill(white)
    #draw here
    graph.blit(line, (350, 0))
    graph.blit(pygame.transform.rotate(line, angle), (350, 0))
    angle += 1
    win.blit(graph, (10, 10))
    
    pygame.display.update()
pygame.quit()
