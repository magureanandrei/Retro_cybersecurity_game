import pygame
import random
import time
from Punishments import draw_hacked_screen, draw_small_text, draw_lives, draw_text, draw_game_over_screen, draw_phishing_screen,ask_security_question,loadStartGame,loadGame
from Declaring import *


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

def main():

    # Initialize game variables
    running = True
    clock = pygame.time.Clock()
    pachete = []
    input_text = ""
    # server_health = 100
    # global score
    score = 0
    lives = INITIAL_LIVES
    firewall_active = False
    firewall_time = 0
    firewall_cooldown = 0
    firewall_max_cooldown = 10
    game_state = "playing"
    last_spawn_time = time.time()
    show_hint = False
    hint_flash_timer = 0
    phishing_email = None
    valid_email = None
    wrong_command_message = ""
    wrong_command_timer = 0
    min_spawn_interval = 1.0
    correct_answear =""
    bad_answers = 0
    right_answers = 0
    hack_start_time = 0
    hack_time_limit = BASE_HACK_TIME_LIMIT
    loadStartGame()
    # Initial packets
    for i in range(3):
        packet = create_packet(0, pachete)
        if packet:
            pachete.append(packet)
        time.sleep(0.1)

    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                #Verifica enter apasat
                elif event.key == pygame.K_RETURN:
                    if game_state == "hacked":
                        if input_text == HACK_RECOVERY_COMMAND:
                            game_state = "playing"
                            bad_answers = 0
                            right_answers = 0
                            pachete = [create_packet(score, pachete) for _ in range(3)]
                        input_text = ""
                    elif game_state == "phishing":
                        # Check if the player typed the correct response to phishing
                        bad_answers = 0
                        right_answers = 0
                        if input_text == "IGNORE":
                            score+=100
                            wrong_command_message = "Good job! You avoided the phishing attempt."
                            wrong_command_timer = current_time
                            game_state = "playing"
                        elif input_text == "CLICK":
                            wrong_command_message = "You fell for the phishing attempt! -20 health."
                            wrong_command_timer = current_time
                            game_state = "playing"
                        pachete = [create_packet(score, pachete) for _ in range(3)]
                        input_text = ""
                    elif game_state == "validEmail":
                        # Check if the player typed the correct response to phishing
                        bad_answers = 0
                        right_answers = 0
                        if input_text == "IGNORE":
                            wrong_command_message = "This was no phising attempt!"
                            wrong_command_timer = current_time
                            game_state = "playing"
                        elif input_text == "CLICK":
                            score+=100
                            wrong_command_message = "Good job! The email was legit."
                            wrong_command_timer = current_time
                            game_state = "playing"
                        pachete = [create_packet(score, pachete) for _ in range(3)]
                        input_text = ""
                    elif game_state == "security":
                        # Check if the player typed the correct response to security
                        bad_answers = 0
                        right_answers = 0
                        if input_text==correct_answear:
                            score+=100
                        pachete = [create_packet(score, pachete) for _ in range(3)]
                        game_state = "playing"
                        input_text = ""
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
                                    right_answers += 1
                                    packet_matched = True
                                    break

                            if not packet_matched:
                                bad_answers += 1
                                wrong_command_message = f"Wrong command! Bad answers: {bad_answers}/{MAX_BAD_ANSWERS}"
                                wrong_command_timer = current_time

                                if bad_answers >= MAX_BAD_ANSWERS:
                                    game_state = random.choice(["hacked","phishing","validEmail","security"])
                                    hack_start_time = current_time
                                    hack_time_limit = BASE_HACK_TIME_LIMIT + right_answers
                            input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode.upper()

        if game_state == "playing":
            # Draw background
            if use_images:
                loadGame()
            else:
                screen.fill(BLACK)

            if bad_answers == 5:
                lives-=1
                if lives>0:
                    game_state = random.choice(["hacked","phishing","validEmail","security"])
                    if game_state == "phishing":
                        phishing_email = random.choice([
                            {"sender": "admin@security-alerts.com", "subject": "Verify Your Account",
                             "body": "Click the link below to secure your account."},
                            {"sender": "it-support@company.com", "subject": "Password Expiry Notice",
                             "body": "Your password will expire in 24 hours. Reset it now."},
                            {"sender": "lottery@winner.com", "subject": "You’ve Won!",
                             "body": "Claim your $1,000,000 prize now by providing your bank details."},
                        ])
                    elif game_state == "validEmail":
                        valid_email = random.choice([
                            {"sender": "google@google.com", "subject": "Verify Your Account",
                             "body": "Click the link below to secure your account."},
                            {"sender": "it@company.com", "subject": "Password Expiry Notice",
                             "body": "Your password will expire in 24 hours. Reset it now."},
                            {"sender": "lottery@winner.com", "subject": "You’ve Won!",
                             "body": "Claim your $10,000,000 prize now by providing your bank details."},
                        ])
                    elif game_state == "security":
                        correct_answear=random.choice(questions)[2]
                    input_text = ""
                else:
                    game_state = "game_over"
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
                            hack_start_time = current_time
                            hack_time_limit = BASE_HACK_TIME_LIMIT + right_answers
                            lives -= 1
                            if lives > 0:
                                game_state = random.choice(["hacked","phishing","validEmail","security"])
                                if game_state == "phishing":
                                    phishing_email = random.choice([
                                        {"sender": "admin@security-alerts.com", "subject": "Verify Your Account",
                                         "body": "Click the link below to secure your account."},
                                        {"sender": "it-support@company.com", "subject": "Password Expiry Notice",
                                         "body": "Your password will expire in 24 hours. Reset it now."},
                                        {"sender": "lottery@winner.com", "subject": "You’ve Won!",
                                         "body": "Claim your $1,000,000 prize now by providing your bank details."},
                                    ])
                                elif game_state == "validEmail":
                                    valid_email = random.choice([
                                        {"sender": "google@google.com", "subject": "Verify Your Account",
                                         "body": "Click the link below to secure your account."},
                                        {"sender": "it@company.com", "subject": "Password Expiry Notice",
                                         "body": "Your password will expire in 24 hours. Reset it now."},
                                        {"sender": "lottery@winner.com", "subject": "You’ve Won!",
                                         "body": "Claim your $10,000,000 prize now by providing your bank details."},
                                    ])
                                elif game_state == "security":
                                    correct_answear = random.choice(questions)[2]
                                input_text = ""
                            else:
                                game_state = "game_over"
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
            draw_text(screen, f"Right Answers: {right_answers}", 10, 40, GREEN,font)  # Display right answers
            draw_text(screen, f"Bad Answers: {bad_answers}/{MAX_BAD_ANSWERS}", 10, 80, RED,font)
            draw_text(screen, f"Score: {score}", 10, 120, GREEN,font)

            # Command line UI
            pygame.draw.rect(screen, DARK_GRAY, (10, WINDOW_HEIGHT - 50, WINDOW_WIDTH - 20, 40))
            draw_text(screen, f">{input_text}_", 20, WINDOW_HEIGHT - 40, GREEN,font1)

            if current_time - wrong_command_timer < 2:
                draw_text(screen, wrong_command_message, WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT - 90, RED,font)

            if current_time - firewall_cooldown < firewall_max_cooldown:
                remaining_time = max(0, firewall_max_cooldown - (current_time - firewall_cooldown))
                draw_text(screen, f"Firewall Cooldown: {int(remaining_time)}s", 10, 170, LIGHT_ORANGE,font)

            current_speed = calculate_packet_speed(INITIAL_PACKET_SPEED, score)
            draw_small_text(screen, f"Packet Speed: {current_speed:.1f}x",
                            WINDOW_WIDTH - 150, 70, WHITE)

        elif game_state == "hacked":
            time_remaining = hack_time_limit - (current_time - hack_start_time)

            if time_remaining <= 0:
                lives -= 1
                if lives > 0:
                    game_state = "playing"
                    pachete = [create_packet(score, pachete) for _ in range(3)]
                else:
                    game_state = "game_over"
            else:
                draw_hacked_screen(input_text, time_remaining)
        elif game_state == "phishing":
            draw_phishing_screen(phishing_email, input_text)
        elif game_state == "validEmail":
            draw_phishing_screen(valid_email,input_text)
        elif game_state =="security":
            ask_security_question(input_text, correct_answear)

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


            draw_game_over_screen(score)

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

main()