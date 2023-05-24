import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen  # making bullets appear ons screen but not draws it there
        self.setting = ai_game.settings
        self.color = self.setting.bullet_color
        # Create a bullet rectangle at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a  decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move bullets up the screen"""
        # Updates the decimal position of the bullet.
        self.y -= self.setting.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

