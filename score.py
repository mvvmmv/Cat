import time, datetime, pygame

class Score():
    """Set up Score"""
    
    def __init__(self, cl_game, cat):
        self.font = pygame.font.Font(None, 30)
        self.screen = cl_game.screen
        self.cat = cat
        self.score = self.font.render(str(0), True, 'blue')
        self.score_value = 0
    
    def update(self):
        """Draw the score"""
        
        self.score_value = self.cat.fish_eaten
        self.score = self.font.render(str(self.score_value), True, 'blue')
        self.screen.blit(self.score, (10,30))