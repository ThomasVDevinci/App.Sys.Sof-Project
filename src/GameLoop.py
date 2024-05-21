import pygame
from src.ConnectFour import ConnectFour
from GUI.GUI import GUI

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

gui = GUI(screen, game, cell_size, offset_y)

game_over = False
win_coordinates = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = gui.handle_menu_event(event)
            if action == "quit":
                running = False
            elif action == "reset" or action == "restart":
                game = ConnectFour(rows, columns)
                pygame.mixer.music.play(-1)
                game_over = False
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
            elif game.is_draw():
                game_over = True
                pygame.mixer.music.stop()

    screen.fill((10, 10, 150))
    gui.display_turn(screen, game.current_player)
    gui.draw_grid(screen, game.board)
    gui.draw_menu(screen)

    if not game_over:
        mouse_x, _ = pygame.mouse.get_pos()
        highlighted_column = mouse_x // cell_size
        gui.draw_highlight(screen, highlighted_column)
    if game_over:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        if win_coordinates is not None:
            winner_text = font.render(f"Player {player_colors[game.current_player]} wins!", True, (241, 196, 15))
            shadow_text = font.render(f"Player {player_colors[game.current_player]} wins!", True, (0, 0, 0))
        else:
            winner_text = font.render("The game is a draw!", True, (241, 196, 15))
            shadow_text = font.render("The game is a draw!", True, (0, 0, 0))
        screen.blit(shadow_text, (350 - winner_text.get_width() // 2 + 5,
                                  300 - winner_text.get_height() // 2 + 5))
        screen.blit(winner_text, (350 - winner_text.get_width() // 2,
                                  300 - winner_text.get_height() // 2))
        button_x = screen.get_width() // 2 - restart_button_width // 2
        button_y = 300 + winner_text.get_height() // 2 + 20
        screen.blit(loop_arrow_image, (button_x, button_y))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_x <= x <= button_x + restart_button_width and button_y <= y <= button_y + restart_button_height:
                    game = ConnectFour(rows, columns)
                    pygame.mixer.music.play(-1)
                    game_over = False
    pygame.display.flip()
