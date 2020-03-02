# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
from CONSTANTS import *
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()


    # # Move the sprite based on user keypresses
    # def update(self, pressed_keys):
    #     if pressed_keys[K_UP]:
    #         self.rect.move_ip(0, -5)
    #     if pressed_keys[K_DOWN]:
    #         self.rect.move_ip(0, 5)
    #     if pressed_keys[K_LEFT]:
    #         self.rect.move_ip(-5, 0)
    #     if pressed_keys[K_RIGHT]:
    #         self.rect.move_ip(5, 0)
    #
    #     # Keep player on the screen
    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #     if self.rect.right > SCREEN_WIDTH:
    #         self.rect.right = SCREEN_WIDTH
    #     if self.rect.top <= 0:
    #         self.rect.top = 0
    #     if self.rect.bottom >= SCREEN_HEIGHT:
    #         self.rect.bottom = SCREEN_HEIGHT