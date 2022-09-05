import pygame

class Cat():
    """Create a cat"""
    def __init__(self, cl_game):
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        
        self.settings = cl_game.settings
        
        # Uploads cat looking left image and gets rectangle.
        self.image = pygame.image.load('images/cat.png')
        self.rect = self.image.get_rect()
        
        # Uploads cat looking right image and gets rectangle.
        self.image_right = pygame.image.load('images/cat_inverse.png')
        # self.rect_right = self.image_right.get_rect()
        
        # The cat appears at the buttom of the screen.
        self.rect.center = self.screen_rect.center
        
        # Saving coordinates of the cat's center.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Relocation flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.cat_looks_right = False
    
    def blitme(self):
        """Draw the cat at the current position"""
        if not self.cat_looks_right:
            self.screen.blit(self.image, self.rect)
        elif self.cat_looks_right:
            self.screen.blit(self.image_right, self.rect)
    
    def update(self):
        """Update location of the cat in regards with flag's value"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.cat_speed
            self.cat_looks_right = True
        
        if self.moving_left and self.rect.left > 100:
            self.x -= self.settings.cat_speed
            self.cat_looks_right = False
        
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.cat_speed
            
        if self.moving_down and self.rect.bottom < self.screen_rect.height - 100:
            self.y += self.settings.cat_speed
        
        # Update attribute rect in regards with self.x, self.y.
        self.rect.x = self.x
        self.rect.y = self.y