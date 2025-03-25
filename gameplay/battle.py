import pygame
import time
import os
from characters.player import Player
from gameplay.questions import QuestionGenerator
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_PATH

class Battle:
    def __init__(self, screen, script_dir, level, player_type="boy"):
        self.screen = screen
        self.script_dir = script_dir
        self.level = level
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.small_font = pygame.font.Font(FONT_PATH, 30)

        # Initialize player and enemy
        self.player = Player(script_dir, player_type)
        self.enemy = level.create_enemy()

        # Battle state
        self.current_question = None
        self.selected_answer = None
        self.answer_buttons = []
        self.timer_start = 0
        self.time_left = level.get_timer_seconds()
        self.battle_message = ""
        self.message_timer = 0

        # Save the current map OST for restoration later
        self.player_type = player_type
        self.map_ost = self.get_map_ost_path()

        # Initialize first question
        self.generate_new_question()

        # Load and play battle music
        self.battle_music = self.load_battle_music()
        if self.battle_music:
            pygame.mixer.music.load(self.battle_music)
            pygame.mixer.music.play(-1)  # Loop the battle music

    def get_map_ost_path(self):
        """Get the path to the map OST based on player type."""
        return os.path.join(self.script_dir, "assets", "audio", "ost", self.player_type,
                            f"{self.player_type}_map_ost.mp3")

    def load_battle_music(self):
        """Load the appropriate battle music based on the player type."""
        if self.player_type == "boy":
            return os.path.join(self.script_dir, "assets", "audio", "ost", "battle", "boy_battle_ost.mp3")
        elif self.player_type == "girl":
            return os.path.join(self.script_dir, "assets", "audio", "ost", "battle", "girl_battle_ost.mp3")
        return None

    def stop_battle_music(self):
        """Stop the battle music and restore map music."""
        pygame.mixer.music.stop()
        # Restore the map OST
        pygame.mixer.music.load(self.map_ost)
        pygame.mixer.music.play(-1)  # Loop the map music

    def generate_new_question(self):
        """Generates a new question for the battle"""
        self.current_question = QuestionGenerator.get_random_question(self.level.get_difficulty())
        self.timer_start = time.time()
        self.time_left = self.level.get_timer_seconds()
        self.selected_answer = None
        self.create_answer_buttons()

    def create_answer_buttons(self):
        """Creates the answer buttons based on the current question"""
        self.answer_buttons = []
        # Create a button for each choice
        button_width = 200
        button_height = 60
        button_margin = 20
        total_width = (button_width + button_margin) * len(self.current_question.choices)
        start_x = (SCREEN_WIDTH - total_width) // 2

        for i, choice in enumerate(self.current_question.choices):
            button_rect = pygame.Rect(
                start_x + i * (button_width + button_margin),
                SCREEN_HEIGHT - 150,
                button_width,
                button_height
            )
            self.answer_buttons.append({
                'rect': button_rect,
                'value': choice,
                'text': str(choice),
                'hovered': False
            })

    def handle_events(self):
        """Handle user input during battle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is hovering over any answer button
                mouse_pos = pygame.mouse.get_pos()
                for button in self.answer_buttons:
                    button['hovered'] = button['rect'].collidepoint(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if an answer button was clicked
                mouse_pos = pygame.mouse.get_pos()
                for button in self.answer_buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        self.selected_answer = button['value']
                        self.check_answer()

    def check_answer(self):
        """Checks if the selected answer is correct"""
        if self.selected_answer == self.current_question.answer:
            # Correct answer - enemy takes damage
            self.enemy.take_damage(1)
            self.battle_message = "Correct! Enemy takes damage!"

            if self.enemy.hp <= 0:
                self.battle_message = "Victory! You defeated the enemy!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Generate a new question
                self.generate_new_question()
        else:
            # Wrong answer - player takes damage
            self.player.take_damage(self.enemy.get_damage_amount())
            self.battle_message = f"Wrong! You take {self.enemy.get_damage_amount()} damage!"

            if self.player.hp <= 0:
                self.battle_message = "Defeat! You have been defeated!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Generate a new question
                self.generate_new_question()

        # Set message timer
        self.message_timer = time.time()

    def update_timer(self):
        """Updates the time left to answer the question"""
        self.time_left = max(0, self.level.get_timer_seconds() - (time.time() - self.timer_start))

        # If time runs out, treat as wrong answer
        if self.time_left <= 0 and self.running:
            self.battle_message = "Time's up! You take damage!"
            self.player.take_damage(self.enemy.get_damage_amount())

            if self.player.hp <= 0:
                self.battle_message = "Defeat! You have been defeated!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Generate a new question
                self.generate_new_question()

            # Set message timer
            self.message_timer = time.time()

    def draw(self):
        """Draws the battle screen"""
        # Draw background
        self.level.draw_background(self.screen)

        # Draw player and enemy
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # Draw timer at the top of the screen
        timer_text = self.font.render(f"Time: {int(self.time_left)}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (timer_rect.x - 10, timer_rect.y - 10,
                          timer_rect.width + 20, timer_rect.height + 20))
        self.screen.blit(timer_text, timer_rect)

        # Draw question box at the bottom
        question_box = pygame.Rect(50, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), question_box)
        pygame.draw.rect(self.screen, (255, 255, 255), question_box, 3)

        # Draw question text
        question_text = self.font.render(self.current_question.question_text, True, (255, 255, 255))
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250))
        self.screen.blit(question_text, question_rect)

        # Draw answer buttons
        for button in self.answer_buttons:
            # Button colors change based on hover state
            if button['hovered']:
                color = (100, 100, 255)
            else:
                color = (50, 50, 200)

            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, (255, 255, 255), button['rect'], 2)

            # Button text
            text = self.small_font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

        # Draw battle message if there is one
        if self.battle_message and time.time() - self.message_timer < 2:  # Show message for 2 seconds
            message_text = self.font.render(self.battle_message, True, (255, 255, 0))
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (message_rect.x - 10, message_rect.y - 10,
                              message_rect.width + 20, message_rect.height + 20))
            self.screen.blit(message_text, message_rect)

    def run(self):
        """Main battle loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Update timer
            self.update_timer()

            # Draw battle
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Stop battle music and restore map music when the battle ends
        self.stop_battle_music()

        # Return result (True for victory, False for defeat)
        return self.enemy.hp <= 0