import pygame
import socket
import threading
import time

HOST = '192.168.34.6'  # IP-ul serverului
PORT = 12345
BUFF_SIZE = 1024
GAME_TIME = 3  # Timpul pentru fiecare formă

# Inițializare Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Joc Retro')
font = pygame.font.SysFont('Arial', 24)
score = 0
shapes = []
game_running = True


def receive_data():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b"HELLO", (HOST, PORT))

    global shapes, score, game_running
    while game_running:
        data, _ = client_socket.recvfrom(BUFF_SIZE)
        message = data.decode()
        print(f"Mesaj primit: {message}")  # Debugging mesaj

        if message.startswith("START"):
            parts = message.split()
            color = (int(parts[1]), int(parts[2]), int(parts[3]))
            x, y, radius = int(parts[4]), int(parts[5]), int(parts[6])
            shapes = [(color, x, y, radius)]  # Păstrează doar o formă pe ecran

        elif message.startswith("CURRENT_SCORE"):
            print(score)
            # score = int(message.split()[1])

        elif message == "GAME_OVER":
            print("Jocul s-a terminat!")
            game_running = False


def draw_shapes():
    for shape in shapes:
        pygame.draw.circle(screen, shape[0], (shape[1], shape[2]), shape[3])


def check_click(x, y, shape):
    dist = ((x - shape[1])*2 + (y - shape[2])*2)*0.5
    return dist <= shape[3]


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.sendto(message.encode(), (HOST,PORT))


def main():
    global score, game_running, shapes
    receive_data_thread = threading.Thread(target=receive_data)
    receive_data_thread.start()

    last_click_time = time.time()

    while game_running:
        screen.fill((0, 0, 0))  # Fundal negru retro
        draw_shapes()

        # Verifică evenimente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN and time.time() - last_click_time > 1:
                x, y = pygame.mouse.get_pos()
                for shape in shapes:
                    if check_click(x, y, shape):
                        if shape[0] == (255, 0, 0):  # Formă roșie
                            score -= 10
                        elif shape[0] == (0, 255, 0):  # Formă verde
                            score += 10
                        if score>=100:
                            game_running = False
                            send_message("UPDATE_SCORE" + str(score))
                        shapes = []  # Elimina forma după ce a fost apăsată
                        last_click_time = time.time()  # Previne clickuri prea rapide

        # Afișează scorul
        score_text = font.render(f"Scor: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


main()