import pygame
from pygame.sprite import Sprite
from pygame.mixer import Sound
import time
from datetime import datetime


class Cat(Sprite):
    """Create a cat"""

    def __init__(self, cl_game, mute_btn, groups, obstacles):
        """Initialize the cat and define the start location"""
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()

        self.settings = cl_game.settings
        self.mute_button = mute_btn
        self.obstacles = obstacles
        
        # Uploads cat looking left image and gets rectangle.
        self.image_straight = pygame.image.load(self.settings.cat_images[0])
        self.image_straight_m = pygame.image.load(self.settings.cat_images[1])
        self.rect = self.image_straight.get_rect()
        self.image = self.image_straight
        # Uploads cat looking right image and gets rectangle.
        self.image_inverse = pygame.image.load(self.settings.cat_images[2])
        self.image_inverse_m = pygame.image.load(self.settings.cat_images[3])
        # self.rect = self.image_inverse.get_rect()

        # The cat appears at the center of the screen.
        self.rect.center = self.screen_rect.center
        self.old_rect = self.rect.copy()

        # Movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        
        # Sounds
        self.meow_sound = pygame.mixer.Sound('sounds/meow.wav')
                
        # Cat actions counter
        self.fish_eaten = 0       
        self.mute_flag = True # game starts with no sound

    def check_input(self):
        """Handles keyboard and mouse events"""
        
        keys = pygame.key.get_pressed()
               
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
  
    def update(self):
        """Update location of the cat"""
        
        self.old_rect = self.rect.copy()
        #self.check_input(dt)
        self.check_input()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #self.pos.x += self.direction.x * self.settings.cat_speed * dt
        self.pos.x += self.direction.x * self.settings.cat_speed
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        #self.pos.y += self.direction.y * self.settings.cat_speed * dt
        self.pos.y += self.direction.y * self.settings.cat_speed
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

        if self.direction.x == 1:
            self.image = self.image_inverse
        if self.direction.x == -1:
            self.image = self.image_straight

    def collision(self, direction):
        """Check collisions with the obstacles"""
        
        collision_sprites = pygame.sprite.spritecollide(
            self, self.obstacles, False)
        
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                       self.rect.left = sprite.rect.right
                       self.pos.x = self.rect.x
            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                       self.rect.bottom = sprite.rect.top
                       self.pos.y = self.rect.y

    def do(self):
        """Cat actions: eat the fish
        """
        for obstacle in self.obstacles:
            if obstacle.name == 'plate':
                # Checking if the cat vertical center is in [between obstacle's vertical center 
                # - self.settings.free_y, between obstacle's vertical center + self.settings.free_y]
                center_y_check = self.rect.centery in range(obstacle.rect.centery - self.settings.free_y, \
                                                            obstacle.rect.centery + self.settings.free_y)
                if (obstacle.rect.right + 5 >= self.rect.left and \
                    obstacle.rect.right < self.rect.right and  center_y_check \
                        # checking if cat look left
                        and self.image == self.image_straight \
                        and obstacle.image == obstacle.image_fish) \
                        or \
                        (obstacle.rect.left - 5 <= self.rect.right and \
                            obstacle.rect.left > self.rect.left and center_y_check \
                        # checking if cat look right
                        and self.image == self.image_inverse \
                        and obstacle.image == obstacle.image_fish):
                    obstacle.empty()
                    self.fish_eaten += 1                
    
    def meow(self):
        """Makes meow sounds"""
        self.meow_sound.play()
    
    def animation(self):
        if self.image == self.image_straight:
            self.image = self.image_straight_m
        elif self.image == self.image_straight_m :
            self.image = self.image_straight
        if self.image == self.image_inverse:
            self.image = self.image_inverse_m
        elif  self.image == self.image_inverse_m:
            self.image = self.image_inverse