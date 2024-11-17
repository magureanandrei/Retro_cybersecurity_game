import pygame
import sys

# Inițializare pygame
pygame.init()

# Setări ecran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecran Start cu Buton")

def loadStartGame():
    bg = pygame.image.load("wordGuard.jpg")
    bg = pygame.transform.scale(bg, (screen_width,screen_height))
    screen.blit(bg, (0, 0))

# Culori
black = (0, 0, 0)
white = (255, 255, 255)

# Încarcă imaginea butonului
button_image = pygame.image.load("pressStart.png")

# Funcția pentru a desena butonul
def draw_button(surface, image, x, y, width, height):
    # Desenăm imaginea butonului
    scaled_image = pygame.transform.scale(image, (width, height))
    surface.blit(scaled_image, (x, y))

    # Detectăm click-ul
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y and click[0] == 1:
        return True  # Butonul a fost apăsat

    return False

# Funcția pentru ecranul de start
def start_screen():
    loadStartGame()
    running = True
    while running:
        # Fundal negru
        # Desenează butonul
        if draw_button(screen, button_image, 325, 250, 150, 75):  # Poziționează butonul
            return  # Se finalizează ecranul de start

        # Gestionăm evenimentele
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Actualizează ecranul
        pygame.display.update()
