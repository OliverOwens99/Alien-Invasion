import json
import os
import sys
from time import sleep

import pygame
from pygame import mixer

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class that manages the game assets and behaviour"""
    clock = pygame.time.Clock()

    def __init__(self):

        """initializes the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Create instance of game stats
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        mixer.music.load("star_trek.mp3")
        mixer.music.get_volume()
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
        # Initialise joystick
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()

        with open(os.path.join("ps4_keys.json"), 'r+') as file:

            self.button_keys = json.load(file)
        # # 0: Left analog horizontal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

    def run_game(self):
        """Start the main loop for the game """
        while True:
            # Watch for keyboard/mouse  events
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(500)
            self._update_screen()

    def _check_events(self):
        # Responds to key event and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  # passing event into keydown method
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  # passing event into keyup method
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.JOYBUTTONDOWN:
                self._fire_bullet()

            elif event.type == pygame.JOYAXISMOTION:
                self.analog_keys[event.axis] = event.value
                #             # print(analog_keys)
                #             # Horizontal Analog
                if abs(self.analog_keys[0]) > .4:
                    if self.analog_keys[0] < -.7:
                        self.ship.moving_left = True
                    else:
                        self.ship.moving_left = False
                    if self.analog_keys[0] > .7:

                        self.ship.moving_right = True
                    else:
                        self.ship.moving_right = False

    def _check_play_button(self, mouse_pos):
        """ Starts a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)
            # Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to key presses down"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):

        """Respond to key presses when button released"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet object and add it to bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets"""
        # Update bullet positions and get rid of old bullets
        self.bullets.update()
        # Get rid of bullets that have gone off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien  collisions"""
        # Check if any bullets have hit the aliens.
        # if so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            # Increase speed of game
            self.settings.increase_speed()
            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        # Make the fleet of aliens
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create a full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in a row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        # Redraw the screen during each pass of the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        # self.clock.tick(500)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet and check if its at an edge"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet  and change the direction of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responds to the ship being hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
