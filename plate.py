import pygame
from pygame.sprite import Sprite

class Plate(Sprite):
    """Create a plate"""
    
    def __init__(self, cl_game, groups):
        """Initialize a plate"""
        
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings 
        
        # Uploads an empty plate and gets rectangle.
        self.image = pygame.image.load('images/fish_on_plate.png')
        self.rect = self.image.get_rect()
        self.plate_empty = True
        
        # The plate appears at the cormer of the board.
        # self.rect.left = self.screen_rect.left + self.settings.border_width
    
        # The plate appears at the center of the board.
        self.rect.left = self.screen_rect.left + 300
        self.rect.top = self.screen_rect.top + 100