import pygame
from pygame.sprite import Sprite
import time

class Ball(Sprite):
    """Create a ball"""
    
    def __init__(self, cl_game, cat, groups, obstacles):
        """Initialize a ball"""
        
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings 
        self.obstacles = obstacles
        self.cat = cat
        
        # Uploads image of ball and gets rectangle.
        self.image_ball = pygame.image.load(self.settings.ball_image[0])
        
        self.image = self.image_ball
        self.rect = self.image.get_rect()
        self.old_rect = self.rect.copy()
        
        # The ball appears at the corner of the board.
        self.rect.right = self.screen_rect.left+250
        self.rect.bottom = self.screen_rect.top+300
        
        self.pos = pygame.math.Vector2(self.rect.right,self.rect.bottom)
        self.direction = pygame.math.Vector2()

        self.time_kick = time.time()
        self.name = 'ball'
                
    
    def kick(self, direction):
        '''Set the direction of the ball and starts timer'''
        
        # Starts timer
        self.time_kick = time.time()
        
        # Set the direction
        if direction == 'right':
            self.direction.x = -1
        if direction == 'left':
            self.direction.x = 1      
        if direction == 'up':
            self.direction.y = -1
        if direction == 'down':
            self.direction.y = 1 
    
    def update(self):
        """Update location of the ball"""
    
        # Updates position only if ball's been kicked or met an obstacle
        # and only for <kicked_time> time
            
        self.old_rect = self.rect.copy()
        
        if time.time() - self.time_kick < self.settings.kicked_time:
        
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.pos.x += self.direction.x * self.settings.cat_speed
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.pos.y += self.direction.y * self.settings.cat_speed
            self.rect.y = round(self.pos.y)
            self.collision('vertical')
            
        self.time_update = time.time()

        
    def collision(self, direction):
        """Check collisions with the obstacles or the cat"""

        collision_sprites = pygame.sprite.spritecollide(
            self, self.obstacles, False)

        # If met obstacle - bounce, i.e. change direction to opposite 
        # and keep moving
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction.x = self.direction.x * -1

                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction.x = self.direction.x * -1 
                        
            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction.y = self.direction.y * -1
                            
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y = self.direction.y * -1
        
        # If met cat - stop            
        if pygame.sprite.collide_rect(self, self.cat):
            
            if self.rect.right >= self.cat.rect.left and self.old_rect.right <= self.cat.old_rect.left:
                        self.rect.right = self.cat.rect.left
                        self.pos.x = self.rect.x
            
            if self.rect.left <= self.cat.rect.right and self.old_rect.left >= self.cat.old_rect.right:
                        self.rect.left = self.cat.rect.right
                        self.pos.x = self.rect.x
            
            if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
            
            if self.rect.bottom >= self.cat.rect.top and self.old_rect.bottom <= self.cat.old_rect.top:
                        self.rect.bottom = self.cat.rect.top
                        self.pos.y = self.rect.y            