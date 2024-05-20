def main():
    global game
    rows = int(input("Enter the number of rows for the board: "))
    columns = int(input("Enter the number of columns for the board: "))
    game = ConnectFour(rows, columns)
    while True:
        game.print_board()
        column = int(input(f"Player {game.current_player}, choose a column: ")) - 1
        if not game.drop_piece(column):
            print("This column is full. Choose another one.")
            continue
        if game.check_win():
            game.print_board()
            print(f"Player {game.current_player} wins!")
            break
        game.switch_player()

if __name__ == "__main__":
    main()