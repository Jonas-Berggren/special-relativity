import pygame
import math
import time
pygame.init()
#colors
active = (0, 0, 255)
inactive = (0, 100, 100)
white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)

#globals
winsize = (1800, 900)
graphsize = (800, 800)
consize = (800, 800)
boxsize = (400, 400)
errsize = (400, 400)
win = pygame.display.set_mode(winsize, 0, 32)#use idsplaysize
graph = pygame.Surface(graphsize)
control = pygame.Surface(consize)
errwin = pygame.Surface(errsize)   
running = True
img = pygame.image.load
inactiveline = [img('inactiveline_black.png'), img('inactiveline_red.png'), img('inactiveline_blue.png'), img('inactiveline_green.png'), img('inactiveline_orange.png'), img('inactiveline_yellow.png'), img('inactiveline_purple.png'), img('inactiveline_turq.png'), img('inactiveline_brown.png'), img('inactiveline_grey.png')]
activeline = [img('activeline_black.png'), img('activeline_red.png'), img('activeline_blue.png'), img('activeline_green.png'), img('activeline_orange.png'), img('activeline_yellow.png'), img('activeline_purple.png'), img('activeline_turq.png'), img('activeline_brown.png'), img('activeline_grey.png')]
inactivetick = pygame.image.load('inactivetick.png')
activetick = pygame.image.load('activetick.png')
FONT = pygame.font.Font(None, 32)
font = pygame.font.Font(None, 20)
fontobj = pygame.font.Font(None, 25)
graphpos = (10, 10)
conpos = (winsize[0] - (consize[0] + 10), 10)
errpos = (100, 100)
clock = pygame.time.Clock()
rotate = pygame.transform.rotate
deg = math.degrees
atan = math.atan
tan = math.tan
sin = math.sin
cos = math.cos
pi = math.pi
root = math.sqrt
state = None
txt_t = font.render('t', True, black)
txt_ct = font.render('ct', True, black)
txt_t_rect = pygame.Rect(graphsize[0]/2 + 20, 20, 140, 40)
txt_ct_rect = pygame.Rect(graphsize[0] - 40, graphsize[1]/2 + 20, 140, 40)
increment = 0.1
err = None

#lists
objs = []
buttons = []
sendbuttons = []
inputs = []
delbuttons = []

xaxis = rotate(inactiveline[0], 90)
xticks = []
for i in range(int(graphsize[0] / 20)):
    xticks.append((rotate(inactivetick, 90), (i*20, graphsize[1]/2)))
yaxis = inactiveline[0]
yticks = []
for i in range(int(graphsize[1] / 20)):
    yticks.append((inactivetick, (graphsize[0]/2, i*20)))

def error(m):
    global err
    global count
    if m == 'frame': 
        text = 'frame'
    if m == 'char':
        text = 'das ist keine Zahl'
    if m == 'speed':
        text = 'Einstein sagt nein'
    if text != None:
        err = m
        txt_surface = FONT.render(text, True, black)
        errwin.blit(txt_surface, (5, 5))
        button = Button('ok')
        buttons.append(button)

def change(f):
    global state
    incx = 0.3
    incv = 0.01
    framex = objs[f].x
    framev = objs[f].v
    state = f
    if abs(objs[f].v) == 1: 
        error('frame')
        state = None
    else:
        if framex != 0:
            if framex > incx:
                for i in range(len(objs)):
                    x = objs[i].x - incx
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex)
                    inputs[i].x.text = str(round(x/20, 8))
            elif framex < -incx:
                for i in range(len(objs)):
                    x = objs[i].x + incx
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex)
                    inputs[i].x.text = str(round(x/20, 8))
            else:
                for i in range(len(objs)):
                    x = objs[i].x - framex
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex)
                    inputs[i].x.text = str(round(x/20, 8))
        elif framev != 0:
            if framev > incv:
                for i in range(len(objs)):
                    if abs(objs[i].v) !=1:
                        x = objs[i].x
                        v = (objs[i].v - incv)/(1+(objs[i].v*-incv)) 
                        objs[i] = Obj(objs[i].n, i, objs[i].x, v, objs[i].cindex)
                        inputs[i].v.text = str(round(v, 8))
            elif framev < -incv:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        v = (objs[i].v + incv)/(1+(objs[i].v*incv)) 
                        objs[i] = Obj(objs[i].n, i, objs[i].x, v, objs[i].cindex)
                        inputs[i].v.text = str(round(v, 8))
            else:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        v = (objs[i].v - framev)/(1+(objs[i].v*-framev)) 
                        objs[i] = Obj(objs[i].n, i, objs[i].x, v, objs[i].cindex)
                        inputs[i].v.text = str(round(v, 8))
        else:
            state = None

class Button: 
    def __init__(self, btype, parent = None):
        if btype == 'add':
            self.rect = pygame.Rect(consize[0] - 100, len(inputs) * 50 +15, 70, 40)
        if btype == 'send':
            self.rect = pygame.Rect(consize[0] - 100, len(inputs) * 50 +15, 70, 40)
        if btype == 'ok':
            self.rect = pygame.Rect(errsize[0]/2, errsize[1]/2, 140, 40)
        #close button
        if btype == 'x':
            self.rect = pygame.Rect(consize[0]-30, len(inputs)*50+10,  20, 20)
        self.btype = btype
        self.color = inactive
        self.text = btype
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.buttontype = btype
        self.surf = control.get_rect()
        self.type = btype
        self.parent = parent
        self.i = None 

    def handle(self, event): 
        if self.btype == 'ok':
            mousepos = (pygame.mouse.get_pos()[0]-errpos[0], pygame.mouse.get_pos()[1]-errpos[1])
        else:
            mousepos = (pygame.mouse.get_pos()[0]-conpos[0], pygame.mouse.get_pos()[1]-conpos[1])
        if self.rect.collidepoint(mousepos):
            self.color = active
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.type == 'add':
                    inputs.append(Input())
                    objs.append(Obj())
                    self.rect = pygame.Rect(consize[0] - 100, len(inputs) * 50 +15, 70, 40)
                if self.type == 'send':
                    for i in range(len(sendbuttons)): 
                        if sendbuttons[i] == self:
                            self.parent.enter('click', i) 
                            break
                if self.btype == 'ok': 
                    global err
                    err = None
                if self.btype == 'x':
                    for i in range(len(sendbuttons)): 
                        if delbuttons[i] is self:
                            x = i 
                            break
                    del objs[x]
                    del sendbuttons[x]
                    del inputs[x]
                    del delbuttons[x]
                    buttons[0] = Button('add')
                    for i in range(len(inputs)):
                        inputs[i].n.rect = pygame.Rect(consize[0]-560, i*50+15, 140, 40) 
                        inputs[i].x.rect = pygame.Rect(consize[0]-410, i*50+15, 140, 40) 
                        inputs[i].v.rect = pygame.Rect(consize[0]-260, i*50+15, 140, 40) 
                    for i in range(len(sendbuttons)):
                        sendbuttons[i].rect = pygame.Rect(consize[0] - 100, i * 50 +15, 70, 40)
                    for i in range(len(delbuttons)):
                        delbuttons[i].rect = pygame.Rect(consize[0]-30, i*50+10,  20, 20)
                        if i>=x:
                            objs[i].index -= 1

        else:
            self.color = inactive

    def draw(self):
        if self.btype == 'ok':
            # Blit the text.
            errwin.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pygame.draw.rect(errwin, self.color, self.rect, 2)       # Blit the text.
        elif self.btype == 'x':
            control.blit(self.txt_surface, (self.rect.x+5, self.rect.y-1))
            # Blit the rect.
            pygame.draw.rect(control, self.color, self.rect, 2)
        else:
            control.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pygame.draw.rect(control, self.color, self.rect, 2)

class Input:
    def __init__(self):
        self.n = Box(self, 'n')
        self.x = Box(self, 'x')
        self.v = Box(self, 'v')
        sendbuttons.append(Button('send', self))
        delbuttons.append(Button('x', self))

    def enter(self, event, x): 
        if event == 'click':
            if self.x.text == '' or self.x.text == self.x.textd:
                self.x.val = 0
            else:
                try:
                    self.x.val = float(self.x.text) 
                except:
                    error('char') 
            if self.v.text == '' or self.v.text == self.v.textd:
                self.v.val = 0
                objs[x] = Obj(self.n.text, x, self.x.val*20, self.v.val, x) 
            else:
                try:
                    self.v.val = float(self.v.text)
                    if abs(self.v.val) > 1:
                        error('speed')
                    else:
                        objs[x] = Obj(self.n.text, x, self.x.val*20, self.v.val, x) 
                except:
                    error('char')

class Box():
    def __init__(self, parent, ttype):
        self.parent = parent
        self.type = ttype
        if ttype == 'n':
            x = 560
            self.textd = 'name'
        if ttype == 'x':
            x = 410
            self.textd = 'position'
        if ttype == 'v':
            x = 260
            self.textd = 'speed'
        self.text = self.textd
        self.rect = pygame.Rect(consize[0]-x, len(inputs)*50+15, 140, 40) 
        self.color = inactive
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False
        self.color = inactive
        

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = (pygame.mouse.get_pos()[0]-conpos[0], pygame.mouse.get_pos()[1]-conpos[1])
            if self.rect.collidepoint(mousepos):
                if self.text == self.textd:
                    self.active = True
                    self.text = ''
                else:
                    self.active = True
            else:
                self.active = False
                if self.text == '':
                    self.text = self.textd
            self.color = active if self.active else inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color) 

    def draw(self, surf):
        self.txt_surface = FONT.render(str(self.text), True, self.color)
        # Blit the text.
        surf.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(surf, self.color, self.rect, 2)

class Obj:
    def __init__(self, n = '', i = None, x = 0, v = 0, ci = 0): 
        if n == 'name':
            self.n = ''
        else:
            self.n = n
        self.x = x 
        self.v = v
        if ci < 0:
            self.cindex = 0
        else:
            self.cindex = ci%len(inactiveline)
        if i < 0:
            self.index = 0
        else:
            self.index = i
        self.angle = -deg(atan(v))
        self.rotated = rotate(inactiveline[self.cindex], self.angle)
        self.rect = self.rotated.get_rect() 
        self.drawpos = [graphsize[0]/2+x-self.rect.w/2, graphsize[1]/2-self.rect.h/2] 
        self.active = False
        self.tickpos = []
        if self.angle < 0:
            pos = [self.drawpos[0]+self.rect.w, self.drawpos[1]]
        else:
            pos = [self.drawpos[0], self.drawpos[1]]
        if abs(self.v) != 1:
            self.xline = []
            self.xlinepos = []
            xlineangle = 90 - self.angle
            self.xline.append(rotate(inactiveline[self.cindex], xlineangle))
            xcut = pos[0]+ (self.rect.h/2.0)*tan(pi*self.angle/180.0)
            for line in self.xline:
                rec = line.get_rect()
                self.xlinepos.append([xcut-(rec.w/2), (graphsize[1]/2)-rec.h/2])
       
            timetick = 10/root(1-v**2) 
            self.tickpos.append([xcut, pos[1] + self.rect.h/2]) 
            for i in range(1, 50):
                a = (-1)**i
                xfac = sin(self.angle*pi/180)*i*a*timetick
                yfac = cos(self.angle*pi/180)*i*a*timetick
                self.tickpos.append([self.tickpos[0][0]+xfac, self.tickpos[0][1]+yfac]) 
            for i in range(1, 50):
                a = (-1)**i
                yfac = sin(self.angle*pi/180)*i*a*timetick
                xfac = cos(self.angle*pi/180)*i*a*timetick
                self.tickpos.append([self.tickpos[0][0]+xfac, self.tickpos[0][1]+yfac])
                #grid
        else:
            self.xline = None
        s = 10-pos[1]
        x = pos[0]+ s*tan(pi*self.angle/180.0)
        self.nrect = pygame.Rect(x+5, 10, len(self.n)*20, 20) 
        self.n_surface = fontobj.render(self.n, True, black)
        #check for collision with other names, lines, out of frame, t label

    def draw(self):
        graph.blit(self.n_surface, (self.nrect.x+4, self.nrect.y+2))
        #pygame.draw.rect(graph, black, self.nrect, 2)
        if self.active:
            self.rotated = rotate(activeline[self.cindex], self.angle)
            self.ttick = rotate(activetick, self.angle)
            self.xtick = rotate(activetick, 90 - self.angle)
        else:
            self.rotated = rotate(inactiveline[self.cindex], self.angle)
            self.ttick = rotate(inactivetick, self.angle)
            self.xtick = rotate(activetick, 90 - self.angle)
        for i in range(len(self.tickpos)):
            if i < 50:
                graph.blit(self.ttick, self.tickpos[i])
            else:
                graph.blit(self.xtick, self.tickpos[i])
        graph.blit(self.rotated, self.drawpos)
        if self.xline != None:
            for i in range(len(self.xline)):
                graph.blit(self.xline[i], self.xlinepos[i])

    def handle(self, event):
        mousepos = (pygame.mouse.get_pos()[0]-graphpos[0], pygame.mouse.get_pos()[1]-graphpos[1])
        if self.angle > 0:
            valmin = (mousepos[0]-10.0 - self.drawpos[0])/(mousepos[1] - self.drawpos[1])
            valmax = (mousepos[0]+10.0 - self.drawpos[0])/(mousepos[1] - self.drawpos[1])
            if deg(atan(valmin)) < self.angle and deg(atan(valmax)) > self.angle:
                self.active = True
                #draw raster
                if event.type == pygame.MOUSEBUTTONDOWN:
                    change(self.index)
            else:
                self.active = False
        else:
            valmin = (mousepos[0]-10.0 - (self.drawpos[0]+self.rect.w))/(mousepos[1] - self.drawpos[1])
            valmax = (mousepos[0] +10.0 - (self.drawpos[0]+self.rect.w))/(mousepos[1] - self.drawpos[1]) 
            if deg(atan(valmin)) < self.angle and deg(atan(valmax)) > self.angle:
                self.active = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(objs)):
                        if objs[i] == self:
                            change(i)
                            break
            else:
                self.active = False

inputs.append(Input())
buttons.append(Button('add'))
objs.append(Obj())

#main loop
while running:
    starttime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in sendbuttons:
            button.handle(event)
        for button in buttons:
            button.handle(event)
        for button in delbuttons:
            button.handle(event)
        for inputbox in inputs:
            inputbox.n.handle(event)
            inputbox.x.handle(event)
            inputbox.v.handle(event)
            
        for obj in objs:
            if isinstance(obj, Obj):
                obj.handle(event)

    graph.blit(xaxis, [0, graphsize[1]/2])
    for tick in xticks:
        graph.blit(tick[0], tick[1])
    graph.blit(yaxis, [graphsize[0]/2, 0])
    for tick in yticks:
        graph.blit(tick[0], tick[1])
    if state != None:
        change(state)
    #draw here
    for button in sendbuttons:
        button.draw()
    for button in delbuttons:
        button.draw()
    for button in buttons:
        button.draw()
    for inputbox in inputs:
        inputbox.n.draw(control)
        inputbox.x.draw(control)
        inputbox.v.draw(control)
    for obj in objs:
        if isinstance(obj, Obj):
            obj.draw()
    graph.blit(txt_t, (txt_t_rect.x, txt_t_rect.y))
    graph.blit(txt_ct, (txt_ct_rect.x, txt_ct_rect.y))

    win.blit(graph, graphpos)
    win.blit(control, conpos)
    if err != None:
        error(err)
        win.blit(errwin, errpos)
    pygame.display.update()
    control.fill(white)
    graph.fill(white)
    errwin.fill(white)
    win.fill(grey)
    clock.tick(30)
    endtime = time.time() 
pygame.quit()
