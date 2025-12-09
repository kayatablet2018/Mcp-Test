import unittest
from game import SOSGame

class TestSOSGame(unittest.TestCase):

    def test_board_initialization_empty(self):
        game = SOSGame(size=3)
        expected_board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.assertEqual(game.get_board(), expected_board, "Board should be initialized as empty.")
        self.assertEqual(game.size, 3, "Board size should be 3.")

    def test_board_initialization_different_sizes(self):
        game_5x5 = SOSGame(size=5)
        self.assertEqual(game_5x5.size, 5, "Board size should be 5.")
        self.assertEqual(len(game_5x5.get_board()), 5, "Board should have 5 rows.")
        self.assertEqual(len(game_5x5.get_board()[0]), 5, "Board should have 5 columns.")

        game_4x4 = SOSGame(size=4)
        self.assertEqual(game_4x4.size, 4, "Board size should be 4.")
        self.assertEqual(len(game_4x4.get_board()), 4, "Board should have 4 rows.")
        self.assertEqual(len(game_4x4.get_board()[0]), 4, "Board should have 4 columns.")

    def test_make_valid_move(self):
        game = SOSGame(size=3)
        self.assertTrue(game.make_move(0, 0, 'S'), "Valid move should return True.")
        self.assertEqual(game.get_board()[0][0], 'S', "Cell (0,0) should contain 'S'.")

        self.assertTrue(game.make_move(1, 1, 'O'), "Valid move should return True.")
        self.assertEqual(game.get_board()[1][1], 'O', "Cell (1,1) should contain 'O'.")

    def test_make_invalid_move_out_of_bounds(self):
        game = SOSGame(size=3)
        # Test out of bounds for row
        self.assertFalse(game.make_move(-1, 0, 'S'), "Move out of bounds (negative row) should return False.")
        self.assertFalse(game.make_move(3, 0, 'O'), "Move out of bounds (row too large) should return False.")
        # Test out of bounds for column
        self.assertFalse(game.make_move(0, -1, 'S'), "Move out of bounds (negative col) should return False.")
        self.assertFalse(game.make_move(0, 3, 'O'), "Move out of bounds (col too large) should return False.")

        # Ensure board state hasn't changed
        expected_board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.assertEqual(game.get_board(), expected_board, "Board should remain empty after invalid moves.")

    def test_make_invalid_move_cell_occupied(self):
        game = SOSGame(size=3)
        self.assertTrue(game.make_move(0, 0, 'S'), "First move should be valid.")
        self.assertEqual(game.get_board()[0][0], 'S', "Cell (0,0) should contain 'S'.")

        # Try to make another move on the same cell
        self.assertFalse(game.make_move(0, 0, 'O'), "Move on an occupied cell should return False.")
        self.assertEqual(game.get_board()[0][0], 'S', "Cell (0,0) content should not change after invalid move.")

    def test_invalid_player_move(self):
        game = SOSGame(size=3)
        self.assertFalse(game.make_move(0, 0, 'X'), "Invalid player ('X') should return False.")
        expected_board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.assertEqual(game.get_board(), expected_board, "Board should remain empty after invalid player move.")


if __name__ == '__main__':
    unittest.main()