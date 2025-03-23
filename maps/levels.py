import pygame
import os

class Levels:
    def __init__(self, script_dir):
        """Initialize the levels with their positions and attributes."""
        self.script_dir = script_dir
        self.levels = []
        self.load_levels()

    def load_levels(self):
        """Load level sprites and define their positions on the map."""
        # Load level images
        spawn_img = pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels", "spawn_point.png"))
        level_1_img = pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels", "stage_1.png"))
        level_2_img = pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels", "stage_2.png"))
        level_3_img = pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels", "stage_3.png"))

        # Scale level images
        LEVEL_SCALE = 0.15
        self.spawn_img = pygame.transform.scale(spawn_img,(int(spawn_img.get_width() * LEVEL_SCALE), int(spawn_img.get_height() * LEVEL_SCALE)))
        self.level_1_img = pygame.transform.scale(level_1_img, (int(level_1_img.get_width() * LEVEL_SCALE), int(level_1_img.get_height() * LEVEL_SCALE)))
        self.level_2_img = pygame.transform.scale(level_2_img, (int(level_2_img.get_width() * LEVEL_SCALE), int(level_2_img.get_height() * LEVEL_SCALE)))
        self.level_3_img = pygame.transform.scale(level_3_img, (int(level_3_img.get_width() * LEVEL_SCALE), int(level_3_img.get_height() * LEVEL_SCALE)))

        self.levels = [
            {"id": 0, "img": self.spawn_img, "map_x": 1930, "map_y": 1830, "width": self.spawn_img.get_width(),"height": self.spawn_img.get_height(), "interaction_radius": 0},
            {"id": 1,"img": self.level_1_img,"map_x": 3000,"map_y": 1830,"width": self.level_1_img.get_width(),"height": self.level_1_img.get_height(),"interaction_radius": 75},
            {"id": 2,"img": self.level_2_img,"map_x": 4190,"map_y": 1450,"width": self.level_2_img.get_width(),"height": self.level_2_img.get_height(),"interaction_radius": 75},
            {"id": 3,"img": self.level_3_img,"map_x": 3375,"map_y": 550,"width": self.level_3_img.get_width(),"height": self.level_3_img.get_height(),"interaction_radius": 75}
        ]

    def get_level_by_id(self, level_id):
        """Get a level by its ID."""
        return next((l for l in self.levels if l["id"] == level_id), None)

    def get_all_levels(self):
        """Return all levels."""
        return self.levels

    def draw_levels(self, screen, map_x, map_y):
        """Draw all levels on the map at their correct positions."""
        for level in self.levels:
            level_screen_x = map_x + level["map_x"]
            level_screen_y = map_y + level["map_y"]
            screen.blit(level["img"], (level_screen_x, level_screen_y))

    def check_proximity(self, char_map_x, char_map_y):
        """Check if character is near any level and return the level ID if so."""
        for level in self.levels:
            # Calculate center of level
            level_center_x = level["map_x"] + level["width"] // 2
            level_center_y = level["map_y"] + level["height"] // 2

            # Calculate distance to level
            distance = ((char_map_x - level_center_x) ** 2 +
                        (char_map_y - level_center_y) ** 2) ** 0.5

            # If within interaction radius
            if distance <= level["interaction_radius"]:
                return level["id"]
        return None