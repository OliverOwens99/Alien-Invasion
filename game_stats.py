class GameStats:
    """Track statistics for the alien invasion game"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state
        self.game_active = False
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialise statistics that can change during the game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

