import pygame
from src.ConnectFour import ConnectFour

player_colors = {'X': 'yellow', 'O': 'red'}

pygame.init()
screen = pygame.display.set_mode((700, 700))
running = True
font = pygame.font.Font(None, 84)
cell_size = 100
game = ConnectFour()
offset_y = 50

def display_turn(display, player):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {player}'s turn", True, (255, 255, 255))
    display.blit(text, (350 - text.get_width() // 2, 10))


def draw_grid(display, board):
    offset_y = 50  # This is the vertical space reserved for displaying the player's turn
    for i in range(6):
        for j in range(7):
            pygame.draw.rect(display, (255, 255, 255), (j * cell_size, i * cell_size + offset_y, cell_size, cell_size), 1)
            if board[i][j] != ' ':
                color = (255, 0, 0) if board[i][j] == 'X' else (255, 255, 0)  # Assign red to player 'X' and yellow to player 'O'
                pygame.draw.circle(display, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2 + offset_y), cell_size // 2 - 5)

game_over = False
win_coordinates = None
animation_progress = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            column = x // cell_size
            game.drop_piece(column)
            game.switch_player()
            win_coordinates = game.check_win()
            if win_coordinates:
                pygame.display.set_caption(
                    f"Player {game.current_player} wins!")
                game_over = True
    screen.fill("blue")
    display_turn(screen, game.current_player)
    draw_grid(screen, game.board)
    if game_over:
        start_pos = (
            win_coordinates[0][1] * cell_size + cell_size // 2, win_coordinates[0][0] * cell_size + cell_size // 2 + offset_y)
        end_pos = (
            win_coordinates[-1][1] * cell_size + cell_size // 2, win_coordinates[-1][0] * cell_size + cell_size // 2 + offset_y)
        if animation_progress < 100:
            pygame.draw.line(screen, (0, 0, 128), start_pos, (
                start_pos[0] + (end_pos[0] - start_pos[0]) * animation_progress / 100,
                start_pos[1] + (end_pos[1] - start_pos[1]) * animation_progress / 100), 5)
            animation_progress += 1
            pygame.time.wait(20)  #
        else:
            winner_text = font.render(f"Player {player_colors[game.current_player]} wins!", True, (0, 0, 139))
            screen.blit(winner_text, (350 - winner_text.get_width() // 2, 300 - winner_text.get_height() // 2))
    pygame.display.flip()
