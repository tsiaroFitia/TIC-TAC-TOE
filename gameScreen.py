import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
DARK_BLUE = (10, 10, 63)
LIGHT_BLUE = (100, 160, 255, 120)
RED = (255, 60, 56)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 150)
PLAYER_CARD_COLOR = (50, 50, 100)  # Bleu foncé
ROBOT_CARD_COLOR = (100, 50, 50)   # Rouge foncé

# Dimensions
WIDTH, HEIGHT = 450, 650
CELL_SIZE = 110
MARGIN = 12
BORDER_RADIUS = 20
CARD_WIDTH, CARD_HEIGHT = 140, 100

# Position de la grille
GRID_WIDTH = 3 * CELL_SIZE + 2 * MARGIN
GRID_ORIGIN_X = (WIDTH - GRID_WIDTH) // 2
GRID_ORIGIN_Y = 220

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Polices
symbol_font = pygame.font.SysFont("Arial", 60, bold=True)  # Pour les symboles X/O
title_font = pygame.font.SysFont("Arial", 24, bold=True)    # Pour le titre
player_font = pygame.font.SysFont("Arial", 22, bold=True)   # Pour les noms joueurs

def create_player_card(title, symbol, main_color, symbol_color):
    """Crée une carte joueur stylisée avec ombre douce, symbole réduit et espace avec le titre"""
    card = pygame.Surface((CARD_WIDTH + 5, CARD_HEIGHT + 12), pygame.SRCALPHA)

    # Ombre floue simulée
    for alpha, offset in [(30, 6), (20, 4), (10, 2)]:
        shadow = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, alpha), shadow.get_rect(), border_radius=BORDER_RADIUS)
        card.blit(shadow, (offset, offset))

    # Surface principale de la carte
    surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, main_color, surface.get_rect(), border_radius=BORDER_RADIUS)
    
    # Symbole centré plus petit
    symbol_font = pygame.font.SysFont("Arial", 36, bold=True)
    symbol_text = symbol_font.render(symbol, True, symbol_color)
    symbol_rect = symbol_text.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2 - 20))
    surface.blit(symbol_text, symbol_rect)

    # Titre (sous le symbole, avec espacement)
    title_text = player_font.render(title, True, WHITE)
    title_rect = title_text.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT - 20))
    surface.blit(title_text, title_rect)

    # Fusion
    card.blit(surface, (0, 0))
    return card


# Création des deux cartes identiques en style mais avec des couleurs et symboles différents
player_card = create_player_card("YOU", "X", (60, 60, 120), RED)
robot_card = create_player_card("ROBOT", "O", (60, 60, 120), YELLOW)

# Positions des cartes
PLAYER_CARD_POS = (WIDTH//4 - CARD_WIDTH//2, 30)
ROBOT_CARD_POS = (3*WIDTH//4 - CARD_WIDTH//2, 30)

# État du jeu
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_win_positions():
    """Vérifie les conditions de victoire"""
    # Lignes horizontales
    for i, row in enumerate(board):
        if row[0] != "" and row.count(row[0]) == 3:
            return row[0], [(i, 0), (i, 1), (i, 2)]
    
    # Lignes verticales
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col], [(0, col), (1, col), (2, col)]
    
    # Diagonales
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    return None, None

def draw_grid():
    """Dessine l'interface complète du jeu"""
    screen.fill(DARK_BLUE)

    
    # Afficher les cartes joueurs
    screen.blit(player_card, PLAYER_CARD_POS)
    screen.blit(robot_card, ROBOT_CARD_POS)
    
    # Bordure pour le joueur actif
    active_color = RED if current_player == "X" else YELLOW
    active_pos = PLAYER_CARD_POS if current_player == "X" else ROBOT_CARD_POS
    pygame.draw.rect(screen, active_color, 
                    (active_pos[0]-3, active_pos[1]-3, 
                     CARD_WIDTH+6, CARD_HEIGHT+6), 
                    3, border_radius=BORDER_RADIUS+3)
    
    # Grille de jeu
    winner, win_positions = check_win_positions()
    
    for i in range(3):
        for j in range(3):
            x = GRID_ORIGIN_X + j * (CELL_SIZE + MARGIN)
            y = GRID_ORIGIN_Y + i * (CELL_SIZE + MARGIN)
            
            # Ombre portée
            shadow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 80))
            screen.blit(shadow, (x + 5, y + 5))
            
            # Case
            cell = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            
            if win_positions and (i, j) in win_positions:
                bg_color = (*YELLOW[:3], 200) if winner == "O" else (*RED[:3], 200)
                pygame.draw.rect(cell, bg_color, (0, 0, CELL_SIZE, CELL_SIZE), border_radius=BORDER_RADIUS)
            else:
                pygame.draw.rect(cell, LIGHT_BLUE, (0, 0, CELL_SIZE, CELL_SIZE), border_radius=BORDER_RADIUS)
            
            # Symbole
            if board[i][j]:
                color = RED if board[i][j] == "X" else YELLOW
                text = symbol_font.render(board[i][j], True, color)
                cell.blit(text, ((CELL_SIZE - text.get_width()) // 2, 
                               (CELL_SIZE - text.get_height()) // 2))
            
            screen.blit(cell, (x, y))
    
    pygame.display.flip()

def main():
    global current_player, board
    board = [["" for _ in range(3)] for _ in range(3)]  # Reset board at start
    current_player = "X"

    clock = pygame.time.Clock()
    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(3):
                    for j in range(3):
                        cell_x = GRID_ORIGIN_X + j * (CELL_SIZE + MARGIN)
                        cell_y = GRID_ORIGIN_Y + i * (CELL_SIZE + MARGIN)
                        rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                        if rect.collidepoint(x, y):
                            if board[i][j] == "":
                                board[i][j] = current_player
                                winner, _ = check_win_positions()
                                if winner:
                                    import winScreen
                                    winScreen.main(winner)
                                    return
                                current_player = "O" if current_player == "X" else "X"
        clock.tick(60)

if __name__ == "__main__":
    main()