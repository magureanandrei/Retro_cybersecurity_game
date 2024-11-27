import os

import pygame
from pathlib import Path

pygame.init()
pygame.mixer.init()

# Load background music (make sure the file is in the same folder as the game or provide the correct path)
pygame.mixer.music.load('../assets/retro_music.mp3')  # Replace 'retro_music.mp3' with your file

# Set volume (optional)
pygame.mixer.music.set_volume(0.2)  # Volume range: 0.0 to 1.0

# Start playing the music in a loop
pygame.mixer.music.play(-1)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)
DARK_RED = (139, 0, 0)
DARK_GRAY = (40, 40, 40)

# Recovery commands
RECOVERY_COMMAND = "FIREWALL -RESTORE"
HACK_RECOVERY_COMMAND = "/KILL ALL"
# HINT_MESSAGE = "Hint: Use a command to restore your firewall (check system logs...)"
HACK_HINT_MESSAGE = "Hint: Use system termination command to eliminate threats..."
BASE_HACK_TIME_LIMIT = 10
# Game configuration
INITIAL_PACKET_SPEED = 2
SPEED_INCREASE_FACTOR = 0.2
INITIAL_LIVES = 3
WRONG_COMMAND_PENALTY = 5
MAX_BAD_ANSWERS = 5
SHIP_SIZE = (60, 60)
# Word lists
MALICIOUS_WORDS = [
    "STOP", "BLOCK", "SAFE", "GUARD", "WALL",
    "LOCK", "SHIELD", "SECURE", "DEFEND", "PROTECT"
]

VIRUS_WORDS = [
    "CLEAN", "SCAN", "FIX", "HEAL", "CURE",
    "PATCH", "UPDATE", "REPAIR", "CHECK", "REMOVE"
]

FLOOD_WORDS = [
    "DRAIN", "FLOW", "CALM", "COOL", "FILTER",
    "REDUCE", "LIMIT", "SLOW", "PAUSE", "STEADY"
]

LEGITIMATE_WORDS = [
    "PASS", "ALLOW", "GOOD", "OKAY", "FINE",
    "VALID", "TRUE", "RIGHT", "SAFE", "CLEAN"
]

# Set up the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cyber Defense Word Game")

questions =[["Two-factor authentication (2FA) uses two methods to verify your "
                "identity, like a password plus a code sent to your phone. "
                "It adds extra protection if one method is compromised.",["a) Logging in with a password and a code sent to your phone",
        "b) Using just a strong password",
        "c) Using fingerprint recognition only",
        "d) Scanning a QR code to access your account"],"A"]]

# Load images
base_dir = os.path.join(os.getcwd(), "../assets")
image_pathg = os.path.join(base_dir, "enemy_green.png")
image_pathr = os.path.join(base_dir, "enemy_red.png")
image_pathb = os.path.join(base_dir, "enemy_blue.png")
image_pathy = os.path.join(base_dir, "enemy_yellow.png")

try:
    malicious_ship = pygame.transform.scale(pygame.image.load(image_pathg), SHIP_SIZE)
    virus_ship = pygame.transform.scale(pygame.image.load(image_pathr), SHIP_SIZE)
    flood_ship = pygame.transform.scale(pygame.image.load(image_pathy), SHIP_SIZE)
    legitimate_ship = pygame.transform.scale(pygame.image.load(image_pathb), SHIP_SIZE)
    use_images = True
except pygame.error:
    use_images = False
    print("Image files not found. Falling back to colored rectangles.")

# Font
font1 = pygame.font.Font(pygame.font.get_default_font(), 24)
font = pygame.font.Font('../assets/Evil Empire.otf', 24)
small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
large_font = pygame.font.Font(pygame.font.get_default_font(), 32)

global running, input_text, server_health,score, firewall_active, firewall_time
global firewall_cooldown, game_state, bad_answers