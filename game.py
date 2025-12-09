class SOSBoard:
    def __init__(self, size):
        if not (3 <= size <= 10):
            raise ValueError("Board size must be between 3 and 10.")
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.sos_count = {'Player 1': 0, 'Player 2': 0}
        self.moves_made = 0

    def display(self):
        print("-" * (self.size * 4 + 1))
        for r in range(self.size):
            row_str = "| "
            for c in range(self.size):
                row_str += self.board[r][c] + " | "
            print(row_str)
            print("-" * (self.size * 4 + 1))

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and \
               0 <= col < self.size and \
               self.board[row][col] == ' '

    def make_move(self, row, col, letter):
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = letter
        self.moves_made += 1
        return True

    def check_sos(self, row, col, player):
        letter = self.board[row][col]
        sos_found = 0
        
        line_directions = [
            (0, 1),   # Horizontal (right)
            (1, 0),   # Vertical (down)
            (1, 1),   # Diagonal (down-right)
            (1, -1)   # Diagonal (down-left)
        ]

        for dr, dc in line_directions:
            if letter == 'S':
                # Check for S O S where current 'S' is the first S
                # Sequence: S(row,col) O(row+dr,col+dc) S(row+2dr,col+2dc)
                if (0 <= row + 2 * dr < self.size and 0 <= col + 2 * dc < self.size and
                    self.board[row + dr][col + dc] == 'O' and
                    self.board[row + 2 * dr][col + 2 * dc] == 'S'):
                    sos_found += 1

                # Check for S O S where current 'S' is the last S
                # Sequence: S(row-2dr,col-2dc) O(row-dr,col-dc) S(row,col)
                if (0 <= row - 2 * dr < self.size and 0 <= col - 2 * dc < self.size and
                    self.board[row - dr][col - dc] == 'O' and
                    self.board[row - 2 * dr][col - 2 * dc] == 'S'):
                    sos_found += 1
            
            elif letter == 'O':
                # Check for S O S where current 'O' is the middle O
                # Sequence: S(row-dr,col-dc) O(row,col) S(row+dr,col+dc)
                if (0 <= row - dr < self.size and 0 <= col - dc < self.size and
                    0 <= row + dr < self.size and 0 <= col + dc < self.size and
                    self.board[row - dr][col - dc] == 'S' and
                    self.board[row + dr][col + dc] == 'S'):
                    sos_found += 1
        
        if sos_found > 0:
            self.sos_count[player] += sos_found
            return True
        return False

    def is_full(self):
        return self.moves_made == self.size * self.size

def play_game():
    print("SOS Oyununa Hoş Geldiniz!")

    while True:
        try:
            board_size = int(input("Tahta boyutunu girin (örn. 3x3 için 3): "))
            board = SOSBoard(board_size)
            break
        except ValueError as e:
            print(f"Hata: {e}. Lütfen geçerli bir sayı girin.")

    players = ["Player 1", "Player 2"]
    current_player_index = 0
    game_over = False

    while not game_over:
        current_player = players[current_player_index]
        print(f"\nSıra: {current_player}")
        board.display()
        print(f"Mevcut SOS Sayısı: Player 1: {board.sos_count['Player 1']}, Player 2: {board.sos_count['Player 2']}")

        valid_input = False
        while not valid_input:
            try:
                move_str = input(f"{current_player}, hamlenizi girin (örn. 0 0 S): ").upper().split()
                if len(move_str) != 3:
                    raise ValueError("Geçersiz giriş formatı. Lütfen 'satır sütun harf' şeklinde girin.")
                
                row, col = int(move_str[0]), int(move_str[1])
                letter = move_str[2]

                if letter not in ['S', 'O']:
                    raise ValueError("Geçersiz harf. S veya O girin.")

                if not board.is_valid_move(row, col):
                    print("Geçersiz hamle. Lütfen boş ve geçerli bir hücreye yapın.")
                else:
                    if board.make_move(row, col, letter):
                        valid_input = True
            except ValueError as e:
                print(f"Hata: {e}. Lütfen tekrar deneyin.")
            except IndexError:
                print("Geçersiz giriş formatı. Lütfen 'satır sütun harf' şeklinde girin.")

        if board.check_sos(row, col, current_player):
            print(f"{current_player} bir SOS dizisi oluşturdu! Tekrar oynama hakkı kazandınız.")
        else:
            current_player_index = (current_player_index + 1) % 2

        if board.is_full():
            game_over = True
            board.display()
            print("\nOyun sona erdi! Tahta doldu.")
            if board.sos_count['Player 1'] > board.sos_count['Player 2']:
                print(f"Kazanan: Player 1! ({board.sos_count['Player 1']} SOS)")
            elif board.sos_count['Player 2'] > board.sos_count['Player 1']:
                print(f"Kazanan: Player 2! ({board.sos_count['Player 2']} SOS)")
            else:
                print("Berabere! Her iki oyuncunun da aynı sayıda SOS'u var.")
    
    print("Oyun bitti. Tekrar oynamak için programı yeniden başlatın.")

if __name__ == "__main__":
    play_game()
