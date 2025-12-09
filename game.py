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
            return False, "Invalid coordinates (row or column out of bounds)."
        if not self.is_cell_empty(row, col):
            return False, "Cell is already occupied."

        self.board[row][col] = player_char
        return True, f"Move successful. {player_char} placed at ({row}, {col})."

    def get_cell(self, row, col):
        if not self.is_valid_coordinate(row, col):
            return None
        return self.board[row][col]

    def display_board(self):
        print("\n  " + " ".join(str(i) for i in range(self.size)))
        print("  " + "--" * self.size)
        for r_idx, row in enumerate(self.board):
            print(f"{r_idx}|{"|".join(row)}|")
        print("  " + "--" * self.size)


class SOSGame:
    def __init__(self, size):
        self.board = SOSBoard(size)
        self.current_player_char = 'S'  # 'S' for Player 1, 'O' for Player 2
        self.player_map = {'S': 'Player 1 (S)', 'O': 'Player 2 (O)'}
        self.game_over = False  # To be used for game end conditions (SOS, board full)

    def _switch_player(self):
        self.current_player_char = 'O' if self.current_player_char == 'S' else 'S'

    def _get_valid_player_input(self):
        while True:
            try:
                print(f"\nIt's {self.player_map[self.current_player_char]}'s turn.")
                row_str = input("Enter row (0-{}): ".format(self.board.size - 1))
                col_str = input("Enter column (0-{}): ".format(self.board.size - 1))
                char_input = input("Enter 'S' or 'O': ").upper()

                row = int(row_str)
                col = int(col_str)

                if char_input not in ['S', 'O']:
                    print("Invalid character input. Please enter 'S' or 'O'.")
                    continue

                # Ensure the player plays their assigned character
                if char_input != self.current_player_char:
                    print(f"You must play '{self.current_player_char}' on your turn.")
                    continue

                return row, col, char_input
            except ValueError:
                print("Invalid input. Please enter numbers for row/column.")
            except Exception as e:
                print(f"An unexpected error occurred during input: {e}")

    def play_turn(self):
        self.board.display_board()
        row, col, char = self._get_valid_player_input()

        success, message = self.board.make_move(row, col, char)

        if success:
            print(message)
            # In a full game, here we would check for SOS and if the board is full
            # For this task, we just switch player after a successful move
            self._switch_player()
        else:
            print(f"Move failed: {message}")
            # If move fails (e.g., cell occupied), the turn remains with the same player.

    def start_game(self):
        print("\n--- SOS Game Started! ---")
        # A simple loop for demonstration.
        # In a complete game, this loop would continue until self.game_over is True
        # which would be set by SOS detection or board full logic.
        max_possible_moves = self.board.size * self.board.size
        moves_made = 0

        while not self.game_over and moves_made < max_possible_moves:
            self.play_turn()
            # A simple check for board full for demonstration
            if all(cell != ' ' for row in self.board.board for cell in row):
                print("\nBoard is full. It's a draw!")
                self.game_over = True
            moves_made += 1

        if not self.game_over:
            print("\nGame ended (for demonstration). Implement full game end conditions (SOS win/draw).")


if __name__ == "__main__":
    game = SOSGame(3)  # Create a 3x3 game
    game.start_game()
