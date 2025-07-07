import pygame
import sys
from enum import Enum

# Initialisation
pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
GRID_SIZE = 3
CELL_SIZE = 150
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = 150

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
GREEN = (50, 150, 50)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
HOVER_GREEN = (100, 200, 100)
HOVER_BLUE = (100, 150, 250)

# États du jeu
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        
        # Polices
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 40)
        self.info_font = pygame.font.SysFont("Arial", 30)
        
        # État du jeu
        self.state = GameState.MENU
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = "X"
        self.winner = None
        self.game_mode = None  # "PvP" ou "PvAI"
        
        # Boutons
        self.pvp_btn = None
        self.pvai_btn = None
        self.quit_btn = None
        self.back_btn = None
        self.restart_btn = None
        
    def draw_text(self, text, font, color, x, y, centered=True):
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(x, y, width, height)
        
        # Changement de couleur si survolé
        fill_color = hover_color if btn_rect.collidepoint(mouse_pos) else color
        
        pygame.draw.rect(self.screen, fill_color, btn_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, btn_rect, 2, border_radius=10)
        
        self.draw_text(text, self.button_font, BLACK, x + width//2, y + height//2)
        return btn_rect
    
    def draw_menu(self):
        self.screen.fill(WHITE)
        
        # Titre
        self.draw_text("TIC TAC TOE", self.title_font, BLUE, 
                      SCREEN_WIDTH//2, 100)
        
        # Boutons
        btn_width, btn_height = 300, 60
        x_pos = SCREEN_WIDTH//2 - btn_width//2
        
        self.pvp_btn = self.draw_button("Player vs Player", x_pos, 250, 
                                      btn_width, btn_height, GREEN, HOVER_GREEN)
        self.pvai_btn = self.draw_button("Player vs AI", x_pos, 330, 
                                       btn_width, btn_height, BLUE, HOVER_BLUE)
        self.quit_btn = self.draw_button("Quit", x_pos, 410, 
                                       btn_width, btn_height, RED, (255, 150, 150))
    
    def draw_game(self):
        self.screen.fill(WHITE)
        
        # Header avec joueur actuel
        header_text = f"Player {self.current_player}'s turn"
        header_color = BLUE if self.current_player == "X" else GREEN
        self.draw_text(header_text, self.info_font, header_color, 
                      SCREEN_WIDTH//2, 80)
        
        # Dessiner la grille
        grid_rect = pygame.Rect(GRID_OFFSET_X, GRID_OFFSET_Y, 
                               GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE)
        pygame.draw.rect(self.screen, BLACK, grid_rect, 2)
        
        # Lignes de la grille
        for i in range(1, GRID_SIZE):
            # Lignes verticales
            pygame.draw.line(self.screen, DARK_GRAY, 
                           (GRID_OFFSET_X + i*CELL_SIZE, GRID_OFFSET_Y), 
                           (GRID_OFFSET_X + i*CELL_SIZE, GRID_OFFSET_Y + GRID_SIZE*CELL_SIZE), 2)
            # Lignes horizontales
            pygame.draw.line(self.screen, DARK_GRAY, 
                           (GRID_OFFSET_X, GRID_OFFSET_Y + i*CELL_SIZE), 
                           (GRID_OFFSET_X + GRID_SIZE*CELL_SIZE, GRID_OFFSET_Y + i*CELL_SIZE), 2)
        
        # Dessiner les X et O
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col]:
                    x_pos = GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                    y_pos = GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                    
                    if self.board[row][col] == "X":
                        self.draw_x(x_pos, y_pos)
                    else:
                        self.draw_o(x_pos, y_pos)
        
        # Bouton retour
        self.back_btn = self.draw_button("Menu", 20, SCREEN_HEIGHT-70, 
                                       100, 50, LIGHT_GRAY, DARK_GRAY)
    
    def draw_x(self, x, y):
        size = CELL_SIZE // 3
        pygame.draw.line(self.screen, BLUE, (x-size, y-size), (x+size, y+size), 5)
        pygame.draw.line(self.screen, BLUE, (x-size, y+size), (x+size, y-size), 5)
    
    def draw_o(self, x, y):
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.screen, GREEN, (x, y), radius, 5)
    
    def draw_game_over(self):
        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Message de fin de jeu
        if self.winner:
            message = f"Player {self.winner} wins!"
            color = BLUE if self.winner == "X" else GREEN
        else:
            message = "It's a draw!"
            color = BLACK
            
        self.draw_text(message, self.title_font, color, 
                      SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
        
        # Boutons
        btn_width, btn_height = 200, 60
        x_pos = SCREEN_WIDTH//2 - btn_width//2
        
        self.restart_btn = self.draw_button("Play Again", x_pos, SCREEN_HEIGHT//2 + 50, 
                                          btn_width, btn_height, GREEN, HOVER_GREEN)
        self.back_btn = self.draw_button("Main Menu", x_pos, SCREEN_HEIGHT//2 + 130, 
                                       btn_width, btn_height, BLUE, HOVER_BLUE)
    
    def handle_click(self, pos):
        if self.state == GameState.MENU:
            if self.pvp_btn.collidepoint(pos):
                self.state = GameState.PLAYING
                self.game_mode = "PvP"
                self.reset_game()
            elif self.pvai_btn.collidepoint(pos):
                self.state = GameState.PLAYING
                self.game_mode = "PvAI"
                self.reset_game()
            elif self.quit_btn.collidepoint(pos):
                return False
        
        elif self.state == GameState.PLAYING:
            if self.back_btn.collidepoint(pos):
                self.state = GameState.MENU
            else:
                # Vérifier si le clic est dans la grille
                if (GRID_OFFSET_X <= pos[0] <= GRID_OFFSET_X + GRID_SIZE*CELL_SIZE and
                    GRID_OFFSET_Y <= pos[1] <= GRID_OFFSET_Y + GRID_SIZE*CELL_SIZE):
                    
                    row = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
                    col = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
                    
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and not self.board[row][col]:
                        self.board[row][col] = self.current_player
                        
                        if self.check_winner():
                            self.winner = self.current_player
                            self.state = GameState.GAME_OVER
                        elif self.is_board_full():
                            self.state = GameState.GAME_OVER
                        else:
                            self.current_player = "O" if self.current_player == "X" else "X"
                            
                            # Tour de l'IA si en mode PvAI
                            if self.game_mode == "PvAI" and self.current_player == "O":
                                self.ai_move()
        
        elif self.state == GameState.GAME_OVER:
            if self.restart_btn.collidepoint(pos):
                self.reset_game()
                self.state = GameState.PLAYING
            elif self.back_btn.collidepoint(pos):
                self.state = GameState.MENU
        
        return True
    
    def ai_move(self):
        """Simple mouvement aléatoire de l'IA (peut être amélioré avec un algorithme plus intelligent)"""
        import random
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if not self.board[r][c]]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = "O"
            
            if self.check_winner():
                self.winner = "O"
                self.state = GameState.GAME_OVER
            elif self.is_board_full():
                self.state = GameState.GAME_OVER
            else:
                self.current_player = "X"
    
    def check_winner(self):
        # Vérifier les lignes
        for row in self.board:
            if all(cell == self.current_player for cell in row):
                return True
        
        # Vérifier les colonnes
        for col in range(GRID_SIZE):
            if all(self.board[row][col] == self.current_player for row in range(GRID_SIZE)):
                return True
        
        # Vérifier les diagonales
        if all(self.board[i][i] == self.current_player for i in range(GRID_SIZE)):
            return True
        if all(self.board[i][GRID_SIZE-1-i] == self.current_player for i in range(GRID_SIZE)):
            return True
        
        return False
    
    def is_board_full(self):
        return all(all(cell is not None for cell in row) for row in self.board)
    
    def reset_game(self):
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = "X"
        self.winner = None
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.handle_click(event.pos):
                        running = False
            
            # Affichage
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.GAME_OVER:
                self.draw_game()  # Dessiner le plateau en arrière-plan
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()