import pygame as pg
import random
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self ,start, dirx=1, diry=0, color=(255,0,0)):
        self.pos = start
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        #position in the grid
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        r = self.pos[0]
        col = self.pos[1]
        #draw in bounds
        pg.draw.rect(surface, self.color, (r*dis+1, col*dis+1, dis-2, dis-2))

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
       #keeps track of which direction snake is moving
        self.dirx = 0
        self.diry = 1

    def move(self):
        #gather user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            #control direction based on input
            keys = pg.key.get_pressed()
            for key in keys:
                if keys[pg.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pg.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pg.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pg.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        #for each cube object, grab its position and verify if its in turn list
        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                #turn at position
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                #once last cube of snake hits the turn, remove the turn
                if i == len(self.body)-1:
                    self.turns.pop(p)
            #If not making a turn/catching a cube, isn't invisible overslapping with eduges
            else:
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirx, c.diry)

    def reset(self, pos):
        self.turns = []
        self.body = []
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry
        #moving right, add cube to left in row
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        #moving left, add cube to right in row
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        #moving below, add cube at the above in col
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        #moving above, add it below in col
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        #draws veritcal and horizontal grid lines - lines method given a start and end position
        pg.draw.line(surface, (255,255,255), (x,0), (x, w))
        pg.draw.line(surface, (255, 255, 255), (0,y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pg.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #get list of positions of snack and see if it overlaps with any of snake's cubes
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    #draw window on top layer
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

    
def main():
    global width, rows, s, snack
    #create window
    width = 500
    #reduce rows to make game harder
    rows = 20
    window = pg.display.set_mode((width, width))

    #instantiate snake object
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))

    flag = True
    clock = pg.time.Clock()
    while flag:
        pg.time.delay(50)
        #ensures game doesn't run more than 10 frames per second
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))

        #check collisions
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('You Lost! ', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(window)


main()


