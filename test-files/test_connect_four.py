import unittest
from GUI.GUI import ConnectFour

class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.game = ConnectFour(6, 7)

    def test_drop_piece(self):
        self.assertTrue(self.game.drop_piece(3))
        self.assertEqual(self.game.board[5][3], 'X')

    def test_check_win(self):
        for i in range(4):
            self.game.drop_piece(i)
        self.assertIsNotNone(self.game.check_win())

if __name__ == '__main__':
    unittest.main()