class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves_made = 0

    def display_board(self):
        print("\n  0 1 2")
        print("  -------")
        for i, row in enumerate(self.board):
            print(f"{i} |{'|'.join(row)}|")
            print("  -------")
        print()

    def is_valid_move(self, row, col):
        if not (0 <= row < 3 and 0 <= col < 3):
            print("Geçersiz satır veya sütun. Lütfen 0-2 arasında değerler girin.")
            return False
        if self.board[row][col] != ' ':
            print("Bu hücre dolu. Lütfen başka bir hücre seçin.")
            return False
        return True

    def make_move(self, row, col, letter):
        if not self.is_valid_move(row, col):
            return False

        if not (letter == 'S' or letter == 'O'):
            print("Geçersiz harf. Lütfen 'S' veya 'O' girin.")
            return False

        self.board[row][col] = letter
        self.moves_made += 1
        return True

    def check_win(self):
        # Satırları kontrol et
        for r in range(3):
            # Her satırda S-O-S desenini kontrol et
            if self.board[r][0] == 'S' and self.board[r][1] == 'O' and self.board[r][2] == 'S':
                return True

        # Sütunları kontrol et
        for c in range(3):
            # Her sütunda S-O-S desenini kontrol et
            if self.board[0][c] == 'S' and self.board[1][c] == 'O' and self.board[2][c] == 'S':
                return True

        # Çaprazları kontrol et (sol üstten sağ alta)
        if self.board[0][0] == 'S' and self.board[1][1] == 'O' and self.board[2][2] == 'S':
            return True

        # Çaprazları kontrol et (sağ üstten sol alta)
        if self.board[0][2] == 'S' and self.board[1][1] == 'O' and self.board[2][0] == 'S':
            return True

        return False

    def check_draw(self):
        return self.moves_made == 9 and not self.check_win()