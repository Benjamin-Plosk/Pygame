import pygame
import random
import math

import constants
from spritesheetfun import SpriteSheet


class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    # def __init__(self, color, width, height):
    def __init__(self):

        super().__init__()

        self.vel_x = 5
        self.vel_y = 5

        self.life = 100
        # self.life_bar = pygame.Surface([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]).convert()

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []

        self.level = None
        self.walls = None

        sprite_sheet = SpriteSheet("main_player.png")
        # Load all the right facing images into a list
        i = 0
        start_x, start_y = 24*9, 32*5
        size_x, size_y = 24, 32
        while i < 3:
            image = sprite_sheet.get_image(start_x, start_y, 24, 32)
            self.walking_frames_r.append(image)
            start_x += size_x
            i += 1

        i = 0
        start_x = 24*9
        start_y = 32*5 - size_y
        while i < 3:
            image = sprite_sheet.get_image(start_x, start_y, 24, 32)
            self.walking_frames_u.append(image)
            start_x += size_x
            i += 1

        i = 0
        start_x = 24*9
        start_y = 32*5 + size_y
        while i < 3:
            image = sprite_sheet.get_image(start_x, start_y, 24, 32)
            self.walking_frames_d.append(image)
            start_x += size_x
            i += 1

        i = 0
        start_x = 24*9
        start_y = 32*5 + 2*size_y
        while i < 3:
            image = sprite_sheet.get_image(start_x, start_y, 24, 32)
            self.walking_frames_l.append(image)
            start_x += size_x
            i += 1

        # Set the image the player starts with
        self.image = self.walking_frames_r[1]
        # # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def update(self, pressed_right, pressed_left, pressed_up, pressed_down):
        if pressed_right:
            self.rect.x += self.vel_x
            self.image = self.walking_frames_r[1]
            if self.rect.right > constants.SCREEN_WIDTH:
                self.rect.right = constants.SCREEN_WIDTH
            frame = (self.rect.x // 50) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        elif pressed_left:
            self.rect.x += -self.vel_x
            self.image = self.walking_frames_l[1]
            if self.rect.left < 0:
                self.rect.left = 0
            frame = (self.rect.x // 50) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        elif pressed_up:
            self.rect.y += -self.vel_y
            self.image = self.walking_frames_u[1]
            if self.rect.top < 0:
                self.rect.top = 0
            frame = (self.rect.y // 50) % len(self.walking_frames_u)
            self.image = self.walking_frames_u[frame]
        elif pressed_down:
            self.rect.y += self.vel_y
            self.image = self.walking_frames_d[1]
            if self.rect.bottom > constants.SCREEN_HEIGHT:
                self.rect.bottom = constants.SCREEN_HEIGHT
            frame = (self.rect.y // 50) % len(self.walking_frames_d)
            self.image = self.walking_frames_d[frame]

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if pressed_right:
                self.rect.right = block.rect.left
            elif pressed_left:
                self.rect.left = block.rect.right
            elif pressed_up:
                self.rect.top = block.rect.bottom
            elif pressed_down:
                self.rect.bottom = block.rect.top

        # self.life_image = pygame.draw.rect(screen, constants.GREEN, (10, 10, 60, 10))


class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class World(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        self.large_image = pygame.image.load('Snipaste_2020-09-07_23-19-25.png').convert()
        self.image = pygame.Surface([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]).convert()
        self.rect = None

    def world_shift(self, x, y):
        self.image.blit(self.large_image, (0, 0), (x, y, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()


class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.move_x = 1
        self.move_y = 1

        self.image = pygame.Surface([30, 30])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # self.move_x = None
        # self.move_y = None
        # self.direction = random.randint(0, 1)
        # self.image = pygame.Surface([50, 50])
        # self.rect = self.image.get_rect()
        #
        # self.aux = 0

    def move_enemy(self, player_x, player_y):

        distance_x = player_x - self.rect.x
        distance_y = player_y - self.rect.y
        # hip = math.sqrt((distance_y ^ 2) + (distance_x ^ 2))
        # cos = distance_x / hip
        # sen = distance_y / hip

        if distance_x > 0:
            self.move_x = 2
        elif distance_x < 0:
            self.move_x = -2
        if distance_y > 0:
            self.move_y = 2
        elif distance_y < 0:
            self.move_y = -2

        self.rect.x += self.move_x
        self.rect.y += self.move_y
    #
    # def move_enemy(self):
    #
    #     if 0 < self.aux < 5:
    #         self.move_x = random.randint(0, 10)
    #         self.rect.x += self.move_x
    #         self.aux -= 1
    #     elif -5 < self.aux < 0:
    #         self.move_y = random.randint(0, 10)
    #         self.rect.y += self.move_y
    #         self.aux += 1
    #     else:
    #         self.aux = random.randint(-5, 5)
