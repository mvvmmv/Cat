import sys
import pygame
from cat import Cat

class CatLive:
    """Class for managing cat's life"""
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((600,400))
        
        pygame.display.set_caption("Cat's life")
        
        self.cat = Cat(self)
    
    def run_game(self):
        """Run main cicle of the game"""
        while True:
            self._check_events()
    
    def _check_events(self):
        """Handles keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == '__main__':
    # Create instance and run the game.
    cl = CatLive()
    cl.run_game()