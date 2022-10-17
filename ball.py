import pygame
from pygame.sprite import Sprite
import time

class Ball(Sprite):
    """Create a ball"""
    
    def __init__(self, cl_game, groups, obstacles):
        """Initialize a ball"""
        
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()
        self.settings = cl_game.settings 
        self.obstacles = obstacles
        
        # Uploads image of ball and gets rectangle.
        self.image_ball = pygame.image.load(self.settings.ball_image[0])
        
        self.image = self.image_ball
        self.rect = self.image.get_rect()
        
        # The ball appears at the corner of the board.
        self.rect.right = self.screen_rect.left+200
        self.rect.bottom = self.screen_rect.top+300
        
        self.pos = pygame.math.Vector2(self.rect.right,self.rect.bottom)
        self.direction = pygame.math.Vector2()

        self.time_kick = time.time()
        self.name = 'ball'
    
    def kick(self, direction):
        
        # starts timer
        self.time_kick = time.time()
        if direction == 'right':
            self.direction.x = -1
        if direction == 'left':
            self.direction.x = 1      
    
    def update(self):
        """Update location of the ball"""
        
        self.old_rect = self.rect
        # Update position of the ball only for some time
        # Because it should stop eventually
        if time.time() - self.time_kick < 1:
            self.pos.x += self.direction.x
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
        
    def collision(self, direction):
        """Check collisions with the obstacles"""

        print('checknig collisions')
        collision_sprites = pygame.sprite.spritecollide(
            self, self.obstacles, False)
        print('collision_sprites',collision_sprites)

        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    print('checking collision on the right', sprite)
                    #if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                    if self.rect.right >= sprite.rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        print('collision on the right, changing direction')
                        self.direction.x = self.direction.x * -1

                    # collision on the left
                    print('checking collision on the left', sprite)
                    print('sprite.rect.right', sprite.rect.right, 'self.rect.left', self.rect.left, 'self.old_rect.left', self.old_rect.left)
                    if self.rect.left <= sprite.rect.right:
                    #if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        print('collision on the left, changing direction')
                        self.direction.x = self.direction.x * -1 