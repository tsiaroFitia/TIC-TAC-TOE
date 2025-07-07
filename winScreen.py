import pygame
import sys

pygame.init()

# Couleurs
BLUE = (10, 10, 63)
YELLOW = (255, 215, 0)
RED = (255, 60, 56)
WHITE = (255, 255, 255)
DARK_BLUE = (5, 5, 40)

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Win Screen")

def draw_win_screen(winner):
    screen.fill(DARK_BLUE)

    # Police plus simple, plus petite, sans gras
    font_big = pygame.font.SysFont("arial", 50)  # taille 50, pas bold
    font_button = pygame.font.SysFont("arial", 36, bold=True)  # bouton un peu plus grand

    # Message gagnant avec couleurs conditionnelles
    text_color = YELLOW if winner == "O" else RED
    win_message = f"Player {winner} Wins!"
    text_surf = font_big.render(win_message, True, text_color)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 3 - 30))

    # Bouton RESTART
    button_width, button_height = 180, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 60
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Bouton jaune avec ombre et arrondi
    mouse_pos = pygame.mouse.get_pos()
    button_color = (255, 240, 100) if button_rect.collidepoint(mouse_pos) else (255, 215, 0)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)

    # Texte RESTART centré et coloré en bleu foncé
    text_restart = font_button.render("RESTART", True, DARK_BLUE)
    screen.blit(text_restart, (button_x + (button_width - text_restart.get_width()) // 2,
                               button_y + (button_height - text_restart.get_height()) // 2))

    pygame.display.flip()

    return button_rect

def main(winner):
    while True:
        button_rect = draw_win_screen(winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    import startScreen
                    startScreen.main()
                    return

if __name__ == "__main__":
    main("X")
