import pygame
import constants
from entities import Player
from entities import Wall
from entities import World


def main():
    """ Main Program """
    pygame.init()
    # # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    # # Set display screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    # # Create world
    world = World()
    sprite_group = pygame.sprite.Group()
    # # Create the player
    player = Player()
    # # Create Walls
    wall = Wall(500, 400, 100, 100)
    wall2 = Wall(100, 100, 50, 50)
    # # Group
    sprite_group.add(wall)
    sprite_group.add(wall2)
    player.walls = sprite_group
    # Loop until the user clicks the close button.
    done = False
    # # Get keys
    pressed_right = None
    pressed_left = None
    pressed_up = None
    pressed_down = None
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_RIGHT:
                    pressed_right = True
                elif event.key == pygame.K_LEFT:
                    pressed_left = True
                elif event.key == pygame.K_UP:
                    pressed_up = True
                elif event.key == pygame.K_DOWN:
                    pressed_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressed_right = False
                elif event.key == pygame.K_LEFT:
                    pressed_left = False
                elif event.key == pygame.K_UP:
                    pressed_up = False
                elif event.key == pygame.K_DOWN:
                    pressed_down = False

        player.update(pressed_right, pressed_left, pressed_up, pressed_down)
        # # Go ahead and update the screen with what we've drawn.
        world.world_shift(player.rect.x, player.rect.y)

        screen.fill(constants.WHITE)
        screen.blit(world.image, world.rect)
        sprite_group.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        # Limit to 60 frames per second
        clock.tick(60)
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()
