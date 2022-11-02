import pygame
from pygame.sprite import Sprite

class Border(Sprite):
    """Class for borders"""
    
    def __init__(self,pos,size,groups,color):
        super().__init__(groups)    
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.name = 'boarder '+str(self.rect.topleft)