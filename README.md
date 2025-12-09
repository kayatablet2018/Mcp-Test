# SOS Oyunu

Bu, iki oyunculu, konsol tabanlı basit bir SOS (Tic-Tac-Toe benzeri) oyunudur.

## Özellikler

*   İki oyunculu oynanış
*   Kullanıcı dostu oyun tahtası gösterimi
*   Hamle yapma ve kontrol mekanizması
*   Kazananı belirleme
*   Beraberlik durumunu kontrol etme

## Nasıl Oynanır?

1.  Oyunu başlatmak için `main.py` dosyasını çalıştırın:
    ```bash
    python main.py
    ```
2.  Oyun başladığında, 3x3 bir tahta görüntülenecektir.
3.  Oyuncular sırayla `S` veya `O` harflerini seçer ve tahtadaki boş bir hücreye yerleştirmek için satır ve sütun numaralarını girer.
    *   Örnek: `1 1` (birinci satır, birinci sütun) veya `2 3` (ikinci satır, üçüncü sütun).
4.  Oyun, bir oyuncu yatay, dikey veya çapraz olarak art arda üç `SOS` veya `OOO` veya `SSS` dizisi oluşturduğunda veya tahta tamamen dolduğunda sona erer.
5.  Oyun bittiğinde, kazanan ilan edilir veya beraberlik olduğu belirtilir.
