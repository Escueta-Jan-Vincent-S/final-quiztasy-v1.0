import pygame
import os
from .battle import Battle
from importlib import import_module

class Levels:
    def __init__(self, script_dir):
        """Initialize the levels with their positions and attributes."""
        self.script_dir = script_dir
        self.levels = []
        self.load_levels()
        self.active_level = None
        self.screen = None
        self.hero_type = None

    def load_levels(self):
        """Load level sprites and define their positions on the map."""
        LEVEL_SCALE = 0.15
        level_names = ["spawn_point"] + [f"stage_{i}" for i in range(1, 21)]  # Includes spawn and 20 levels

        # Load and scale images dynamically
        self.level_images = {
            name: pygame.transform.scale(
                pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels", f"{name}.png")),
                (int(pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels",
                                                    f"{name}.png")).get_width() * LEVEL_SCALE),
                 int(pygame.image.load(os.path.join(self.script_dir, "assets", "images", "levels",
                                                    f"{name}.png")).get_height() * LEVEL_SCALE))
            )
            for name in level_names
        }

        # Define level positions and interaction radii
        level_data = [
            (0, "spawn_point", 1930, 1830, 0),
            (1, "stage_1", 3000, 1830, 75),
            (2, "stage_2", 4190, 1450, 75),
            (3, "stage_3", 3375, 550, 75),
            (4, "stage_4", 4715, 2575, 75),
            (5, "stage_5", 5400, 1775, 75),
            (6, "stage_6", 6350, 1225, 75),
            (7, "stage_7", 6350, 2700, 75),
            (8, "stage_8", 6300, 4500, 75),
            (9, "stage_9", 6300, 6400, 75),
            (10, "stage_10", 7880, 6150, 75),
            (11, "stage_11", 9700, 4700, 75),
            (12, "stage_12", 9600, 3050, 75),
            (13, "stage_13", 7550, 4700, 75),
            (14, "stage_14", 6830, 3550, 75),
            (15, "stage_15", 7160, 1735, 75),
            (16, "stage_16", 7975, 1835, 75),
            (17, "stage_17", 8465, 1000, 75),
            (18, "stage_18", 9050, 1835, 75),
            (19, "stage_19", 9825, 1600, 75),
            (20, "stage_20", 9700, 600, 75),
        ]

        self.levels = [
            {"id": lvl_id,"img": self.level_images[name],"map_x": x,"map_y": y,"width": self.level_images[name].get_width(),"height": self.level_images[name].get_height(),"interaction_radius": radius}
            for lvl_id, name, x, y, radius in level_data
        ]

    def set_context(self, screen, hero_type):
        """Set the screen and hero type needed for the enter_level method."""
        self.screen = screen
        self.hero_type = hero_type

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

    def set_active_level(self, level_id):
        """Set the active level."""
        self.active_level = level_id

    def enter_level(self):
        """Enter the currently active level."""
        if self.active_level is not None and self.screen is not None:
            print(f"Level {self.active_level} is clicked")
            try:
                module = import_module(f"gameplay.level_{self.active_level}")
                # Get the level class (assuming naming convention Level1, Level2, etc.)
                level_class = getattr(module, f"Level{self.active_level}")
                level = level_class(self.script_dir)
            except (ImportError, AttributeError):
                # Fallback to level 1 if there's any error
                from gameplay.level_1 import Level1
                level = Level1(self.script_dir)
            # Start the battle with the player's hero type

            battle = Battle(self.screen, self.script_dir, level, self.hero_type)
            victory = battle.run()

            # Handle battle result
            if victory:
                print(f"Victory! Level {self.active_level} completed.")
                # Here you could unlock the next level or provide rewards
            else:
                print(f"Defeat! Try level {self.active_level} again.")