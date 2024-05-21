import pygame

class GUI:
    def __init__(self, screen, game, cell_size, offset_y):
        self.screen = screen
        self.game = game
        self.cell_size = cell_size
        self.offset_y = offset_y

    def draw_menu(self, display):
        menu_width = 100
        menu_height = 25
        menu_x = display.get_width() - menu_width - 10
        menu_y = display.get_height() - menu_height - 10
        button_width = menu_width // 2 - 10
        button_height = menu_height
        pygame.draw.rect(display, (100, 100, 100), (menu_x, menu_y, button_width, button_height))
        pygame.draw.rect(display, (100, 100, 100), (menu_x + button_width + 10, menu_y, button_width, button_height))
        font = pygame.font.Font(None, 18)
        quit_text = font.render("Quit", True, (0, 0, 0))
        reset_text = font.render("Reset", True, (0, 0, 0))
        display.blit(quit_text, (menu_x + button_width / 2 - quit_text.get_width() / 2, menu_y + button_height / 2 - quit_text.get_height() / 2))
        display.blit(reset_text, (menu_x + button_width + button_width / 2 - reset_text.get_width() / 2 + 10, menu_y + button_height / 2 - reset_text.get_height() / 2))

    def handle_menu_event(self, event):
        menu_width = 100
        menu_height = 25
        menu_x = self.screen.get_width() - menu_width - 10
        menu_y = self.screen.get_height() - menu_height - 10
        button_width = menu_width // 2 - 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height:
                if menu_x <= x <= menu_x + button_width:
                    return "quit"
                elif menu_x + button_width + 10 <= x <= menu_x + 2 * button_width + 10:
                    return "reset"

    def display_turn(self, display, player):
        font = pygame.font.Font(None, 36)
        color = "yellow" if player == 'O' else "red"
        text = font.render(f"{color} player's turn", True, (255, 255, 255))
        self.screen.blit(font.render(f"{color} player's turn", True, (0, 0, 0)), (350 - text.get_width() // 2 + 5, 10 + 5))
        display.blit(text, (350 - text.get_width() // 2, 10))

    def draw_grid(self, display, board):
        for i in range(self.game.rows):
            for j in range(self.game.columns):
                pygame.draw.circle(display, (255, 255, 255), (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2 + self.offset_y), self.cell_size // 2 - 5)
                if board[i][j] != ' ':
                    color = (255, 0, 0) if board[i][j] == 'X' else (255, 255, 0)
                    pygame.draw.circle(display, color, (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2 + self.offset_y), self.cell_size // 2 - 5)

    def draw_highlight(self, display, column):
        pygame.draw.rect(display, (200, 200, 200), (column * self.cell_size, self.offset_y, self.cell_size, self.cell_size * self.game.rows), 5)
