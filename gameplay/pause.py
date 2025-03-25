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

        # Create pause button
        self.button = Button(
            x=100,
            y=100,
            idle_img=self.pause_idle,
            hover_img=self.pause_hover,
            action=self.toggle_pause,
            scale=0.15,
            audio_manager=self.audio_manager
        )

    def load_scaled_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        if self.scale != 1.0:
            new_width = int(image.get_width() * self.scale)
            new_height = int(image.get_height() * self.scale)
            return pygame.transform.scale(image, (new_width, new_height))
        return image

    def toggle_pause(self):
        """Toggle pause state and play click sound"""
        self.paused = not self.paused
        if self.audio_manager:
            self.audio_manager.play_sfx()

            if self.paused:
                self.pause_start_time = time.time()  # Record when pause started
                pygame.mixer.music.pause()
            else:
                # Calculate how long we were paused
                self.total_paused_time += time.time() - self.pause_start_time
                pygame.mixer.music.unpause()

    def get_total_paused_time(self):
        """Returns the total time spent paused and resets the counter"""
        paused_time = self.total_paused_time
        self.total_paused_time = 0  # Reset after getting
        return paused_time

    def draw_pause_overlay(self):
        """Draw the pause overlay when game is paused"""
        if self.paused:
            # Create semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))

            # Draw "PAUSED" text
            paused_text = self.font.render("PAUSED", True, (255, 255, 255))
            paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(paused_text, paused_rect)

    def draw(self):
        """Draw the pause button (always visible)"""
        self.button.draw(self.screen)
        self.draw_pause_overlay()

    def update(self, event):
        """Handle pause button events"""
        self.button.update(event)

    def is_paused(self):
        """Check if game is paused"""
        return self.paused