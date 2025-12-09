import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_COLOR, SNAKE_HEAD_COLOR

class Snake:
    def __init__(self):
        # Yılanın başlangıç konumu ve parçaları
        initial_x = SCREEN_WIDTH // 2
        initial_y = SCREEN_HEIGHT // 2
        self.body = [(initial_x, initial_y),
                     (initial_x - TILE_SIZE, initial_y),
                     (initial_x - 2 * TILE_SIZE, initial_y)]
        
        # Yılanın başlangıç yönü (sağa)
        self.direction = (TILE_SIZE, 0) # (x_değişimi, y_değişimi)
        self.grow_pending = False # Yılanın büyümesi gerektiğinde True olur

    def move(self):
        # Yeni kafa pozisyonunu hesapla
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Yeni kafayı vücudun başına ekle
        self.body.insert(0, new_head)

        # Büyüme beklemiyorsa, kuyruğu kaldır
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def change_direction(self, new_direction):
        # Anında geri dönmeyi engelle (örneğin sağa giderken sola dönemez)
        current_dir_x, current_dir_y = self.direction
        new_dir_x, new_dir_y = new_direction

        if (current_dir_x * -1 != new_dir_x) or \
           (current_dir_y * -1 != new_dir_y):
            self.direction = new_direction

    def grow(self):
        # Yılanın bir sonraki harekette büyümesini sağlayacak bayrağı ayarla
        self.grow_pending = True

    def get_head_position(self):
        # Yılanın kafa pozisyonunu döndür
        return self.body[0]

    def check_collision_self(self):
        # Yılanın kendi vücuduna çarpıp çarpmadığını kontrol et (kafa hariç)
        head = self.body[0]
        return head in self.body[1:]

    def draw(self, screen):
        # Yılanın kafasını çiz
        head_rect = pygame.Rect(self.body[0][0], self.body[0][1], TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, head_rect)

        # Yılanın kalan vücudunu çiz
        for segment in self.body[1:]:
            segment_rect = pygame.Rect(segment[0], segment[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)
