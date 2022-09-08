import time, datetime, pygame

class Clock():
    """Set up clock"""
    def __init__(self, cl_game):
        date_time = datetime.datetime.fromtimestamp(time.time())
        self.font = pygame.font.Font(None, 30)
        self.clock = self.font.render(date_time.strftime("%H:%M:%S"), True, 'blue')
        self.screen = cl_game.screen
    
    def update(self):
        date_time = datetime.datetime.fromtimestamp(time.time())
        self.clock = self.font.render(date_time.strftime("%H:%M:%S"), True, 'blue')
        self.screen.blit(self.clock, (10,10))