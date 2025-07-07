import pygame
import sys

pygame.init()

# Couleurs
BLUE = (10, 10, 63)
YELLOW = (255, 215, 0)
YELLOW_HOVER = (255, 240, 100)
RED = (255, 60, 56)
WHITE = (255, 255, 255)
DARK_BLUE = (5, 5, 40)

# Fenêtre
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Start Screen")

def draw_start_screen():
    screen.fill(DARK_BLUE)
    
    # Police stylée et grasse
    title_font = pygame.font.SysFont("impact", 80, bold=True)
    subtitle_font = pygame.font.SysFont("segoeui", 24, italic=True)
    button_font = pygame.font.SysFont("impact", 50, bold=True)  # taille 50 pour correspondre au win.py

    # Texte principal
    title_text = ["TIC", "TAC", "TOE"]
    colors = [YELLOW, RED]

    # Placement vertical
    total_title_height = len(title_text) * 90
    start_y = HEIGHT // 3 - total_title_height // 2

    for i, word in enumerate(title_text):
        # Largeur totale avec espacement entre lettres
        char_widths = [title_font.size(c)[0] for c in word]
        total_width = sum(char_widths) + (len(word)-1)*10
        x = WIDTH // 2 - total_width // 2
        y = start_y + i * 90

        for j, char in enumerate(word):
            color = colors[(i + j) % 2]
            char_surf = title_font.render(char, True, color)
            screen.blit(char_surf, (x, y))
            x += char_surf.get_width() + 10

    # Sous-titre
    subtitle = "Play With IA"
    subtitle_surf = subtitle_font.render(subtitle, True, WHITE)
    screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, start_y + 280))

    # Bouton START (mêmes dimensions et style que RESTART dans win.py)
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = 450
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Couleur jaune et jaune clair au survol
    mouse_pos = pygame.mouse.get_pos()
    button_color = YELLOW_HOVER if button_rect.collidepoint(mouse_pos) else YELLOW

    pygame.draw.rect(screen, button_color, button_rect, border_radius=15)

    # Texte START centré et en bleu foncé
    text = button_font.render("START", True, DARK_BLUE)
    text_x = button_x + (button_width - text.get_width()) // 2
    text_y = button_y + (button_height - text.get_height()) // 2
    screen.blit(text, (text_x, text_y))

    pygame.display.flip()

    return button_rect

def main():
    while True:
        button_rect = draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    import gameScreen  # Ton fichier de jeu principal
                    gameScreen.main()
                    return

if __name__ == "__main__":
    main()
