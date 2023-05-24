import pygame
from pygame.sprite import Sprite
""" A class to manage the ship"""


class Ship(Sprite):
    """ A class to manage the ship"""

    def __init__(self, ai_game):
        """initialise ship and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load ship image and get its rect
        self.image = pygame.image.load("star-trek-enterprise-icon-16.jpg")
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen (spawnpoint)
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ships horizontal position
        self.x = float(self.rect.x)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
