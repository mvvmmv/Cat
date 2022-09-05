import sys
import pygame

from cat import Cat
from game_board import GameBoard
from settings import Settings

class CatLive:
    """Class for managing cat's life"""
    
    def __init__(self):
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        
        pygame.display.set_caption("Cat's life")
        
        self.cat = Cat(self)
        self.gb = GameBoard(self)
    
    def run_game(self):
        """Run main cicle of the game"""
        while True:
            self._check_events()
            self.cat.update()
            self._update_screen()
            
    def _check_events(self):
        """Handles keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)
                
    def _check_key_down_events(self, event):
        """Reacts to keyboard button down events"""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        elif event.key == pygame.K_UP:
            self.cat.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.cat.moving_down = True
    
    def _check_key_up_events(self, event):
        """Reacts to keyboard button up events"""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        if event.key == pygame.K_LEFT:
            self.cat.moving_left = False
        if event.key == pygame.K_UP:
            self.cat.moving_up = False
        if event.key == pygame.K_DOWN:
            self.cat.moving_down = False
            
    def _update_screen(self):
        """Updates screen"""
        self.screen.fill(self.settings.bg_color)
        self.cat.blitme()
        self.gb.draw_lines()
        
        pygame.display.flip()
        
if __name__ == '__main__':
    # Create instance and run the game.
    cl = CatLive()
    cl.run_game()