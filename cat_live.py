import sys
import pygame
from ball import Ball

from button import Button
from cat import Cat
from settings import Settings
from plate import Plate
from border import Border
from clock import Clock
from score import Score
from bed import Bed

class CatLive:
    """Main class for the CL game"""
    
    def __init__(self):
        pygame.init()
    
        # Game window setup:
        self.settings = Settings()
        # - Set the caption
        pygame.display.set_caption("Cat's life")
        # - Set the icon
        programIcon = pygame.image.load(self.settings.cat_images[0])
        pygame.display.set_icon(programIcon)
        # - Set the size
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        
        # Sprites groups setup
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # Gameboard setup   
        self.initBorders()
        self.clock = Clock(self)
        self.mute_button = Button(self, self.settings.images_of_button, self.settings.mb_pos, self.all_sprites)
                       
        # Game objects setup
        self.plate = Plate(self, [self.all_sprites, self.collision_sprites])
        self.bed = Bed(self, [self.all_sprites])
        self.cat = Cat(self, self.mute_button, self.bed, self.all_sprites, self.collision_sprites)
        self.ball = Ball(self, self.cat, [self.all_sprites, self.collision_sprites], self.collision_sprites)
        
        
        self.score = Score(self, self.cat)



        # Custom events:
        # - Trigger for meow every 5 seconds
        self.MEOW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MEOW, 5000)
        
        # - Animation
        self.ANIMATION = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ANIMATION, 1000)
     
    def initBorders(self):
        self.left_border = Border(
            (0,0),(100, 400), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.right_border = Border(
            (500,0),(500, 600), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.bottom_border = Border(
            (0,350),(550, 400), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
        self.top_border = Border(
            (100,0),(600, 1), [self.all_sprites, self.collision_sprites], 
            self.settings.obst_color)
        
    def run_game(self): 
        """Run main cycle of the game"""
        
        clock = pygame.time.Clock()
        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == self.MEOW:
                    self.cat.meow()   
                if event.type == self.ANIMATION:
                    self.cat.animation()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if self.cat.mute_flag == True:
                            self.cat.mute_button.image = self.cat.mute_button.images[1]
                            self.cat.mute_flag = False
                            break
                        if self.cat.mute_flag == False:
                            self.cat.mute_button.image = self.cat.mute_button.images[0]
                            self.cat.mute_flag = True
                    if event.key == pygame.K_SPACE:
                        self.cat.do()
                    if event.key == pygame.K_a:
                        self.cat.do('right')
                    if event.key == pygame.K_d:
                        self.cat.do('left')
                    if event.key == pygame.K_w:
                        self.cat.do('up')
                    if event.key == pygame.K_s:
                        self.cat.do('down')
                         
                        
            self.screen.fill(self.settings.bg_color)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.plate.check_refill()
            # display output
            self.clock.update()
            self.score.update()
            
            pygame.display.update()
            
            clock.tick(30)
            
if __name__ == '__main__':
    # Create instance and run the game.
    cl = CatLive()
    cl.run_game()