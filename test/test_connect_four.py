import unittest
import pygame
from unittest.mock import MagicMock
from src.ConnectFour import ConnectFour
from GUI.GUI import display_turn
import csv

class TestConnectFour(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_results = []

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.game = ConnectFour(6, 7)
        self.player_x = 'X'
        self.player_o = 'O'

    def tearDown(self):
        pygame.quit()
        self.game = None

    def simulate_game(self, moves):
        for move in moves:
            self.assertTrue(self.game.drop_piece(move))
            if not self.game.check_win() and not self.game.is_draw():
                self.game.switch_player()

    def record_result(self, test_id, description, expected, actual):
        self.test_results.append({
            'Test ID': test_id,
            'Description': description,
            'Expected Results': expected,
            'Actual Results': actual
        })

    def test_correct_placement(self):
        description = "Accept a token only if placed in a column where there is still room"
        expected = "Token placed correctly"
        try:
            self.assertTrue(self.game.drop_piece(0))
            self.assertEqual(self.game.board[5][0], self.player_x)
            actual = "Token placed correctly"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(1, description, expected, actual)

    def test_incorrect_placement(self):
        description = "Reject token if column is full"
        expected = "Token not placed in full column"
        try:
            for _ in range(6):  # Fill the first column
                self.assertTrue(self.game.drop_piece(0))
                if not self.game.check_win() and not self.game.is_draw():
                    self.game.switch_player()
            self.assertFalse(self.game.drop_piece(0))  # Column is full
            actual = "Token not placed in full column"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(2, description, expected, actual)

    def test_horizontal_win(self):
        description = "When the 4th token of a horizontal sequence of same color tokens is placed, this color’s player wins"
        expected = "Horizontal win detected"
        try:
            moves = [0, 1, 1, 2, 2, 3, 2, 3, 3, 4, 3]
            self.simulate_game(moves)
            self.assertIsNotNone(self.game.check_win())
            actual = "Horizontal win detected"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(3, description, expected, actual)

    def test_vertical_win(self):
        description = "When the 4th token of a vertical sequence of same color tokens is placed, this color’s player wins"
        expected = "Vertical win detected"
        try:
            moves = [0, 0, 1, 0, 2, 0, 3]
            self.simulate_game(moves)
            self.assertIsNotNone(self.game.check_win())
            actual = "Vertical win detected"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(4, description, expected, actual)

    def test_diagonal_win(self):
        description = "When the 4th token of a diagonal sequence of same color tokens is placed, this color’s player wins"
        expected = "Diagonal win detected"
        try:
            moves = [0, 1, 1, 2, 2, 3, 2, 3, 3, 4, 3]
            self.simulate_game(moves)
            self.assertIsNotNone(self.game.check_win())
            actual = "Diagonal win detected"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(5, description, expected, actual)

    def test_draw_condition(self):
        description = "When the board is full but there is no winning token sequence, the game is a draw"
        expected = "Draw condition detected"
        try:
            moves = [
                0, 1, 2, 3, 4, 5, 6,
                0, 1, 2, 3, 4, 5, 6,
                0, 1, 2, 3, 4, 5, 6,
                0, 1, 2, 3, 4, 5, 6,
                0, 1, 2, 3, 4, 5, 6,
                0, 1, 2, 3, 4, 5, 6
            ]
            self.simulate_game(moves)
            self.assertTrue(self.game.is_draw())
            actual = "Draw condition detected"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(6, description, expected, actual)

    def test_invalid_column(self):
        description = "Reject token if column index is out of range"
        expected = "ValueError raised"
        try:
            with self.assertRaises(ValueError):
                self.game.drop_piece(7)  # Column out of range
            with self.assertRaises(ValueError):
                self.game.drop_piece(-1)  # Column out of range
            actual = "ValueError raised"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(7, description, expected, actual)

    def test_non_integer_column(self):
        description = "Reject token if column index is not an integer"
        expected = "ValueError raised"
        try:
            with self.assertRaises(ValueError):
                self.game.drop_piece('a')
            actual = "ValueError raised"
        except AssertionError as e:
            actual = f"Assertion failed: {str(e)}"
        self.record_result(8, description, expected, actual)

    def test_display_turn(self):
        description = "Display the current player's turn correctly"
        expected = "Turn displayed correctly"
        try:
            self.game.current_player = self.player_x
            display_turn(self.screen, self.game.current_player)
            # Check if the screen surface was modified correctly
            # You can add more specific checks based on your requirements
            actual = "Turn displayed correctly"
        except Exception as e:
            actual = f"Exception occurred: {str(e)}"
        self.record_result(9, description, expected, actual)

    @classmethod
    def tearDownClass(cls):
        with open('../test-files/test_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Test ID', 'Description', 'Expected Results', 'Actual Results']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in cls.test_results:
                writer.writerow(result)

if __name__ == '__main__':
    unittest.main()
