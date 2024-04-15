import pygame
from src import Main

pygame.init()
screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption('Connect Four')
running = True


def draw_grid(display, board):
    cell_size = 100  # Size of each cell in the grid
    for i in range(6):  # There are 6 rows in the Connect Four board
        for j in range(7):  # There are 7 columns in the Connect Four board
            pygame.draw.rect(display, (255, 255, 255), (j * cell_size, i * cell_size, cell_size, cell_size), 1)
            if board[i][j] != ' ':
                color = (255, 0, 0) if board[i][j] == 'X' else (0, 0, 255)
                pygame.draw.circle(display, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
                                   cell_size // 2 - 5)


# In your main loop:
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")
    draw_grid(screen, Main.game.board)  # Draw the grid on each frame
    pygame.display.flip()
pygame.quit()
