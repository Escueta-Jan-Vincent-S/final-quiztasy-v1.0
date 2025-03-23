import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui.back_button import BackButton
from .map_character_movement import MapCharacterMovement


class Map:
    def __init__(self, screen, script_dir, go_back_callback, audio_manager, hero_type=None):
        """Initialize the LSPU map with a Back button and navigation features."""
        self.script_dir = script_dir
        self.screen = screen
        self.running = True
        self.go_back_callback = go_back_callback  # Store the callback function
        self.audio_manager = audio_manager

        # Set the hero type (boy or girl)
        self.hero_type = hero_type if hero_type else "boy"  # Default to boy if not specified

        # Play hero-specific OST if audio is enabled
        if self.audio_manager.audio_enabled:
            self.audio_manager.play_music()

        # Load and scale the map
        self.map_original = pygame.image.load(os.path.join(script_dir, "assets", "images", "map", "lspu_map.png"))
        SCALE_FACTOR = 3
        self.map_width = int(self.map_original.get_width() * SCALE_FACTOR)
        self.map_height = int(self.map_original.get_height() * SCALE_FACTOR)
        self.map = pygame.transform.scale(self.map_original, (self.map_width, self.map_height))

        # Initial map position - center the map
        self.map_x = (SCREEN_WIDTH - self.map_width) // 2
        self.map_y = (SCREEN_HEIGHT - self.map_height) // 2

        # Initialize the Back button
        self.back_button = BackButton(screen, script_dir, self.go_back, position=(100, 100), scale=0.25)

        # Initialize character movement handler
        self.character_movement = MapCharacterMovement(
            self.hero_type,
            self.script_dir,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

        # Initialize clock for the run method
        self.clock = pygame.time.Clock()

    def go_back(self):
        """Handle back button action."""
        if self.audio_manager:
            self.audio_manager.play_sfx()  # Play sound effect when clicking back
        if self.go_back_callback:
            self.go_back_callback()  # Call the callback to return to the main menu
        self.running = False  # Stop the map loop

    def move_character(self):
        """Handle character movement based on keyboard input."""
        # Get map boundaries for character movement
        map_bounds = {
            'min_x': SCREEN_WIDTH - self.map_width,  # Rightmost limit (negative value)
            'max_x': 0,  # Leftmost limit
            'min_y': SCREEN_HEIGHT - self.map_height,  # Bottom limit (negative value)
            'max_y': 0,  # Top limit
            'width': self.map_width,
            'height': self.map_height
        }

        # Call the character movement handler
        map_adjustment, character_pos = self.character_movement.handle_movement(
            map_bounds,
            (self.map_x, self.map_y),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # Update map position
        self.map_x = map_adjustment[0]
        self.map_y = map_adjustment[1]

    def draw(self):
        """Draw the map, levels, and player icon on the screen."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map, (self.map_x, self.map_y))

        # Get current character frame and position
        self.character_movement.draw(self.screen)

        # Draw back button
        self.back_button.draw()

    def handle_events(self):
        """Handle map interactions and level selection."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle back button
            self.back_button.update(event)

    def update_character_animation(self):
        """Update character animation frames"""
        self.character_movement.update_animation()

    def run(self):
        """Main map loop."""
        while self.running:
            # Handle events
            self.handle_events()

            # Handle character movement - this should be called every frame
            self.move_character()

            # Update animation
            self.update_character_animation()

            # Draw everything
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)