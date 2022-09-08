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
        self.image_fish = pygame.image.load('images/fish_on_plate.png')
        self.image_empty = pygame.image.load('images/empty_plate.png')
        
        self.image = self.image_fish
        self.rect = self.image.get_rect()
        self.plate_empty = True
        self.time_empty = 0
        
        # The plate appears at the cormer of the board.
        # self.rect.left = self.screen_rect.left + self.settings.border_width
    
        # The plate appears at the center of the board.
        self.rect.left = self.screen_rect.left + 300
        self.rect.top = self.screen_rect.top + 100
        
        self.name = 'plate'
        
    def empty(self):
        """Image of the plate changes to empty"""
        
        self.image = self.image_empty
        # Get timestamp when the plate's emptied in seconds
        self.time_empty = time.time()        
    
    def check_refill(self):
        """Refill the plate if it's empty"""
        
        if time.time() - self.time_empty >= 5:
            self.image = self.image_fish        
        