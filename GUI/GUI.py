import pygame
from src import Main

pygame.init()
screen = pygame.display.set_mode((700, 600))
running = True
font = pygame.font.Font(None, 84)  # Create a font object with size 216
cell_size = 100  # Size of each cell in the grid

def draw_grid(display, board):
    for i in range(6):  # There are 6 rows in the Connect Four board
        for j in range(7):  # There are 7 columns in the Connect Four board
            pygame.draw.rect(display, (255, 255, 255), (j * cell_size, i * cell_size, cell_size, cell_size), 1)
            if board[i][j] != ' ':
                color = (255, 0, 0) if board[i][j] == 'X' else (
                    255, 255, 0)  # Change the color of the second player's tokens to yellow
                pygame.draw.circle(display, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
                                   cell_size // 2 - 5)

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
            Main.game.drop_piece(column)
            Main.game.switch_player()  # Switch the player immediately after a piece is dropped
            win_coordinates = Main.game.check_win()
            if win_coordinates:
                pygame.display.set_caption(f"Player {Main.game.current_player} wins!")
                game_over = True
    screen.fill("blue")
    draw_grid(screen, Main.game.board)  # Draw the grid on each frame
    if game_over:
        start_pos = (
            win_coordinates[0][1] * cell_size + cell_size // 2, win_coordinates[0][0] * cell_size + cell_size // 2)
        end_pos = (
            win_coordinates[-1][1] * cell_size + cell_size // 2, win_coordinates[-1][0] * cell_size + cell_size // 2)
        if animation_progress < 100:  # Draw a portion of the line in each frame
            pygame.draw.line(screen, (0, 0, 128), start_pos, (
                start_pos[0] + (end_pos[0] - start_pos[0]) * animation_progress / 100,
                start_pos[1] + (end_pos[1] - start_pos[1]) * animation_progress / 100), 5)
            animation_progress += 1
            pygame.time.wait(20)  # Wait for 80 milliseconds before drawing the next segment of the line
        else:  # Once the animation is complete, display the overlay
            winner_text = font.render(f"Player {Main.game.current_player} wins!", True, (255, 255, 255))
            screen.blit(winner_text, (350 - winner_text.get_width() // 2,
                                      300 - winner_text.get_height() // 2))  # Draw the winner text in the middle of the screen
    pygame.display.flip()

while running:  # Keep the window open until the user manually closes it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()