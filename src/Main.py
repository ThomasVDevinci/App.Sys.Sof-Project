from ConnectFour import ConnectFour

game = ConnectFour()

def main():
    global game
    game = ConnectFour()
    while True:
        game.print_board()
        column = int(input(f"Player {game.current_player}, choose a column: ")) - 1
        game.drop_piece(column)
        if game.check_win():
            game.print_board()
            print(f"Player {game.current_player} wins!")
            break
        game.switch_player()

if __name__ == "__main__":
    main()