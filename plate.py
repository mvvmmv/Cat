import time
from turtle import delay
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
        
        # Uploads images of plates and gets rectangle.
        self.image_fish = pygame.image.load(self.settings.plate_images[0])
        self.image_empty = pygame.image.load(self.settings.plate_images[1])
        
        self.image = self.image_fish
        self.rect = self.image.get_rect()
        
        # Properties of the plate
        self.plate_empty = True
        self.time_empty = 0
        self.name = 'plate'
        
        # The plate appears on the board.
        self.rect.left = self.screen_rect.left + (self.settings.screen_width-self.settings.screen_border_width)//2
        self.rect.top = self.screen_rect.top + self.settings.screen_border_width
        
    def empty(self):
        """Changes image of the plate to empty and starts timer"""
        
        self.image = self.image_empty
        # Get timestamp when the plate's emptied in seconds
        self.time_empty = time.time()        
    
    def check_refill(self):
        """Refills the plate if it's empty for <fish_delay> seconds """
        
        if time.time() - self.time_empty >= self.settings.fish_delay:
            self.image = self.image_fish