import pygame
from pygame.locals import *

class road(pygame.sprite.Sprite):
    def __init__(self, obj_file, xPos, yPos, flip):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(obj_file)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 2, self.image.get_size()[1] * 2))
        self.rect = self.image.get_rect()
        
        self.xPos = xPos
        self.yPos = yPos