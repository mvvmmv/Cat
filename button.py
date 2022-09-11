import pygame
from pygame.sprite import Sprite

class Button(Sprite):
    """Set up button"""
    
    def __init__(self, cl_game, images_of_button, pos, groups):
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings
        self.pos = pos
        
        self.images = []
        
        # Uploads images for the button.
        for i in range(len(images_of_button)):
            self.images.append(pygame.image.load(images_of_button[i]))
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        self.rect.left = self.screen_rect.left + pos[0]
        self.rect.top = self.screen_rect.top + pos[1]