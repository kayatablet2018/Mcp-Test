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

    def check_for_sos(self, row, col):
        # Check horizontal
        # Case 1: S O S where (row, col) is the first S
        if col + 2 < self.size and \
           self.board[row][col] == 'S' and \
           self.board[row][col+1] == 'O' and \
           self.board[row][col+2] == 'S':
            return True
        # Case 2: S O S where (row, col) is the O
        if col - 1 >= 0 and col + 1 < self.size and \
           self.board[row][col-1] == 'S' and \
           self.board[row][col] == 'O' and \
           self.board[row][col+1] == 'S':
            return True
        # Case 3: S O S where (row, col) is the last S
        if col - 2 >= 0 and \
           self.board[row][col-2] == 'S' and \
           self.board[row][col-1] == 'O' and \
           self.board[row][col] == 'S':
            return True

        # Check vertical
        # Case 1: (row, col) is top S
        if row + 2 < self.size and \
           self.board[row][col] == 'S' and \
           self.board[row+1][col] == 'O' and \
           self.board[row+2][col] == 'S':
            return True
        # Case 2: (row, col) is O
        if row - 1 >= 0 and row + 1 < self.size and \
           self.board[row-1][col] == 'S' and \
           self.board[row][col] == 'O' and \
           self.board[row+1][col] == 'S':
            return True
        # Case 3: (row, col) is bottom S
        if row - 2 >= 0 and \
           self.board[row-2][col] == 'S' and \
           self.board[row-1][col] == 'O' and \
           self.board[row][col] == 'S':
            return True

        # Check main diagonal (top-left to bottom-right)
        # Case 1: (row, col) is top-left S
        if row + 2 < self.size and col + 2 < self.size and \
           self.board[row][col] == 'S' and \
           self.board[row+1][col+1] == 'O' and \
           self.board[row+2][col+2] == 'S':
            return True
        # Case 2: (row, col) is middle O
        if row - 1 >= 0 and col - 1 >= 0 and \
           row + 1 < self.size and col + 1 < self.size and \
           self.board[row-1][col-1] == 'S' and \
           self.board[row][col] == 'O' and \
           self.board[row+1][col+1] == 'S':
            return True
        # Case 3: (row, col) is bottom-right S
        if row - 2 >= 0 and col - 2 >= 0 and \
           self.board[row-2][col-2] == 'S' and \
           self.board[row-1][col-1] == 'O' and \
           self.board[row][col] == 'S':
            return True

        # Check anti-diagonal (top-right to bottom-left)
        # Case 1: (row, col) is top-right S
        if row + 2 < self.size and col - 2 >= 0 and \
           self.board[row][col] == 'S' and \
           self.board[row+1][col-1] == 'O' and \
           self.board[row+2][col-2] == 'S':
            return True
        # Case 2: (row, col) is middle O
        if row - 1 >= 0 and col + 1 < self.size and \
           row + 1 < self.size and col - 1 >= 0 and \
           self.board[row-1][col+1] == 'S' and \
           self.board[row][col] == 'O' and \
           self.board[row+1][col-1] == 'S':
            return True
        # Case 3: (row, col) is bottom-left S
        if row - 2 >= 0 and col + 2 < self.size and \
           self.board[row-2][col+2] == 'S' and \
           self.board[row-1][col+1] == 'O' and \
           self.board[row][col] == 'S':
            return True

        return False


class SOSGame:
    def __init__(self, size):
        self.board = SOSBoard(size)
        self.current_player_char = 'S'  # 'S' for Player 1, 'O' for Player 2
        self.player_map = {'S': 'Player 1 (S)', 'O': 'Player 2 (O)'}
        self.game_over = False  # To be used for game end conditions (SOS, board full)
        self.scores = {'S': 0, 'O': 0}

    def _switch_player(self):
        self.current_player_char = 'O' if self.current_player_char == 'S' else 'S'

    def _get_valid_player_input(self):
        while True:
            try:
                row_str = input("Enter row (0-{}): ".format(self.board.size - 1))
                col_str = input("Enter column (0-{}): ".format(self.board.size - 1))
                char_input = input("Enter 'S' or 'O': ").upper()

                row = int(row_str)
                col = int(col_str)

                if char_input not in ['S', 'O']:
                    print("Invalid character input. Please enter 'S' or 'O'.")
                    continue

                if char_input != self.current_player_char:
                    print(f"You must play '{self.current_player_char}' on your turn.")
                    continue

                return row, col, char_input
            except ValueError:
                print("Invalid input. Please enter numbers for row/column.")
            except Exception as e:
                print(f"An unexpected error occurred during input: {e}")

    def is_board_full(self):
        return all(cell != ' ' for row in self.board.board for cell in row)

    def play_turn(self) -> bool:
        self.board.display_board()
        
        move_successful = False
        while not move_successful:
            print(f"\nIt's {self.player_map[self.current_player_char]}'s turn. Current score: {self.player_map['S']}: {self.scores['S']}, {self.player_map['O']}: {self.scores['O']}")
            
            if self.is_board_full():
                self.game_over = True
                print("Board is full. Game Over.")
                return False

            row, col, char = self._get_valid_player_input()

            success, message = self.board.make_move(row, col, char)

            if success:
                print(message)
                move_successful = True
                
                sos_found = self.board.check_for_sos(row, col)
                if sos_found:
                    self.scores[self.current_player_char] += 1
                    print(f"!!! {self.player_map[self.current_player_char]} made an SOS! Score: {self.scores[self.current_player_char]} They get another turn!")
                else:
                    print("No SOS made. Switching player.")
                    self._switch_player()
            else:
                print(f"Move failed: {message}. Please try again.")
        
        if self.is_board_full():
            self.game_over = True
            print("Board is full. Game Over.")
            return False
            
        return True

    def start_game(self):
        print("\n--- SOS Game Started! ---")
        
        while not self.game_over:
            if not self.play_turn():
                break
        
        print("\n--- Game Over! ---")
        self.board.display_board()
        print(f"Final Scores: {self.player_map['S']}: {self.scores['S']}, {self.player_map['O']}: {self.scores['O']}")

        if self.scores['S'] > self.scores['O']:
            print(f"{self.player_map['S']} wins!")
        elif self.scores['O'] > self.scores['S']:
            print(f"{self.player_map['O']} wins!")
        else:
            print("It's a draw!")


if __name__ == "__main__":
    game = SOSGame(3)
    game.start_game()