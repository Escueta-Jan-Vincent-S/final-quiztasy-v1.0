import pygame
import os
from ui.button import Button
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Pause:
    def __init__(self, screen, script_dir, audio_manager=None, scale=1):
        self.screen = screen
        self.script_dir = script_dir
        self.audio_manager = audio_manager
        self.paused = False
        self.scale = scale

        pause_idle_path = os.path.join(script_dir, "assets", "images", "battle", "pause", "pause", "pause_icon_img.png")
        pause_hover_path = os.path.join(script_dir, "assets", "images", "battle", "pause", "pause", "pause_icon_hover.png")

        self.pause_idle = self.load_scaled_image(pause_idle_path)
        self.pause_hover = self.load_scaled_image(pause_hover_path)

        self.button = Button(
            x=100,
            y=100,
            idle_img=self.pause_idle,
            hover_img=self.pause_hover,
            action=self.toggle_pause,
            scale=0.25,
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
            self.audio_manager.play_sfx("click")

            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
    def draw(self):
        self.button.draw(self.screen)

    def update(self, event):
        self.button.update(event)