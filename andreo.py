import pygame
import random
import time
import drawRectangle

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load background music (make sure the file is in the same folder as the game or provide the correct path)
pygame.mixer.music.load('retro_music.mp3')  # Replace 'retro_music.mp3' with your file

# Set volume (optional)
pygame.mixer.music.set_volume(0.2)  # Volume range: 0.0 to 1.0

# Start playing the music in a loop
pygame.mixer.music.play(-1)  # The '-1' argument makes the music loop indefinitely

# Window dimensions
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
HACK_HINT_MESSAGE = "Hint: Use system termination command to eliminate threats..."

# Game configuration
INITIAL_PACKET_SPEED = 2
SPEED_INCREASE_FACTOR = 0.2
INITIAL_LIVES = 3
MAX_BAD_ANSWERS = 5
SHIP_SIZE = (60, 60)
BASE_HACK_TIME_LIMIT = 10

# [Word lists remain the same]
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


# [Setup code remains the same until the main game loop]
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cyber Defense Word Game")

# my code

def loadGame():
    bg = pygame.image.load("retropicture.jpg")
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(bg, (0, 0))

def loadStartGame():
    drawRectangle.start_screen()

# my code

# Load images
try:
    malicious_ship = pygame.transform.scale(pygame.image.load("enemy_red.png"), SHIP_SIZE)
    virus_ship = pygame.transform.scale(pygame.image.load("enemy_green.png"), SHIP_SIZE)
    flood_ship = pygame.transform.scale(pygame.image.load("enemy_yellow.png"), SHIP_SIZE)
    legitimate_ship = pygame.transform.scale(pygame.image.load("friendly_blue.png"), SHIP_SIZE)
    use_images = True
except pygame.error:
    use_images = False
    print("Image files not found. Falling back to colored rectangles.")

# Font
font = pygame.font.Font(pygame.font.get_default_font(), 24)
small_font = pygame.font.Font(pygame.font.get_default_font(), 16)
large_font = pygame.font.Font(pygame.font.get_default_font(), 32)


def draw_text(surface, text, x, y, color):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))


def draw_small_text(surface, text, x, y, color):
    text_obj = small_font.render(text, True, color)
    surface.blit(text_obj, (x, y))


def draw_large_text(surface, text, x, y, color):
    text_obj = large_font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_lives(surface, lives):
    for i in range(lives):
        pygame.draw.circle(surface, RED, (30 + i * 30, 20), 10)


def calculate_packet_speed(base_speed, score):
    speed_multiplier = 1 + (score // 20) * SPEED_INCREASE_FACTOR
    return base_speed * speed_multiplier


def find_safe_position(pachete, word_width=80, word_height=30):
    max_attempts = 50
    min_vertical_spacing = 60

    for _ in range(max_attempts):
        x = random.randint(0, WINDOW_WIDTH - word_width)
        position_safe = True

        for packet in pachete:
            vertical_distance = abs(packet["y"] - 0)
            if vertical_distance < min_vertical_spacing and abs(packet["x"] - x) < word_width:
                position_safe = False
                break

        if position_safe:
            return x

    return None


def create_packet(score, pachete):
    x = find_safe_position(pachete)
    if x is None:
        return None

    y = 0
    attack_type = random.choice(["malicious", "legitimate", "virus", "flood"])

    if attack_type == "malicious":
        word = random.choice(MALICIOUS_WORDS)
        color = RED
        ship_img = malicious_ship if use_images else None
    elif attack_type == "virus":
        word = random.choice(VIRUS_WORDS)
        color = GREEN
        ship_img = virus_ship if use_images else None
    elif attack_type == "flood":
        word = random.choice(FLOOD_WORDS)
        color = ORANGE
        ship_img = flood_ship if use_images else None
    else:
        word = random.choice(LEGITIMATE_WORDS)
        color = BLUE
        ship_img = legitimate_ship if use_images else None

    base_speed = calculate_packet_speed(INITIAL_PACKET_SPEED, score)
    speed = base_speed * random.uniform(0.8, 1.2)

    packet = {
        "x": x,
        "y": y,
        "type": attack_type,
        "color": color,
        "word": word,
        "speed": speed,
        "width": SHIP_SIZE[0] if use_images else 80,
        "height": SHIP_SIZE[1] if use_images else 30
    }

    if use_images:
        packet["image"] = ship_img

    return packet

def draw_game_over_screen():
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(RED)
    overlay.set_alpha(150)  # Adjust alpha for transparency
    screen.blit(overlay, (0, 0))

    # Game over text
    draw_large_text(screen, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, WHITE)
    draw_large_text(screen, f"Final Score: {score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20, YELLOW)
    draw_text(screen, "Press ENTER to Restart", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, GREEN)


def draw_hacked_screen(input_text, time_remaining):
    screen.fill(BLACK)

    # Create glitch effect
    for _ in range(10):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        width = random.randint(50, 200)
        height = random.randint(2, 5)
        pygame.draw.rect(screen, DARK_RED, (x, y, width, height))

    draw_large_text(screen, "! YOU'VE BEEN HACKED !", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3, RED)
    draw_large_text(screen, f"BAD ANSWERS: {bad_answers}/{MAX_BAD_ANSWERS}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30, RED)
    draw_large_text(screen, f"TIME REMAINING: {int(time_remaining)}s", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, YELLOW)

    fake_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    draw_text(screen, f"IP: {fake_ip}", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 80, WHITE)

    draw_text(screen, HACK_HINT_MESSAGE, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 150, PURPLE)
    draw_text(screen, f"Enter command: {input_text}", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 100, GREEN)


def main():
    global running, input_text, score, firewall_active, firewall_time
    global firewall_cooldown, game_state, score, bad_answers

    # Initialize game variables
    running = True
    clock = pygame.time.Clock()
    pachete = []
    input_text = ""
    score = 0
    lives = INITIAL_LIVES
    bad_answers = 0
    right_answers = 0  # Track correct answers
    firewall_active = False
    firewall_time = 0
    firewall_cooldown = 0
    firewall_max_cooldown = 10
    game_state = "playing"
    last_spawn_time = time.time()
    hack_start_time = 0
    hack_time_limit = BASE_HACK_TIME_LIMIT
    show_hint = False
    hint_flash_timer = 0
    wrong_command_message = ""
    wrong_command_timer = 0
    min_spawn_interval = 1.0

    loadStartGame()

    # Initial packets
    for i in range(3):
        packet = create_packet(0, pachete)
        if packet:
            pachete.append(packet)
        time.sleep(0.1)

    while running:
        loadGame()
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if game_state == "hacked":
                        if input_text == HACK_RECOVERY_COMMAND:
                            game_state = "playing"
                            bad_answers = 0
                            right_answers = 0  # Reset right answers after the hacked screen
                            score += 100  # Gain 100 points for successful recovery
                            pachete = [create_packet(score, pachete) for _ in range(3)]
                            input_text = ""
                        else:
                            # Incorrect command, lose a life and exit hacked screen
                            lives -= 1
                            if lives > 0:
                                # Return to normal gameplay if lives remain
                                game_state = "playing"
                                bad_answers = 0
                                right_answers = 0  # Reset right answers
                                pachete = [create_packet(score, pachete) for _ in range(3)]
                            else:
                                # Game over if no lives remain
                                game_state = "game_over"
                            input_text = ""  # Clear input text
                    elif game_state == "playing":
                        if input_text == RECOVERY_COMMAND:
                            if not firewall_active and current_time - firewall_cooldown >= firewall_max_cooldown:
                                firewall_active = True
                                firewall_time = current_time
                                firewall_cooldown = current_time
                                score += 10
                            input_text = ""
                        else:
                            packet_matched = False
                            for packet in pachete[:]:
                                if input_text == packet["word"]:
                                    pachete.remove(packet)
                                    score += 10  # Fixed gain for correct typing
                                    right_answers += 1  # Increment right answers
                                    packet_matched = True
                                    break
                            if not packet_matched:
                                bad_answers += 1
                                wrong_command_message = f"Wrong command! Bad answers: {bad_answers}/{MAX_BAD_ANSWERS}"
                                wrong_command_timer = current_time

                                if bad_answers >= MAX_BAD_ANSWERS:
                                    game_state = "hacked"
                                    hack_start_time = current_time
                                    hack_time_limit = BASE_HACK_TIME_LIMIT + right_answers  # Add bonus time based on right answers
                            input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode.upper()

        if game_state == "playing":
            # Draw background
            if use_images:
                # screen.blit(bg, (0, 0))
                loadGame()
            else:
                screen.fill(BLACK)

            # Spawn new packets
            if current_time - last_spawn_time > min_spawn_interval:
                if len(pachete) < 5:
                    new_packet = create_packet(score, pachete)
                    if new_packet:
                        pachete.append(new_packet)
                        last_spawn_time = current_time

            # Update and draw packets
            for packet in pachete[:]:
                packet["y"] += packet["speed"]
                if packet["y"] > WINDOW_HEIGHT - 100:
                    score = max(0, score - 10)
                    if packet["type"] != "legitimate":
                        bad_answers += 1
                        if bad_answers >= MAX_BAD_ANSWERS:
                            game_state = "hacked"
                            hack_start_time = current_time
                            hack_time_limit = BASE_HACK_TIME_LIMIT + right_answers
                    pachete.remove(packet)
                else:
                    if use_images:
                        screen.blit(packet["image"], (packet["x"], packet["y"]))
                        draw_small_text(screen, packet["word"],
                                        packet["x"] + packet["width"] // 2 - 20,
                                        packet["y"] + packet["height"] + 5,
                                        WHITE)
                    else:
                        pygame.draw.rect(screen, packet["color"],
                                         (packet["x"], packet["y"], packet["width"], packet["height"]))
                        draw_small_text(screen, packet["word"],
                                        packet["x"] + 5, packet["y"] + 5, WHITE)

            # Draw firewall
            if firewall_active and current_time - firewall_time < 5:
                pygame.draw.rect(screen, LIGHT_ORANGE, (0, 0, WINDOW_WIDTH, 30))
                for packet in pachete[:]:
                    if packet["y"] < 30:
                        pachete.remove(packet)
            else:
                firewall_active = False

            # Draw UI
            draw_lives(screen, lives)  # Draw lives
            draw_text(screen, f"Right Answers: {right_answers}", 10, 40, GREEN)  # Display right answers
            draw_text(screen, f"Bad Answers: {bad_answers}/{MAX_BAD_ANSWERS}", 10, 80, RED)
            draw_text(screen, f"Score: {score}", 10, 120, GREEN)

            # Command line UI
            pygame.draw.rect(screen, DARK_GRAY, (10, WINDOW_HEIGHT - 50, WINDOW_WIDTH - 20, 40))
            draw_text(screen, f">{input_text}_", 20, WINDOW_HEIGHT - 40, GREEN)

            if current_time - wrong_command_timer < 2:
                draw_text(screen, wrong_command_message, WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT - 90, RED)

            if current_time - firewall_cooldown < firewall_max_cooldown:
                remaining_time = max(0, firewall_max_cooldown - (current_time - firewall_cooldown))
                draw_text(screen, f"Firewall Cooldown: {int(remaining_time)}s", 10, 170, LIGHT_ORANGE)

        elif game_state == "hacked":
            time_remaining = hack_time_limit - (current_time - hack_start_time)

            if time_remaining <= 0:
                lives -= 1
                if lives > 0:
                    game_state = "playing"
                    bad_answers = 0
                    right_answers = 0  # Reset right answers after the hacked screen
                    pachete = [create_packet(score, pachete) for _ in range(3)]
                else:
                    game_state = "game_over"
            else:
                draw_hacked_screen(input_text, time_remaining)


        elif game_state == "game_over":

            # Draw the main screen background (use gameplay appearance here)

            if use_images:

                loadGame()

            else:

                screen.fill(BLACK)

            # Optionally draw remaining packets on the screen

            for packet in pachete:

                if use_images and packet.get("image"):

                    screen.blit(packet["image"], (packet["x"], packet["y"]))

                else:

                    pygame.draw.rect(screen, packet["color"],

                                     (packet["x"], packet["y"], packet["width"], packet["height"]))

            # Add the "Game Over" overlay on top of the gameplay screen

            draw_game_over_screen()

            # Check for input to restart the game

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:  # Restart game with Enter key

                        # Reset all game variables

                        lives = INITIAL_LIVES

                        score = 0

                        bad_answers = 0

                        right_answers = 0

                        firewall_active = False

                        firewall_time = 0

                        firewall_cooldown = 0

                        game_state = "playing"

                        pachete = [create_packet(score, pachete) for _ in range(3)]

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


