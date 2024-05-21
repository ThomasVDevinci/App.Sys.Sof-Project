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
            if win_coordinates:
                pygame.display.set_caption(f"Player {game.current_player} wins!")
                game_over = True
                pygame.mixer.music.stop()
                win_sound = pygame.mixer.Sound('../src/win.mp3')
                win_sound.play()

    screen.fill((10, 10, 150))  # Blue background
    display_turn(screen, game.current_player)
    draw_grid(screen, game.board)
    draw_menu(screen)  # Draw the menu

    if not game_over:
        mouse_x, _ = pygame.mouse.get_pos()
        highlighted_column = mouse_x // cell_size
        draw_highlight(screen, highlighted_column)

    if game_over and not line_animation_start:
    # Start the line animation
        line_animation_start = True
        start_point = (win_coordinates[0][1] * cell_size + cell_size // 2, win_coordinates[0][0] * cell_size + cell_size // 2 + offset_y)
        end_point = (win_coordinates[-1][1] * cell_size + cell_size // 2, win_coordinates[-1][0] * cell_size + cell_size // 2 + offset_y)

    if line_animation_start and not line_animation_done:
        # Increment the animation progress
        line_animation_progress += 1
        # Draw the line animation
        current_point = (start_point[0] + (end_point[0] - start_point[0]) * line_animation_progress / 100,
                         start_point[1] + (end_point[1] - start_point[1]) * line_animation_progress / 100)
        pygame.draw.line(screen, (255, 255, 255), start_point, current_point, 5)
        if line_animation_progress >= 100:
            # The animation has reached the end point
            line_animation_done = True
            pygame.time.wait(1000)  # Wait for 2 seconds

    if game_over and line_animation_done:
        # Draw the end game overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))  # Create a new surface
        overlay.fill((0, 0, 0))  # Fill the surface with black
        overlay.set_alpha(150)  # Set the alpha value to make the surface semi-transparent
        screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

        # Draw the end game text
        winner_text = font.render(f"Player {player_colors[game.current_player]} wins!", True, (241, 196, 15))
        screen.blit(font.render(f"Player {player_colors[game.current_player]} wins!", True, (0, 0, 0)),
                    (350 - winner_text.get_width() // 2 + 5, 300 - winner_text.get_height() // 2 + 5))
        screen.blit(winner_text, (350 - winner_text.get_width() // 2, 300 - winner_text.get_height() // 2))

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