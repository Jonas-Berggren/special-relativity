import pygame as pg
#add curser
inputboxes = []
dsize = [800, 800]
boxsize = [140, 40]
pg.init()
size = pg.display.Info()
screen = pg.display.set_mode(dsize)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class InputBox:
    def __init__(self, w, h,):
        self.rect = pg.Rect(dsize[0] - boxsize[0] - 70, 50*len(inputboxes)+10, 140, 40)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)




clock = pg.time.Clock()
for i in range(5):
    inputboxes.append(InputBox( boxsize[0], boxsize[1]))
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        for box in inputboxes:
            box.handle_event(event)
    for box in inputboxes:
        box.update()

    screen.fill((255, 255, 255))
    for box in inputboxes:
        box.draw(screen)

    pg.display.flip()
    #clock.tick(30)

pg.quit()
