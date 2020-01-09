import pygame
from pygame.locals import *

class road(pygame.sprite.Sprite):
    def __init__(self, obj_file, xPos, yPos, flip, obj = None):
        pygame.sprite.Sprite.__init__(self)

        if obj_file == None:
            self.image = obj
            if flip:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load(obj_file)
            if flip:
                self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 2, self.image.get_size()[1] * 2))
        self.rect = self.image.get_rect()
        
        self.xPos = xPos
        self.yPos = yPos

    def copy(self, xPos, yPos, flip):
        return road(None, xPos, yPos, flip, obj=self.image.copy())