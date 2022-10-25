from secrets import choice
import pygame
from pygame.sprite import Sprite
from pygame.mixer import Sound
import time
from datetime import datetime
from random import randint


class Cat(Sprite):
    """Create a cat"""

    def __init__(self, cl_game, mute_btn, bed, groups, obstacles):
        """Initialize the cat and define the start location"""
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()

        self.settings = cl_game.settings
        self.mute_button = mute_btn
        self.obstacles = obstacles
        self.bed = bed
        
        # Uploads cat looking left image and gets rectangle.
        self.image_straight = pygame.image.load(self.settings.cat_images[0])
        self.image_straight_m = pygame.image.load(self.settings.cat_images[1])
        self.rect = self.image_straight.get_rect()
        self.image = self.image_straight
        # Uploads cat looking right image and gets rectangle.
        self.image_inverse = pygame.image.load(self.settings.cat_images[2])
        self.image_inverse_m = pygame.image.load(self.settings.cat_images[3])
        # Uploads sleeping cat image
        self.image_sleep = pygame.image.load(self.settings.cat_images[4])
        # The cat appears at the center of the screen.
        self.rect.center = self.screen_rect.center
        self.old_rect = self.rect.copy()
        # Movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        # Timers
        self.key_pressed_time = time.perf_counter()
        self.change_direction_timer = time.perf_counter()
        # Flags
        self.roaming_flag = False
        self.sleep = False
        self.mute_flag = True
        # Initialization for random roaming position
        self.c_d_x, self.c_d_y = [0, 0]
        # Sounds
        self.meow_sound = pygame.mixer.Sound('sounds/meow.wav')     
        # Cat feeding counter
        self.fish_eaten = 0       

    def check_input(self):
        """Handles keyboard events"""
        
        # Checks keys pressed only if cat isn't sleeping
        if self.sleep == True:
            return
        else:
            # Checks keys pressed and starts the timer after each pressed key
            keys = pygame.key.get_pressed()
                   
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.key_pressed_time = time.perf_counter()
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.key_pressed_time = time.perf_counter()
            else:
                self.direction.y = 0
    
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.key_pressed_time = time.perf_counter()
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.key_pressed_time = time.perf_counter()
            else:
                self.direction.x = 0
    
            #if self.sleep == False:
            # If last key pressed more than <afk_delay> seconds ago - cat starts roaming.
            if (abs(self.key_pressed_time - time.perf_counter()) >= self.settings.afk_delay):        
                if self.roaming_flag == False:
                    self.change_direction_timer = time.perf_counter()
                self.roaming_flag = True

            if (abs(self.key_pressed_time - time.perf_counter()) < self.settings.afk_delay):
                self.roaming_flag = False
  
    def update(self):
        """Update location of the cat"""
        
        self.old_rect = self.rect.copy()
        self.check_input()

        if self.roaming_flag == True:
            # if random romaing enabled change direction every 5 seconds    
            if time.perf_counter() - self.change_direction_timer > self.settings.keep_random_direction_time:
                self.c_d_y, self.c_d_x, = choice([[0,1], [1,0], [-1, 0], [0, -1]])
                self.change_direction_timer = time.perf_counter()
            self.direction.x, self.direction.y = self.c_d_x, self.c_d_y
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.settings.cat_speed
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.settings.cat_speed
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

        # Change image accordingly to cat's direction
        if self.direction.x == 1:
            self.image = self.image_inverse
        if self.direction.x == -1:
            self.image = self.image_straight
        if self.direction.y == 1:
            self.image = self.image_straight
        if self.direction.y == -1:
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
                        if self.roaming_flag == True:
                            self.direction.x = self.direction.x * -1
                            
                    # collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        if self.roaming_flag == True:
                            self.direction.x = self.direction.x * -1
            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        if self.roaming_flag == True:
                            self.direction.y = self.direction.y * -1
                            
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        if self.roaming_flag == True:
                            self.direction.y = self.direction.y * -1                    

    def do(self, direction=None):
        """Cat actions: eats the fish, sleeps, kicks the ball
        """
        for obstacle in self.obstacles:
            if obstacle.name == 'plate':
                # Checks if cat looks to the plate and is located near the plate.
                # Checking if the cat vertical center is in [between obstacle's vertical center 
                # - self.settings.free_y, between obstacle's vertical center + self.settings.free_y]
                center_y_check = self.rect.centery in range(obstacle.rect.centery - self.settings.free_y, \
                                                            obstacle.rect.centery + self.settings.free_y)
                if center_y_check:
                    if (obstacle.rect.right in range(self.rect.left - 5, self.rect.right) \
                            # checking if cat look left
                            and self.image == self.image_straight) \
                            or \
                            (obstacle.rect.left in range(self.rect.left+1, self.rect.right + 5 + 1) \
                            # checking if cat look right
                            and self.image == self.image_inverse):
                        obstacle.empty()
                        self.fish_eaten += 1
                        
            if obstacle.name == 'ball': 
                # Checks if cat is located near the ball.
                # Checking if the cat vertical center is in [between obstacle's top
                # and obstacle's bottom]
                center_y_check = obstacle.rect.centery in range(self.rect.top, \
                                                            self.rect.bottom)
                if center_y_check:
                    if obstacle.rect.right in range(self.rect.left - 5, self.rect.right) \
                            or  obstacle.rect.left in range(self.rect.left+1,self.rect.right + 5 + 1):
                            obstacle.kick(direction=direction)
        
        self.cat_sleep()                        
            
    def meow(self):
        """Makes meow sounds"""
        
        if self.mute_flag == False and self.sleep == False:
            self.meow_sound.play()
    
    def cat_sleep(self):

        center_ybed_check = self.rect.centery in range(self.bed.rect.centery - self.settings.free_y, \
                                self.bed.rect.centery + self.settings.free_y)
        center_xbed_check = self.rect.centerx in range(self.bed.rect.centerx - self.settings.free_y, \
                                self.bed.rect.centerx + self.settings.free_y)
        if center_xbed_check and center_ybed_check:
            if self.sleep == True:
                self.sleep = False
                self.image = self.image_straight
                self.key_pressed_time = 0
            else:
                self.sleep = True
                self.image = self.image_sleep
            
    def animation(self):
        if self.image == self.image_straight:
            self.image = self.image_straight_m
        elif self.image == self.image_straight_m :
            self.image = self.image_straight
        if self.image == self.image_inverse:
            self.image = self.image_inverse_m
        elif  self.image == self.image_inverse_m:
            self.image = self.image_inverse