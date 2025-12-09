class SOSBoard:
    def __init__(self, size):
        if not isinstance(size, int) or size < 3:
            raise ValueError("Board size must be an integer and at least 3.")
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

    def is_valid_coordinate(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_cell_empty(self, row, col):
        if not self.is_valid_coordinate(row, col):
            return False
        return self.board[row][col] == ' '

    def make_move(self, row, col, player_char):
        if player_char not in ['S', 'O']:
            raise ValueError("Player character must be 'S' or 'O'.")

        if not self.is_valid_coordinate(row, col):
            return False, "Invalid coordinates."
        if not self.is_cell_empty(row, col):
            return False, "Cell is already occupied."

        self.board[row][col] = player_char
        return True, "Move successful."

    def get_cell(self, row, col):
        if not self.is_valid_coordinate(row, col):
            return None # Or raise an error, depending on desired behavior
        return self.board[row][col]

    def display_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        print("  " + "--" * self.size)
        for r_idx, row in enumerate(self.board):
            print(f"{r_idx}|{"|".join(row)}|")
        print("  " + "--" * self.size)


# Örnek kullanım (test amaçlı):
# if __name__ == "__main__":
#     game_board = SOSBoard(3)
#     game_board.display_board()

#     success, message = game_board.make_move(0, 0, 'S')
#     print(message)
#     game_board.display_board()

#     success, message = game_board.make_move(0, 1, 'O')
#     print(message)
#     game_board.display_board()

#     success, message = game_board.make_move(0, 0, 'O') # Geçersiz hamle
#     print(message)
#     game_board.display_board()