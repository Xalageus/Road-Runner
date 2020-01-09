import pygame
from pygame.locals import *

class player(pygame.sprite.Sprite):
    def __init__(self, obj_file, xPos, yPos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(obj_file)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 2, self.image.get_size()[1] * 2))
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()
        
        self.speedX = 0.13
        self.xPos = xPos
        self.yPos = yPos

    def moveLeft(self, time):
        self.xPos = self.xPos - (self.speedX * time)

    def moveRight(self, time):
        self.xPos = self.xPos + (self.speedX * time)

    def moveLeftAxis(self, mod, time):
        if(mod < -0.99):
            self.moveLeft(time)
        else:
            self.xPos = self.xPos - (self.speedX * (abs(mod) * time))

    def moveRightAxis(self, mod, time):
        if(mod > 0.99):
            self.moveRight(time)
        else:
            self.xPos = self.xPos + (self.speedX * (abs(mod) * time))