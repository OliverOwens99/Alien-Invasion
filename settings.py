class Settings:
    """A class to handle the games settings"""

    def __init__(self):
        """initialises the games static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (230, 230, 230)  # (230, 230 ,230)

        # Ship Settings

        self.ship_limit = 3

        # Bullet setting

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)  # (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings

        self.fleet_drop_speed = 10
        # How quickly  the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2
        self.alien_speed = 1

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
