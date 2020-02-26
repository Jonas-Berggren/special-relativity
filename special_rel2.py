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
txt_colors = [black, [255, 0, 0], [0, 0, 255], [0, 255, 0], [255, 122, 0], [255, 255, 0], [255, 0, 255], [0, 255, 255], [112, 77, 57], grey]
#globals
#winsize = (1800, 900)
graphsize = (800, 800)
consize = (800, 800)
boxsize = (400, 400)
errsize = (400, 400)
winsize = pygame.display.Info()
winsize = winsize.masks
winsize = (int(winsize[0]/9300), int(winsize[1]/73))

print winsize
#win = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
#win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
win = pygame.display.set_mode(winsize, 0, 32)#use idsplaysize

graph = pygame.Surface(graphsize)
control = pygame.Surface(consize)
errwin = pygame.Surface(errsize)   
running = True
img = pygame.image.load
inactiveline = [img('inactiveline_black.png'), img('inactiveline_red.png'), img('inactiveline_blue.png'), img('inactiveline_green.png'), img('inactiveline_orange.png'), img('inactiveline_yellow.png'), img('inactiveline_purple.png'), img('inactiveline_turq.png'), img('inactiveline_brown.png'), img('inactiveline_grey.png')]
activeline = [img('activeline_black.png'), img('activeline_red.png'), img('activeline_blue.png'), img('activeline_green.png'), img('activeline_orange.png'), img('activeline_yellow.png'), img('activeline_purple.png'), img('activeline_turq.png'), img('activeline_brown.png'), img('activeline_grey.png')]
inactivetick = pygame.image.load('inactivetick.png')
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
txt_t_rect = pygame.Rect(graphsize[0]/2 + 20, 20, 40, 40)
txt_ct_rect = pygame.Rect(graphsize[0] - 40, graphsize[1]/2 + 20, 40, 40)
increment = 0.1
err = None
incx = 1.0
incv = 0.01

#lists
objs = []
buttons = []
sendbuttons = []
inputs = []
delbuttons = []

xaxis = rotate(inactiveline[0], 90)
xticks = []
for i in range(int(graphsize[0] / 40)):
    xticks.append((rotate(inactivetick, 90), (i*40, graphsize[1]/2)))
yaxis = inactiveline[0]
yticks = []
for i in range(int(graphsize[1] / 40)):
    yticks.append((inactivetick, (graphsize[0]/2, i*40)))

def error(m):
    global err 
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
        buttons.append(Button('ok'))

def change(f):
    global state
    framex = objs[f].x
    framev = objs[f].v
    framet = objs[f].t
    state = f
    a = objs[f].angle
    if abs(objs[f].v) == 1: 
        error('frame')
        state = None
    else:
        if framex != 0:
            if framex > incx:
                for i in range(len(objs)):
                    x = objs[i].x - incx
                    t = objs[i].t - incx*tan(a*pi/180)
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex, t)
                    inputs[i].x.text = str(round(x/20, 8)) 
            elif framex < -incx:
                for i in range(len(objs)):
                    x = objs[i].x + incx
                    t = objs[i].t + incx*tan(a*pi/180)
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex, t)
                    inputs[i].x.text = str(round(x/20, 8))
            else:
                for i in range(len(objs)):
                    x = objs[i].x - framex
                    t = objs[i].t - framex*tan(a*pi/180)
                    objs[i] = Obj(objs[i].n, i, x, objs[i].v, objs[i].cindex, t)
                    inputs[i].x.text = str(round(x/20, 8))
        elif framev != 0:
            if framev > incv:
                for i in range(len(objs)):
                    if abs(objs[i].v) !=1:
                        v = (objs[i].v - incv)/(1+(objs[i].v*-incv))
                        t = 1/root(1-incv**2)*(objs[i].t+incv*objs[i].x)
                        x = 1/root(1-incv**2)*(objs[i].x+incv*objs[i].t)
                        objs[i] = Obj(objs[i].n, i, x, v, objs[i].cindex, t)
                        inputs[i].v.text = str(round(v, 8))
            elif framev < -incv:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        v = (objs[i].v + incv)/(1+(objs[i].v*incv)) 
                        t = 1/root(1-incv**2)*(objs[i].t - incv * objs[i].x)
                        x = 1/root(1-incv**2)*(objs[i].x-incv*objs[i].t)
                        objs[i] = Obj(objs[i].n, i, x, v, objs[i].cindex, t)
                        objs[i] = Obj(objs[i].n, i, x, v, objs[i].cindex, t)
                        inputs[i].v.text = str(round(v, 8))
            else:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        v = (objs[i].v - framev)/(1+(objs[i].v*-framev)) 
                        t = 1/root(1-incv**2)*(objs[i].t+framev*objs[i].x)
                        x = 1/root(1-incv**2)*(objs[i].x+framev*objs[i].t)
                        objs[i] = Obj(objs[i].n, i, x, v, objs[i].cindex, t) 
                        objs[i] = Obj(objs[i].n, i, x, v, objs[i].cindex, t)
                        inputs[i].v.text = str(round(v, 8))
        elif framet != 0:
            if framet > incx:
                for i in range(len(objs)):
                    if abs(objs[i].v) !=1:
                        t = objs[i].t - incx
                        objs[i] = Obj(objs[i].n, i, objs[i].x, objs[i].v, objs[i].cindex, t)
            elif framet < -incx:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        t = objs[i].t + incx
                        objs[i] = Obj(objs[i].n, i, objs[i].x, objs[i].v, objs[i].cindex, t)
            else:
                for i in range(len(objs)):
                    if abs(objs[i].v) != 1:
                        t = objs[i].t - framet 
                        objs[i] = Obj(objs[i].n, i, objs[i].x, objs[i].v, objs[i].cindex, t)
        else:
            state = None
    objs[f].active = True

class Button: 
    def __init__(self, btype, parent = None):
        if btype == 'add':
            self.rect = pygame.Rect(consize[0] - 100, len(inputs) * 50 +15, 70, 40)
        if btype == 'send':
            self.rect = pygame.Rect(consize[0] - 100, len(inputs) * 50 +15, 70, 40)
        if btype == 'ok':
            self.rect = pygame.Rect(errsize[0]/2, errsize[1]/2, 140, 40)
        if btype == 'x':
            self.rect = pygame.Rect(consize[0]-30, len(inputs)*50+10,  20, 20) 
        self.color = inactive
        self.txt = FONT.render(btype, True, self.color)
        self.buttontype = btype
        self.surf = control.get_rect()
        self.type = btype
        self.parent = parent
        self.i = None 

    def handle(self, event): 
        if self.type == 'ok':
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
                if self.type == 'ok': 
                    global err
                    err = None
                if self.type == 'x':
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
        if self.type == 'ok':
            errwin.blit(self.txt, (self.rect.x+5, self.rect.y+5))
            pygame.draw.rect(errwin, self.color, self.rect, 2)
        elif self.type == 'x':
            control.blit(self.txt, (self.rect.x+5, self.rect.y-1))
            pygame.draw.rect(control, self.color, self.rect, 2)
        else:
            control.blit(self.txt, (self.rect.x+5, self.rect.y+5))
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
            ok = True
            xval, vval = 0, 0
            if self.x.text != '' and self.x.text != self.x.textd:
                xval = self.x.text
            if self.v.text != '' and self.v.text != self.v.textd:
                vval = self.v.text 
            try:
                xval = float(xval)
                vval = float(vval)
            except:
                error('char')
                ok = False
            if ok and abs(vval) > 1:
                error('speed')
                ok = False
            if ok:
                objs[x] = Obj(self.n.text, x, xval*20, vval, x) 

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
        surf.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(surf, self.color, self.rect, 2)

class Obj:
    def __init__(self, n = '', i = None, x = 0, v = 0, ci = 0, t = 0):
        if n == 'name':
            self.n = ''
        else:
            self.n = n
        self.x = x 
        self.v = v
        self.t = t 
        if ci < 0:
            self.cindex = 0
        else:
            self.cindex = ci%len(inactiveline)
        if i < 0:
            self.index = 0
        else:
            self.index = i
        self.angle = -deg(atan(v))
        self.line = rotate(inactiveline[self.cindex], self.angle)
        self.rect = self.line.get_rect()
        self.linepos = [[graphsize[0]/2+x-self.rect.w/2, (graphsize[1]/2-self.rect.h/2)+t]]
        self.active = False
        if self.angle < 0:
            pos = [self.linepos[0][0]+self.rect.w, self.linepos[0][1]]
        else:
            pos = [self.linepos[0][0], self.linepos[0][1]]
        if abs(self.v) != 1:
            xcut = pos[0]+ (self.rect.h/2.0)*tan(pi*self.angle/180.0)
            self.ttick = rotate(inactivetick, self.angle)
            self.xtick = rotate(inactivetick, 90 - self.angle)
            xlineangle = 90 - self.angle
            self.xline = rotate(inactiveline[self.cindex], xlineangle)
            rect = self.xline.get_rect()
            self.xlinepos = [[xcut-rect.w/2.0, pos[1]+(self.rect.h-rect.h)/2.0]]  
            timetick = 40/root(1-v**2) 
            self.tickpos = [[xcut, pos[1] + self.rect.h/2]]
            for i in range(1, 50):
                yfac = sin(self.angle*pi/180)*i*timetick
                xfac = cos(self.angle*pi/180)*i*timetick
                self.tickpos.append([self.tickpos[0][0]+xfac, self.tickpos[0][1]+yfac])
                self.tickpos.append([self.tickpos[0][0]+yfac, self.tickpos[0][1]+xfac]) 
                self.tickpos.append([self.tickpos[0][0]-xfac, self.tickpos[0][1]-yfac])
                self.tickpos.append([self.tickpos[0][0]-yfac, self.tickpos[0][1]-xfac]) 
            for i in range(1,100):
                xfac = cos(self.angle*pi/180)*i*timetick
                yfac = sin(self.angle*pi/180)*i*timetick
                self.xlinepos.append([self.xlinepos[0][0]+yfac,self.xlinepos[0][1]+xfac])
                self.xlinepos.append([self.xlinepos[0][0]-yfac,self.xlinepos[0][1]-xfac])
                self.linepos.append([self.linepos[0][0]+xfac, self.linepos[0][1]+yfac])
                self.linepos.append([self.linepos[0][0]-xfac, self.linepos[0][1]-yfac])
        else:
            self.xline = None
        s = 10-pos[1]
        x = pos[0]+ s*tan(pi*self.angle/180.0)
        self.nrect = pygame.Rect(x+5, 10, len(self.n)*10+5, 20) 
        self.n_surface = fontobj.render(self.n, True, txt_colors[self.cindex])
        while self.nrect.x + self.nrect.w > graphsize[0] or self.nrect.x < 0:
            y = self.nrect.y + 5
            s = y - pos[1]
            x = pos[0]+ s*tan(pi*self.angle/180.0)
            self.nrect = pygame.Rect(x+5, y, len(self.n)*10+5, 20) 
            self.n_surface = fontobj.render(self.n, True, txt_colors[self.cindex])
        problem = True
        while problem:
            problem = False
            for i in range(self.index):
                if objs[i].nrect.colliderect(self.nrect):
                    problem = True
                    y = self.nrect.y + 30
                    s = y - pos[1]
                    x = pos[0]+ s*tan(pi*self.angle/180.0)
                    self.nrect = pygame.Rect(x+5, y, len(self.n)*10+5, 20) 

    def draw(self):
        if self.active:
            self.line = rotate(activeline[self.cindex], self.angle)
        else:
            self.line = rotate(inactiveline[self.cindex], self.angle)
        for i in range(len(self.tickpos)):
            if i%2 == 0:
                graph.blit(self.ttick, self.tickpos[i])
            else:
                graph.blit(self.xtick, self.tickpos[i])
        if self.xline != None:
            if self.active:
                for pos in self.xlinepos:
                    graph.blit(self.xline, pos)
                first = True
                for pos in self.linepos:
                    graph.blit(self.line, pos) 
                    if first:
                        self.line = rotate(inactiveline[self.cindex], self.angle)
                        first = False

            else:
                graph.blit(self.line, self.linepos[0])
                graph.blit(self.xline, self.xlinepos[0])
        pygame.draw.rect(graph, white, self.nrect, )
        graph.blit(self.n_surface, (self.nrect.x+4, self.nrect.y+2))
        

    def handle(self, event):
        mousepos = (pygame.mouse.get_pos()[0]-graphpos[0], pygame.mouse.get_pos()[1]-graphpos[1])
        if self.angle > 0:
            valmin = (mousepos[0]-10.0 - self.linepos[0][0])/(mousepos[1] - self.linepos[0][1])
            valmax = (mousepos[0]+10.0 - self.linepos[0][0])/(mousepos[1] - self.linepos[0][1])
            if deg(atan(valmin)) < self.angle and deg(atan(valmax)) > self.angle:
                self.active = True 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    change(self.index)
            else:
                self.active = False
        else:
            valmin = (mousepos[0]-10.0 - (self.linepos[0][0]+self.rect.w))/(mousepos[1] - self.linepos[0][1])
            valmax = (mousepos[0] +10.0 - (self.linepos[0][0]+self.rect.w))/(mousepos[1] - self.linepos[0][1]) 
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
pygame.quit()
