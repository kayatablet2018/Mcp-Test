import pygame

# Ekran Boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Yılan rengi
RED = (255, 0, 0)    # Yem rengi
BLUE = (0, 0, 255)   # Oyun sonu metni için kullanılabilecek bir renk

# Yılan Ayarları
SNAKE_SPEED = 10     # Yılanın başlangıç hızı (kare/saniye)
INITIAL_SNAKE_LENGTH = 3 # Yılanın başlangıç uzunluğu

# Yönler
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Oyun durumu
GAME_OVER = 0
PLAYING = 1
