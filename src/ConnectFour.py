import copy


class ConnectFour:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.current_player = 'X'

    def drop_piece(self, column):
        if not isinstance(column, int) or column < 0 or column >= self.columns:
            raise ValueError("Invalid column")

        for row in reversed(range(self.rows)):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                return True
        return False

    def is_draw(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def print_board(self):
        print('  ' + ' '.join(map(str, range(1, 8))))
        for i, row in enumerate(reversed(self.board)):
            print(str(6 - i) + ' ' + ' '.join(row))
        print('  ' + ' '.join(map(str, range(1, 8))))

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row][col + 1] == self.board[row][
                    col + 2] == self.board[row][col + 3]:
                    return [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row + 1][col] == \
                        self.board[row + 2][col] == self.board[row + 3][col]:
                    return [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row + 1][col + 1] == \
                        self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    return [(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)]
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if self.board[row][col] != ' ' and self.board[row][col] == self.board[row - 1][col + 1] == \
                        self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
                    return [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)]
        return None  # Return None when there is no win

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
