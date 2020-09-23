import pygame
import constants


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
        self.height = None
        self.width = None
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        self.height = 2*height
        self.width = 2*width
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (self.width, self.height))
        # Assuming black works as the transparent color
        image.set_colorkey(constants.GREEN_KEY)

        # Return the image
        return image

    def get_wall_image(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
        pass
