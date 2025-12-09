import sys
from game import Game
from player import Player

def get_valid_input(prompt):
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'exit':
                sys.exit("Oyundan çıkılıyor.")
            return value
        except EOFError:
            sys.exit("Oyundan çıkılıyor.")

def main():
    print("SOS Oyununa Hoş Geldiniz!")
    print("Oyundan çıkmak için herhangi bir zamanda 'exit' yazabilirsiniz.")

    while True:
        try:
            player1_name = get_valid_input("1. Oyuncunun adını girin (S): ")
            player2_name = get_valid_input("2. Oyuncunun adını girin (O): ")
            
            if player1_name == player2_name:
                print("Oyuncu adları aynı olamaz. Lütfen farklı adlar girin.")
                continue

            board_size_str = get_valid_input("Oyun tahtasının boyutunu girin (örn: 3): ")
            board_size = int(board_size_str)
            if board_size < 3:
                print("Tahta boyutu en az 3 olmalıdır.")
                continue

            player1 = Player(player1_name, "S")
            player2 = Player(player2_name, "O")
            game = Game(player1, player2, board_size)

            print(f"\n{player1.name} (S) vs {player2.name} (O) - {board_size}x{board_size} SOS Oyunu Başlıyor!\n")

            while not game.is_game_over():
                game.display_board()
                current_player = game.get_current_player()
                
                print(f"\nSıra {current_player.name} ({current_player.piece}).")
                
                while True:
                    try:
                        row_str = get_valid_input("Satır girin (1'den tahta boyutuna kadar): ")
                        col_str = get_valid_input("Sütun girin (1'den tahta boyutuna kadar): ")
                        
                        row = int(row_str) - 1  # 0-indeksli hale getir
                        col = int(col_str) - 1  # 0-indeksli hale getir
                        
                        if game.make_move(row, col):
                            break # Geçerli hamle yapıldı, döngüden çık
                        else:
                            print("Geçersiz hamle. Lütfen boş bir kareye ve tahta sınırları içine girin.")
                    except ValueError:
                        print("Geçersiz giriş. Lütfen bir sayı girin.")

            game.display_board() # Son tahta durumunu göster

            if game.check_win():
                winner = game.get_winner()
                print(f"\nTebrikler {winner.name}! Oyunu kazandın!\n")
            elif game.check_draw():
                print("\nOyun berabere!\n")
            
            play_again = get_valid_input("Tekrar oynamak ister misiniz? (evet/hayır): ").lower()
            if play_again != 'evet':
                print("Oynadığınız için teşekkürler!")
                break

        except ValueError:
            print("Geçersiz giriş. Tahta boyutu için lütfen bir sayı girin.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            play_again = get_valid_input("Tekrar oynamak ister misiniz? (evet/hayır): ").lower()
            if play_again != 'evet':
                print("Oynadığınız için teşekkürler!")
                break


if __name__ == "__main__":
    main()
