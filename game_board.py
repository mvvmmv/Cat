import pygame

class GameBoard():
    """Draw borders"""
    
    def __init__(self, cl_game):
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings
        self.color = self.settings.border_color
        self.bg_color = self.settings.bg_color
        
        # Create vertical and horizontal lines
        self.rect_vert = pygame.Rect(self.settings.border_width, 0, 2, 
                            self.settings.screen_height - self.settings.border_width)
        self.rect_horiz = pygame.Rect(self.settings.border_width, 
                            self.settings.screen_height - self.settings.border_width, 
                            self.settings.screen_width - self.settings.border_width, 2)
             
    def draw_lines(self):
        """Draw lines"""
        pygame.draw.rect(self.screen, self.color, self.rect_horiz)        
        pygame.draw.rect(self.screen, self.color, self.rect_vert)