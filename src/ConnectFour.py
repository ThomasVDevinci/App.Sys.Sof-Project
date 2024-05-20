import copy

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]
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
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
                    return [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
                    return [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    return [(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)]
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    return [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)]
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'