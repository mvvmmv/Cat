import sys, math, time
import pygame

from cat import Cat
from settings import Settings
from plate import Plate
from static_obstacle import StaticObstacle
from clock import Clock
from score import Score

class CatLive:
    """Class for managing cat's life"""
    
    def __init__(self):
        pygame.init()
        
        # Set icon for the game window.
        programIcon = pygame.image.load('images/cat.png')
        pygame.display.set_icon(programIcon)
        
        # Set the game window.
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        
        # Set caption for the game window.
        pygame.display.set_caption("Cat's life")
        
        # Group setup
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Gameboard setup   
        self.left_obstacle = StaticObstacle(
            (0,0),(100, 400), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.right_obstacle = StaticObstacle(
            (699,0),(1, 700), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.bottom_obstacle = StaticObstacle(
            (0,400),(700, 100), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.top_obstacle = StaticObstacle(
            (100,0),(600, 1), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.clock = Clock(self)        
        
        # Sprite setup
        self.plate = Plate(self, [self.all_sprites,self.collision_sprites])
        self.cat = Cat(self, self.all_sprites, self.collision_sprites)
        
        self.score = Score(self, self.cat)
        
     
    def run_game(self): 
        """Run main cycle of the game"""
        
        # loop
        last_time = time.time()
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()
            dt = dt
            print(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
            self.screen.fill(self.settings.bg_color) 
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.plate.check_refill()
            self.cat.meow()
            # display output
            self.clock.update()
            self.score.update()
            pygame.display.update()
            
if __name__ == '__main__':
    # Create instance and run the game.
    cl = CatLive()
    cl.run_game()