class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol  # 'S' or 'O'

    def get_move(self):
        while True:
            try:
                row = int(input(f"{self.name} ({self.symbol}), satır gir (0-2): "))
                col = int(input(f"{self.name} ({self.symbol}), sütun gir (0-2): "))
                if 0 <= row < 3 and 0 <= col < 3:
                    return row, col
                else:
                    print("Geçersiz giriş. Lütfen 0 ile 2 arasında sayılar girin.")
            except ValueError:
                print("Geçersiz giriş. Lütfen bir sayı girin.")
