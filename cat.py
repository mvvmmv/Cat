import pygame
from pygame.sprite import Sprite
from pygame.mixer import Sound
import time
from datetime import datetime


class Cat(Sprite):
    """Create a cat"""

    def __init__(self, cl_game, groups, obstacles):
        """Initialize the cat and define the start location"""
        super().__init__(groups)
        self.screen = cl_game.screen
        self.screen_rect = cl_game.screen.get_rect()

        self.settings = cl_game.settings

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
        
        self.obstacles = obstacles
        
        self.fish_eaten = 0
        self.start_time = time.time()

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
                self.do(dt)
        
  
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

    def do(self,dt):
        time_do_triggered = time.time()
        # print(time_do_triggered - self.start_time)
        time_passed = time_do_triggered > self.start_time + 5
        for obstacle in self.obstacles:
            if obstacle.name == 'plate':
                if (obstacle.rect.right + 5 >= self.rect.left \
                        and obstacle.rect.right < self.rect.right \
                        and self.image == self.image_straight \
                        and self.rect.centery in range(obstacle.rect.centery - self.settings.free_y,obstacle.rect.centery + self.settings.free_y) \
                        and time_passed and obstacle.image == obstacle.image_fish) \
                        or (obstacle.rect.left - 5 <= self.rect.right \
                        and obstacle.rect.left > self.rect.left \
                        and self.image == self.image_inverse \
                        and self.rect.centery in range(obstacle.rect.centery - self.settings.free_y,obstacle.rect.centery + self.settings.free_y) \
                        and time_passed and obstacle.image == obstacle.image_fish):
                    obstacle.empty()
                    self.fish_eaten += 1
                    self.start_time = time_do_triggered
                    #print(self.fish_eaten)
                    #print(self.fish_eaten, self.first_time*dt* 1000 + 5000000000, time1, self.first_time*dt* 1000 + 5000000000 - time1)
    
    def meow(self):
        """Makes meow sounds"""

        if time.time() - self.cat_current_time >= self.settings.meow_delay:
            self.meow_sound.play()
            self.cat_current_time = time.time()