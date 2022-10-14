import pygame
from pygame.sprite import Sprite

class Bed(Sprite):
    """Create a cat's bed"""
    
    def __init__(self, cl_game, groups):
        """Initialize a bed"""
        
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings 
        
        # Uploads image of bed and gets rectangle.
        self.image_bed = pygame.image.load(self.settings.cat_bed_image[0])
        
        self.image = self.image_bed
        self.rect = self.image.get_rect()
        
        # The bed appears at the corner of the board.
        self.rect.right = self.screen_rect.right
        
        self.name = 'bed'