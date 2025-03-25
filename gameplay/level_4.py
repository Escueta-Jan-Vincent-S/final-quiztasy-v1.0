import pygame
from characters.enemy import MiniBoss

class Level4:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.level_id = 4
        self.name = "Level 4"
        self.description = "Basta Level 4"
        # Level-specific settings
        self.enemy_hp = 8
        self.enemy_damage = 2.5
        self.question_difficulty = 1
        self.timer_seconds = 10

        # Load background for this level
        self.background = pygame.image.load(f"{script_dir}/assets/images/battle/backgrounds/level1_bg.png")
        self.background = pygame.transform.scale(self.background, (1920, 1080))

    def create_enemy(self):
        """Creates the enemy for this level"""
        return MiniBoss(
            self.script_dir,
            level=self.level_id,
            hp=self.enemy_hp,
            damage=self.enemy_damage
        )

    def get_timer_seconds(self):
        """Returns the number of seconds for the timer"""
        return self.timer_seconds

    def get_difficulty(self):
        """Returns the difficulty level for questions"""
        return self.question_difficulty

    def draw_background(self, screen):
        """Draws the level background"""
        screen.blit(self.background, (0, 0))