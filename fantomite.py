import pygame
import random
import time

# Initialize Pygame
pygame.init()

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

# Game configuration
INITIAL_PACKET_SPEED = 3
SPEED_INCREASE_FACTOR = 0.2  # Speed increase per 20 points
INITIAL_LIVES = 3
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

# Load images
try:
    bg = pygame.image.load("retropicture.jpg")
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
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


def calculate_packet_speed(base_speed, score):
    speed_multiplier = 1 + (score // 20) * SPEED_INCREASE_FACTOR
    return base_speed * speed_multiplier


def find_safe_position(pachete, word_width=80, word_height=30):
    """Find a safe position for a new packet that doesn't overlap with existing packets."""
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
    """Create a new packet with collision prevention."""
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
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(RED)
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))
    draw_large_text(screen, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, RED)
    draw_large_text(screen, f"Final Score: {score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20, WHITE)


def main():
    global running, input_text, server_health, score, firewall_active, firewall_time
    global firewall_cooldown, game_state

    # Initialize game variables
    running = True
    clock = pygame.time.Clock()
    pachete = []
    input_text = ""
    server_health = 50
    score = 0
    lives = INITIAL_LIVES
    firewall_active = False
    firewall_time = 0
    firewall_cooldown = 0
    firewall_max_cooldown = 10
    game_state = "playing"
    last_spawn_time = time.time()
    min_spawn_interval = 1.0

    # Initial packets
    for i in range(3):
        packet = create_packet(0, pachete)
        if packet:
            pachete.append(packet)
        time.sleep(0.1)

    while running:
        # Draw background
        if use_images:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(BLACK)

        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if game_state == "playing":
                        for packet in pachete[:]:
                            if input_text == packet["word"]:
                                pachete.remove(packet)
                                if packet["type"] == "legitimate":
                                    score += 5
                                elif packet["type"] == "malicious":
                                    score += 10
                                elif packet["type"] == "virus":
                                    score += 15
                                else:  # flood
                                    score += 8
                                break
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode.upper()

        if game_state == "playing":
            if pygame.key.get_pressed()[pygame.K_SPACE] and not firewall_active:
                firewall_active = True
                firewall_time = current_time
                firewall_cooldown = current_time

            # Spawn new packets
            if current_time - last_spawn_time > min_spawn_interval:
                if len(pachete) < 5:
                    new_packet = create_packet(score, pachete)
                    if new_packet:
                        pachete.append(new_packet)
                        last_spawn_time = current_time

            # Update packets
            for packet in pachete[:]:
                packet["y"] += packet["speed"]

                if packet["y"] > WINDOW_HEIGHT - 100:
                    if packet["type"] != "legitimate":
                        damage = 15 if packet["type"] == "virus" else 10 if packet["type"] == "malicious" else 5
                        server_health -= damage
                        if server_health <= 0:
                            lives -= 1
                            if lives > 0:
                                server_health = 50
                            else:
                                game_state = "game_over"
                    pachete.remove(packet)

            # Draw packets
            for packet in pachete:
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

            # Draw UI elements
            draw_text(screen, f"Lives: {lives}", 10, 10, RED)
            draw_text(screen, f"Server Health: {server_health}", 10, 50, WHITE)
            draw_text(screen, f"Score: {score}", 10, 90, GREEN)
            draw_text(screen, f"Input: {input_text}", 10, 130, GREEN)
            draw_text(screen, "Type the words to destroy viruses!", WINDOW_WIDTH - 400, 10, WHITE)
            draw_small_text(screen, "Red: Malicious | Green: Virus | Yellow: Flood | Blue: Legitimate",
                            WINDOW_WIDTH - 490, 40, WHITE)

            if current_time - firewall_cooldown < firewall_max_cooldown:
                remaining_time = max(0, firewall_max_cooldown - (current_time - firewall_cooldown))
                draw_text(screen, f"Firewall Cooldown: {int(remaining_time)}s", 10, 170, LIGHT_ORANGE)

            # Speed indicator
            current_speed = calculate_packet_speed(INITIAL_PACKET_SPEED, score)
            draw_small_text(screen, f"Packet Speed: {current_speed:.1f}x",
                            WINDOW_WIDTH - 150, 70, WHITE)

        elif game_state == "game_over":
            draw_game_over_screen()
            pygame.display.flip()
            time.sleep(3)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()