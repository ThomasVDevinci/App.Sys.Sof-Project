import pygame
from src.ConnectFour import ConnectFour
player_colors = {'X': 'yellow', 'O': 'red'}
loop_arrow_image = pygame.image.load('../src/restart.png')
restart_button_width = 100  # Width of the button
restart_button_height = 100  # Height of the button
loop_arrow_image = pygame.transform.scale(loop_arrow_image, (restart_button_width, restart_button_height))
pygame.init()
pygame.mixer.music.load('../src/background.mp3')
pygame.mixer.music.play(-1)
rows = 6
columns = 7
cell_size = min(700 // columns, 700 // (rows + 1))
screen = pygame.display.set_mode((cell_size * columns, cell_size * (rows + 1)))
running = True
font = pygame.font.Font(None, 84)
game = ConnectFour(rows, columns)
offset_y = 50

def draw_menu(display):
    # Define the dimensions and position of the menu
    menu_width = 100  # Width of the menu
    menu_height = 25  # Height of the menu
    menu_x = display.get_width() - menu_width - 10  # X position of the menu
    menu_y = display.get_height() - menu_height - 10  # Y position of the menu

    # Define the dimensions of the buttons
    button_width = menu_width // 2 - 10  # Width of the buttons, 10 is the space between the buttons
    button_height = menu_height  # Height of the buttons


    # Draw the buttons
    pygame.draw.rect(display, (100, 100, 100), (menu_x, menu_y, button_width, button_height))
    pygame.draw.rect(display, (100, 100, 100), (menu_x + button_width + 10, menu_y, button_width, button_height))  # 10 is the space between the buttons

    # Draw the text on the buttons
    font = pygame.font.Font(None, 18)
    quit_text = font.render("Quit", True, (0, 0, 0))
    reset_text = font.render("Reset", True, (0, 0, 0))

    display.blit(quit_text, (menu_x + button_width / 2 - quit_text.get_width() / 2, menu_y + button_height / 2 - quit_text.get_height() / 2))
    display.blit(reset_text, (menu_x + button_width + button_width / 2 - reset_text.get_width() / 2 + 10, menu_y + button_height / 2 - reset_text.get_height() / 2))  # 10 is the space between the buttons

def handle_menu_event(event):
    # Define the dimensions and position of the menu
    menu_width = 100  # Width of the menu
    menu_height = 25  # Height of the menu
    menu_x = screen.get_width() - menu_width - 10  # X position of the menu
    menu_y = screen.get_height() - menu_height - 10  # Y position of the menu

    # Define the dimensions of the buttons
    button_width = menu_width // 2 - 10  # Width of the buttons, 10 is the space between the buttons

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height:
            if menu_x <= x <= menu_x + button_width:
                return "quit"
            elif menu_x + button_width + 10 <= x <= menu_x + 2 * button_width + 10:  # 10 is the space between the buttons
                return "reset"
def display_turn(display, player):
    font = pygame.font.Font(None, 36)
    color = "yellow" if player == 'O' else "red"
    text = font.render(f"{color} player's turn", True, (255, 255, 255))
    screen.blit(font.render(f"{color} player's turn", True, (0, 0, 0)), (350 - text.get_width() // 2 + 5, 10 + 5))
    display.blit(text, (350 - text.get_width() // 2, 10))


def draw_grid(display, board):
    for i in range(game.rows):
        for j in range(game.columns):
            pygame.draw.circle(display, (255, 255, 255),
                               (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2 + offset_y),
                               cell_size // 2 - 5)
            if board[i][j] != ' ':
                color = (255, 0, 0) if board[i][j] == 'X' else (255, 255, 0)
                pygame.draw.circle(display, color,
                                   (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2 + offset_y),
                                   cell_size // 2 - 5)


def draw_highlight(display, column):
    pygame.draw.rect(display, (200, 200, 200), (column * cell_size, offset_y, cell_size, cell_size * game.rows), 5)

def draw_line_animation(display, coordinates, progress):
    start_x, start_y = coordinates[0]
    end_x, end_y = coordinates[-1]
    pygame.draw.line(display, (255, 255, 255), (start_x, start_y), (end_x, end_y), int(progress * 10))

game_over = False
win_coordinates = None
animation_progress = 0
line_animation_start = False
line_animation_done = False
line_animation_progress = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = handle_menu_event(event)
            if action == "quit":
                running = False
            elif action == "reset" or action == "restart":
                game = ConnectFour(rows, columns)  # Reset the game
                pygame.mixer.music.play(-1)  # Start the background music again
                game_over = False
                line_animation_start = False
                line_animation_done = False
                line_animation_progress = 0
                continue
            x, y = pygame.mouse.get_pos()
            column = x // cell_size
            if not game_over and game.drop_piece(column):
                game.switch_player()
            win_coordinates = game.check_win()
            if win_coordinates is not None:
                game_over = True
                pygame.mixer.music.stop()
                win_sound = pygame.mixer.Sound('../src/win.mp3')
                win_sound.play()
            elif game.is_draw():  # Check if the game is a draw
                game_over = True
                pygame.mixer.music.stop()

    screen.fill((10, 10, 150))  # Blue background
    display_turn(screen, game.current_player)
    draw_grid(screen, game.board)
    draw_menu(screen)  # Draw the menu
    restart_delay = 2000  # Delay in milliseconds
    restart_allowed = False

    if not game_over:
        mouse_x, _ = pygame.mouse.get_pos()
        highlighted_column = mouse_x // cell_size
        draw_highlight(screen, highlighted_column)
    if game_over:
        # Draw the end game overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))  # Create a new surface
        overlay.fill((0, 0, 0))  # Fill the surface with black
        overlay.set_alpha(150)  # Set the alpha value to make the surface semi-transparent
        screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

        # Draw the end game text
        if win_coordinates is not None:
            winner_text = font.render(f"Player {player_colors[game.current_player]} wins!", True, (241, 196, 15))
            if not line_animation_start:
                line_animation_start = True
                line_animation_start_time = pygame.time.get_ticks()
            elif not line_animation_done:
                line_animation_progress = (pygame.time.get_ticks() - line_animation_start_time) / 1000.0
                if line_animation_progress >= 1.0:
                    line_animation_done = True
                    line_animation_progress = 1.0
            draw_line_animation(screen, win_coordinates, line_animation_progress)
        else:
            winner_text = font.render("The game is a draw!", True, (241, 196, 15))
        screen.blit(winner_text, (350 - winner_text.get_width() // 2, 300 - winner_text.get_height() // 2))  # Draw the text on the screen, not the overlay

        # Draw the "Restart" button under the end game text
        button_x = screen.get_width() // 2 - restart_button_width // 2  # X position of the button
        button_y = 300 + winner_text.get_height() // 2 + 20  # Y position of the button, under the end game text

        # Draw the image on the button
        screen.blit(loop_arrow_image, (button_x, button_y))

        # Handle mouse click events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_x <= x <= button_x + restart_button_width and button_y <= y <= button_y + restart_button_height:
                    # The "Restart" button is clicked
                    game = ConnectFour(rows, columns)  # Restart the game
                    pygame.mixer.music.play(-1)  # Start the background music again
                    game_over = False
                    line_animation_start = False
                    line_animation_done = False
                    line_animation_progress = 0
    pygame.display.flip()