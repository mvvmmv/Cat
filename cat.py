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
        self.rect = self.image_straight.get_rect()
        self.image = self.image_straight
        # Uploads cat looking right image and gets rectangle.
        self.image_inverse = pygame.image.load(self.settings.cat_images[2])
        # self.rect = self.image_inverse.get_rect()

        # The cat appears at the center of the screen.
        self.rect.center = self.screen_rect.center
        self.old_rect = self.rect.copy()

        # Movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        
        # Sounds
        self.meow_sound = pygame.mixer.Sound('sounds/meow.wav')
        self.cat_current_time = time.time()   
        self.start_time = time.time()
        self.start_sound_time = time.time() - 20     
        
        # Cat actions counter
        self.fish_eaten = 0       
        self.mute_flag = True # game starts with no sound

    def check_input(self, dt):
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
            
        if keys[pygame.K_SPACE]:
            self.do()
        
        if keys[pygame.K_m]:
            self.sound()
        
  
    def update(self, dt):
        """Update location of the cat"""
        
        self.old_rect = self.rect.copy()
        self.check_input(dt)

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.settings.cat_speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.settings.cat_speed * dt
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
        """Cat actions"""
        
        time_do_triggered = time.time()
        # Checking if more than 5 seconds passed from previous run of this function (this function runs after SPACE's been pressed)
        # SPACE_is_pressed event will be True several times while it's actually been keeping pressed,
        # but we want to run this function only once after SPACE's been pressed.
        # That's why I check if it's passed 5 secs or not.        
        # (Considering that we won't press the key too long. By design I want it to be pressed shortly.)
        time_passed = time_do_triggered > self.start_time + 5
        for obstacle in self.obstacles:
            if obstacle.name == 'plate':
                # Checking if the cat vertical center is in [between obstacle's vertical center - self.settings.free_y, between obstacle's vertical center + self.settings.free_y]
                center_y_check = self.rect.centery in range(obstacle.rect.centery - self.settings.free_y,obstacle.rect.centery + self.settings.free_y)
                if time_passed:
                    if (obstacle.rect.right + 5 >= self.rect.left and obstacle.rect.right < self.rect.right and  center_y_check\
                            # checking if cat look left
                            and self.image == self.image_straight \
                            and obstacle.image == obstacle.image_fish) \
                            or \
                            (obstacle.rect.left - 5 <= self.rect.right and obstacle.rect.left > self.rect.left and center_y_check \
                            # checking if cat look right
                            and self.image == self.image_inverse \
                            and obstacle.image == obstacle.image_fish):
                        obstacle.empty()
                        self.fish_eaten += 1
                        self.start_time = time_do_triggered
               
    def meow(self):
        """Makes meow sounds"""
        time_meow_triggered = time.time()
        if time.time() - self.cat_current_time >= self.settings.meow_delay and self.mute_flag == False:
            self.meow_sound.play()
            self.cat_current_time = time_meow_triggered
    
    def sound(self):
        """Changes the mute flag if M key has been pressed"""
        
        time_sound_triggered = time.time()
        # Same as for the "do" function.
        # I check if this fuction was called not later than 5 seconds ago.
        time_passed = time_sound_triggered > self.start_sound_time + 5
        if time_passed:
            # If sound is playing - turn it off
            if self.mute_flag == False:
                self.mute_button.image = self.mute_button.images[0]
                self.mute_flag = True
                self.meow_sound.stop()
                self.start_sound_time = time_sound_triggered
            # if sound isn't playing - turn it on
            elif self.mute_flag == True:
                self.mute_button.image = self.mute_button.images[1]
                self.mute_flag = False
                self.meow()
                self.start_sound_time = time_sound_triggered