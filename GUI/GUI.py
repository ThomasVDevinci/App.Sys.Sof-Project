import pygame
from src.ConnectFour import ConnectFour

player_colors = {'X': 'yellow', 'O': 'red'}

pygame.init()
pygame.mixer.music.load('../src/background.mp3')
pygame.mixer.music.play(-1)
rows = 6  # Replace with the number of rows you want
columns = 7  # Replace with the number of columns you want
cell_size = min(700 // columns, 700 // (rows + 1))  # Calculate cell size based on board dimensions
screen = pygame.display.set_mode((cell_size * columns, cell_size * (rows + 1)))  # Calculate screen size based on board dimensions
running = True
font = pygame.font.Font(None, 84)
game = ConnectFour(rows, columns)
offset_y = 50

def display_turn(display, player):
    font = pygame.font.Font(None, 36)
    color = "yellow" if player == 'O' else "red"
    text = font.render(f"{color} player's turn", True, (255, 255, 255))
    display.blit(text, (350 - text.get_width() // 2, 10))


def draw_grid(display, board):
    for i in range(game.rows):
        for j in range(game.columns):
            pygame.draw.circle(display, (255, 255, 255), (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2 + offset_y), cell_size // 2 - 5)
            if board[i][j] != ' ':
                color = (255, 0, 0) if board[i][j] == 'X' else (255, 255, 0)
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
            if game.drop_piece(column):  # Only switch player if a piece was successfully dropped
                game.switch_player()
            win_coordinates = game.check_win()
            if win_coordinates:
                pygame.display.set_caption(
                    f"Player {game.current_player} wins!")
                game_over = True
                pygame.mixer.music.stop()
                win_sound = pygame.mixer.Sound('../src/win.mp3')
                win_sound.play()
    screen.fill("blue")
    display_turn(screen, game.current_player)
    draw_grid(screen, game.board)
    if game_over:
        start_pos = (
            win_coordinates[0][1] * cell_size + cell_size // 2,
            win_coordinates[0][0] * cell_size + cell_size // 2 + offset_y)
        end_pos = (
            win_coordinates[-1][1] * cell_size + cell_size // 2,
            win_coordinates[-1][0] * cell_size + cell_size // 2 + offset_y)
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
