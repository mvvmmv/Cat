import time, datetime, pygame

class Clock():
    """Set up time"""
    
    def __init__(self, cl_game):
        date_time = datetime.datetime.fromtimestamp(time.time())
        self.font = pygame.font.Font(None, 30)
        self.clock = self.font.render(date_time.strftime("%H:%M:%S"), True, '#3d5052')
        self.screen = cl_game.screen
    
    def update(self):
        """Draw the time"""
        
        date_time = datetime.datetime.fromtimestamp(time.time())
        self.clock = self.font.render(date_time.strftime("%H:%M:%S"), True, '#3d5052')
        self.screen.blit(self.clock, (10,10))