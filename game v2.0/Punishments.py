import random

import drawRectangle
from Declaring import *
# from fantomite import DARK_RED, screen

bad_answers=0
base_dir = os.path.join(os.getcwd(), "../assets")
image_path = os.path.join(base_dir, "retropicture.jpg")
def loadGame():
    bg = pygame.image.load(image_path)
    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(bg, (0, 0))

def loadStartGame():
    drawRectangle.start_screen()

def draw_text(surface, text, x, y, color,font):
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
        pygame.draw.circle(surface, RED, (30 + i * 30, 30), 10)

def draw_game_over_screen(score):
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(RED)
    overlay.set_alpha(150)  # Adjust alpha for transparency
    screen.blit(overlay, (0, 0))

    # Game over text
    draw_large_text(screen, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, WHITE)
    draw_large_text(screen, f"Final Score: {score}", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20, YELLOW)
    draw_text(screen, "Press ENTER to Restart", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, GREEN,font)

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
    draw_text(screen, f"IP: {fake_ip}", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 80, WHITE,font)

    draw_text(screen, HACK_HINT_MESSAGE, WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 150, PURPLE,font)
    draw_text(screen, f"Enter command: {input_text}", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 100, GREEN,font)

def show_phishing_email():
    phishing_emails = [
        {"sender": "admin@security-alerts.com", "subject": "Verify Your Account", "body": "Click the link below to secure your account."},
        {"sender": "it-support@company.com", "subject": "Password Expiry Notice", "body": "Your password will expire in 24 hours. Reset it now."},
        {"sender": "lottery@winner.com", "subject": "You’ve Won!", "body": "Claim your $1,000,000 prize now by providing your bank details."},
    ]
    selected_email = random.choice(phishing_emails)
    print(f"Phishing Email: From {selected_email['sender']}, Subject: {selected_email['subject']}")
    return selected_email

def show_legit_email():
    real_emails = [
        {"sender": "google@google.com", "subject": "Verify Your Account", "body": "Click the link below to secure your account."},
        {"sender": "it@company.com", "subject": "Password Expiry Notice", "body": "Your password will expire in 24 hours. Reset it now."},
        {"sender": "lottery@winner.com", "subject": "You’ve Won!", "body": "Claim your $10,000,000 prize now by providing your bank details."},
    ]
    selected_email = random.choice(real_emails)
    print(f"Phishing Email: From {selected_email['sender']}, Subject: {selected_email['subject']}")
    return selected_email

def draw_phishing_screen(phishing_email, input_text):
    screen.fill(BLACK)
    for _ in range(10):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        width = random.randint(50, 200)
        height = random.randint(2, 5)
        pygame.draw.rect(screen, DARK_RED, (x, y, width, height))
    draw_large_text(screen, "Possible Phishing Attempt!", WINDOW_WIDTH // 2, 50, RED)
    draw_text(screen, f"From: {phishing_email['sender']}", 50, 100, WHITE,font)
    draw_text(screen, f"Subject: {phishing_email['subject']}", 50, 140, WHITE,font)
    draw_text(screen, phishing_email['body'], 50, 180, YELLOW,font)
    draw_text(screen, "Type 'IGNORE' to avoid the attack or 'CLICK' to fall for it:", 50, 240, GREEN,font)
    pygame.draw.rect(screen, DARK_GRAY, (10, WINDOW_HEIGHT - 50, WINDOW_WIDTH - 20, 40))
    draw_text(screen, f"> {input_text}_", 20, WINDOW_HEIGHT - 40, GREEN,font1)

def ask_security_question(input_text,correct_answer):
    # global score, input_text, game_state
    question = ("Two-factor authentication (2FA) uses two methods to verify your "
                "identity, like a password plus a code sent to your phone. "
                "It adds extra protection if one method is compromised.")
    options = [
        "a) Logging in with a password and a code sent to your phone",
        "b) Using just a strong password",
        "c) Using fingerprint recognition only",
        "d) Scanning a QR code to access your account"
    ]
    # correct_answer = "A"

    # Display the question and options
    screen.fill(BLACK)
    draw_large_text(screen, "Security Question", WINDOW_WIDTH // 2, 100, WHITE)
    draw_text(screen, question, 50, 150, WHITE,font)

    y_offset = 200
    for option in options:
        draw_text(screen, option, 50, y_offset, WHITE,font)
        y_offset += 40

    draw_text(screen, "Type your answer (a/b/c/d):", 50, y_offset, WHITE,font)
    draw_text(screen, f"Your answer: {input_text}", 50, y_offset + 40, GREEN,font)

    # Check for user input
    if input_text in ["A", "B", "C", "D"]:
        if input_text == correct_answer:
            draw_large_text(screen, "Correct! +100 Points", WINDOW_WIDTH // 2, WINDOW_HEIGHT//2 + 200, GREEN)
        else:
            draw_large_text(screen, "Incorrect! Try again.", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200, RED)
        pygame.display.flip()
        # time.sleep(2)  # Pause for 2 seconds to show the result

        # Reset the game state and input text after the answer
