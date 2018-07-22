import pygame as pg
from pygame.locals import *


class Pong(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerX = int(screensize[0]*0.5)
        self.centerY = int(screensize[1]*0.5)
        self.radius = 8
        self.rect = pg.Rect(self.centerX-self.radius,
                            self.centerY-self.radius,
                            self.radius*2, self.radius*2)
        self.color = (0, 0, 0)
        self.direction = [1, 1]
        self.speedX = 2
        self.speedY = 5

        self.hit_edge_left = False
        self.hit_edge_right = False
        
    def update(self, player_paddle, ai_paddle):
        self.centerX += self.direction[0]*self.speedX
        self.centerY += self.direction[1]*self.speedY
        self.rect.center = (self.centerX, self.centerY)

        #ball boundaries for top and bottom of window
        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        #check collision between ball and paddle
        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

    def render(self, screen):
         pg.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
         pg.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius, 1)


class AIPaddle(object):
     def __init__(self, screensize):
         self.screensize = screensize

         self.centerX = 5
         self.centerY = int(screensize[1]*0.5)
         self.height = 100
         self.width = 10
         self.speed = 5

         self.rect = pg.Rect(0, self.centerY - int(self.height*0.5), self.width, self.height)
         self.color = (100, 255, 100)

     def update(self, pong):
         #window boundaries for paddle
         if pong.rect.top < self.rect.top:
             self.centerY -= self.speed
         elif pong.rect.bottom > self.rect.bottom:
             self.centerY += self.speed

         self.rect.center = (self.centerX, self.centerY)
         
     def render(self, screen):
         pg.draw.rect(screen, self.color, self.rect, 0)
         pg.draw.rect(screen, (0, 0, 0), self.rect, 1)


class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerX = screensize[0]-5
        self.centerY = int(screensize[1] * 0.5)
        self.height = 100
        self.width = 10
        self.speed = 4
        self.direction = 0

        self.rect = pg.Rect(0, self.centerY - int(self.height * 0.5), self.width, self.height)
        self.color = (0, 139, 139)

    def update(self):
        self.centerY += self.direction*self.speed
        self.rect.center = (self.centerX, self.centerY)

        #window boundaries for paddle
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
        pg.draw.rect(screen, (0, 0, 0), self.rect, 1)


def main():
    pg.init()
    screensize = (640, 480)
    screen = pg.display.set_mode(screensize)
    clock = pg.time.Clock()

    pg.mixer.music.load('PongSong.mp3')
    pg.mixer.music.play()

    pong = Pong(screensize)
    aiPaddle = AIPaddle(screensize)
    playerPaddle = PlayerPaddle(screensize)

    running = True
    while running:
        clock.tick(64)

        #event handling
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

            #keys
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    playerPaddle.direction = -1
                elif event.key == K_DOWN:
                    playerPaddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and playerPaddle.direction == -1:
                    playerPaddle.direction = 0
                elif event.key == K_DOWN and playerPaddle.direction == 1:
                        playerPaddle.direction = 0

        #update
        aiPaddle.update(pong)
        playerPaddle.update()
        pong.update(playerPaddle, aiPaddle)

        if pong.hit_edge_left:
            print("You Won")
            running = False
        elif pong.hit_edge_right:
            print("You Lose")
            running = False

        #render
        screen.fill((255, 182, 193))
        aiPaddle.render(screen)
        playerPaddle.render(screen)
        pong.render(screen)
        pg.display.flip()

    pg.quit()


main()
