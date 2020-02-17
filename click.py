import pygame
#curser, fulscreen
pygame.init()
dsize = (800, 800)
win = pygame.display.set_mode(dsize)

colorinactive = (122, 122, 122)
inputboxes = []

class Inputbox:
    def __init__(self):
        boxsize = [140, 40]
        self.rect = pygame.Rect(dsize[0]-boxsize[0], len(inputboxes)*50, boxsize[0], boxsize[i])
        self.color = colorinactive
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False

    def handleevent(self, event):
        if event.type == pgygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = coloracctive if self.active else colorinactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    #handle input
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    #handle keyhold
                    self.text = self.text[:-1]
                else:
                    #handle keyhold
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(win, self.color, self.rect, 2)

def clickboxes():
    pass
    


inputboxes.append(Inputbox)
clickbox = clickboxes
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in inputboxes:
            bfjdsox.handleevent(event)
    pygame.display.update()
    win.fill((255, 255, 255))
pygame.quit()
