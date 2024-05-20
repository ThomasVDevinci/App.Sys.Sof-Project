import copy


class ConnectFour:
    def __init__(self, dimension):
        self.board = [[' ' for _ in range(dimension)] for _ in range(dimension)]
        self.current_player = 'X'
        self.state_matrix = []

    def drop_piece(self, column):
        if self.board[0][column] != ' ':
            return False
        for row in reversed(self.board):
            if row[column] == ' ':
                row[column] = self.current_player
                self.state_matrix.append(copy.deepcopy(self.board))
                return True

    def print_board(self):
        print('  ' + ' '.join(map(str, range(1, 8))))
        for i, row in enumerate(reversed(self.board)):
            print(str(6 - i) + ' ' + ' '.join(row))
        print('  ' + ' '.join(map(str, range(1, 8))))

    def check_win(self):
        for row in range(6):
            for i in range(4, 7):
                if self.board[row][i] != ' ' and self.board[row][i] == self.board[row][i - 1] == self.board[row][
                    i - 2] == self.board[row][i - 3]:
                    return [(row, i), (row, i - 1), (row, i - 2), (row, i - 3)]
        for col in range(7):
            for i in range(3, 6):
                if self.board[i][col] != ' ' and self.board[i][col] == self.board[i - 1][col] == self.board[i - 2][
                    col] == self.board[i - 3][col]:
                    return [(i, col), (i - 1, col), (i - 2, col), (i - 3, col)]
        for row in range(3, 6):
            for col in range(4, 7):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col - 1] == \
                        self.board[row - 2][col - 2] == self.board[row - 3][col - 3]:
                    return [(row, col), (row - 1, col - 1), (row - 2, col - 2), (row - 3, col - 3)]
        for row in range(3, 6):
            for col in range(3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col + 1] == \
                        self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    return [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)]
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
