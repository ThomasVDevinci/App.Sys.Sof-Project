import copy

game = ConnectFour()


class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'
        self.state_matrix = []

    def drop_piece(self, column):
        for row in self.board:
            if row[column] == ' ':
                row[column] = self.current_player
                self.state_matrix.append(copy.deepcopy(self.board))

                return

    def print_board(self):
        print('  ' + ' '.join(map(str, range(1, 8))))
        for i, row in enumerate(reversed(self.board)):
            print(str(6 - i) + ' ' + ' '.join(row))
        print('  ' + ' '.join(map(str, range(1, 8))))

    def check_win(self):
        for row in self.board:
            for i in range(4, 7):
                if row[i] != ' ' and row[i] == row[i - 1] == row[i - 2] == row[i - 3]:
                    return True
        for col in range(7):
            for i in range(3, 6):
                if self.board[i][col] != ' ' and self.board[i][col] == self.board[i - 1][col] == self.board[i - 2][
                    col] == self.board[i - 3][col]:
                    return True
        for row in range(3, 6):
            for col in range(4, 7):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col - 1] == \
                        self.board[row - 2][col - 2] == self.board[row - 3][col - 3]:
                    return True
        for row in range(3, 6):
            for col in range(3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col + 1] == \
                        self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'


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