import pygame as pg
#add curser
buttons = []
inputboxes = []
dsize = [1800, 900]
screen = (10, 10, 1000, 800), 2
xaxis = (screen[0][0], screen[0][3]/2 + screen[0][1], screen[0][2], 2)
yaxis = (screen[0][2]/2+10, screen[0][1], 2,screen[0][3])
frame = [screen, xaxis]
boxsize = [140, 40]
pg.init()
size = pg.display.Info()
win = pg.display.set_mode(dsize)
inactive = pg.Color('lightskyblue3')
active = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class Button:
    def __init__(self, buttontype):
        self.rect = pg.Rect(dsize[0] - boxsize[0] - 50, 50*len(inputboxes)+10, boxsize[0], boxsize[1])
        self.color = inactive
        self.text = 'add'
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False
        self.buttontype = buttontype

    def handle(self, event):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.active = True
            if event.type == pg.MOUSEBUTTONDOWN:
                inputboxes.append(Inputbox())
                self.rect.y = 50*len(inputboxes)+10 
        else:
            self.active = False
            # Change the current color of the input box.
        self.color = active if self.active else inactive

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(win, self.color, self.rect, 2)

class Inputbox:
    def __init__(self):
        self.rect = pg.Rect(dsize[0] - boxsize[0] - 70, 50*len(inputboxes)+10, boxsize[0], boxsize[1])
        self.color = inactive
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False

    def handle(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = active if self.active else inactive
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

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(win, self.color, self.rect, 2)

class Object:
    def __init__(self, x, v, name):
        self.v = v
        self.x = x
        self.name = name
        self.rect = pg.Rect(500, 500, 4, 500)

    def change(self):
        self.rect = pg.transform.rotate(self.rect, 10)

    def draw(self):
        pg.draw.rect(win, (255, 0, 0), self.rect)
        


inputboxes.append(Inputbox())
buttons.append(Button('add'))
line = Object(654, 6546, 6456)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for box in inputboxes:
            box.handle(event)
        for button in buttons:
            button.handle(event)

    #graphics start here
    win.fill((255, 255, 255))
    black = (0, 0, 0)
    pg.draw.rect(win, black, screen[0], screen[1])
    pg.draw.rect(win, black, xaxis)
    pg.draw.rect(win, black, yaxis)
    line.change()
    line.draw()
    for button in buttons:
        button.draw(win)
    for box in inputboxes:
        box.draw(win)

    pg.display.update()
pg.quit()
