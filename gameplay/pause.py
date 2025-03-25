import pygame
import os
import time
from ui.button import Button
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH


class Pause:
    def __init__(self, screen, script_dir, audio_manager=None, scale=1):
        self.screen = screen
        self.script_dir = script_dir
        self.audio_manager = audio_manager
        self.paused = False
        self.scale = scale
        self.pause_start_time = 0
        self.total_paused_time = 0

        # Load fonts
        self.font = pygame.font.Font(FONT_PATH, 50)

        # Load pause button images
        pause_idle_path = os.path.join(script_dir, "assets", "images", "battle", "pause", "pause", "pause_icon_img.png")
        pause_hover_path = os.path.join(script_dir, "assets", "images", "battle", "pause", "pause", "pause_icon_hover.png")
        self.pause_idle = self.load_scaled_image(pause_idle_path)
        self.pause_hover = self.load_scaled_image(pause_hover_path)

        # Load pause border image
        border_path = os.path.join(script_dir, "assets", "images", "battle", "pause", "pause_border.png")
        self.border_img = self.load_scaled_image(border_path, 0.5)

        # Create pause button
        self.pause_button = Button(
            x=100,
            y=100,
            idle_img=self.pause_idle,
            hover_img=self.pause_hover,
            action=self.toggle_pause,
            scale=0.15,
            audio_manager=self.audio_manager
        )

        # Initialize pause menu icons only
        self.pause_icons = []
        self.init_pause_icons()

    def init_pause_icons(self):
        """Initialize the pause menu icons"""
        icons = [
            {
                "name": "menu",
                "pos": (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 25),
                "action": self.return_to_menu
            },
            {
                "name": "map",
                "pos": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                "action": self.open_map
            },
            {
                "name": "resume",
                "pos": (SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 + 25),
                "action": self.toggle_pause
            },
        ]

        for icon in icons:
            # Load icon images
            idle_img = self.load_scaled_image(
                os.path.join(self.script_dir, "assets", "images", "battle", "pause", icon["name"], f"{icon['name']}_icon_img.png"),
                0.25
            )
            hover_img = self.load_scaled_image(
                os.path.join(self.script_dir, "assets", "images", "battle", "pause", icon["name"], f"{icon['name']}_icon_hover.png"),
                0.25
            )

            # Create icon
            button = Button(
                x=icon["pos"][0],
                y=icon["pos"][1],
                idle_img=idle_img,
                hover_img=hover_img,
                action=icon["action"],
                scale=1,
                audio_manager=self.audio_manager
            )

            self.pause_icons.append(button)

    def load_scaled_image(self, path, scale=None):
        """Load an image and scale it. If scale is None, use self.scale"""
        image = pygame.image.load(path).convert_alpha()
        scale_factor = scale if scale is not None else self.scale
        if scale_factor != 1.0:
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            return pygame.transform.scale(image, (new_width, new_height))
        return image

    def toggle_pause(self):
        """Toggle pause state and play click sound"""
        self.paused = not self.paused
        if self.audio_manager:
            self.audio_manager.play_sfx()

            if self.paused:
                self.pause_start_time = time.time()
                pygame.mixer.music.pause()
            else:
                self.total_paused_time += time.time() - self.pause_start_time
                pygame.mixer.music.unpause()

    def return_to_menu(self):
        """Return to main menu function"""
        print(f"Returning to menu...")  # Replace with actual menu return logic
        if self.audio_manager:
            self.audio_manager.play_sfx()

    def open_map(self):
        """Open map function"""
        print(f"Opening map...")  # Replace with actual map opening logic
        if self.audio_manager:
            self.audio_manager.play_sfx()

    def get_total_paused_time(self):
        """Returns the total time spent paused and resets the counter"""
        paused_time = self.total_paused_time
        self.total_paused_time = 0
        return paused_time

    def draw_pause_overlay(self):
        """Draw the pause overlay when game is paused"""
        if self.paused:
            # Create semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))

            # Draw border image centered on screen
            border_rect = self.border_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(self.border_img, border_rect)

            # Draw pause icons
            for icon in self.pause_icons:
                icon.draw(self.screen)

    def draw(self):
        """Draw the pause button (always visible) and overlay when paused"""
        if not self.paused:
            self.pause_button.draw(self.screen)
        self.draw_pause_overlay()

    def update(self, event):
        """Handle pause button events"""
        if not self.paused:
            self.pause_button.update(event)
        else:
            # Handle events for pause menu icons
            for icon in self.pause_icons:
                icon.update(event)

    def is_paused(self):
        """Check if game is paused"""
        return self.paused