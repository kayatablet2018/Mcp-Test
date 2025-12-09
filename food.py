
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, FOOD_COLOR

class Food:
    """
Yem nesnesini temsil eder. Yemin konumunu yönetir ve ekranda çizilmesini sağlar.
    """
    def __init__(self):
        """
Yem nesnesini başlatır ve rastgele bir konum belirler.
        """
        self.position = (0, 0)
        # Başlangıçta yılanın konumu boş olduğu için boş bir liste ile çağırılır.
        self.randomize_position([])

    def randomize_position(self, snake_body):
        """
Yem için yeni, rastgele bir konum belirler.
Belirlenen konumun yılanın gövdesinin üzerinde olmamasına dikkat eder.

        Args:
            snake_body (list): Yılanın gövde segmentlerinin (x, y) koordinatlarını içeren liste.
        """
        possible_positions = []
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pos = (x, y)
                if pos not in snake_body:
                    possible_positions.append(pos)

        if possible_positions:
            self.position = random.choice(possible_positions)
        else:
            # Oyunda boş alan kalmadığında ne yapılacağı burada yönetilebilir.
            # Şu an için bu durumun oluşmayacağı varsayılıyor.
            pass

    def draw(self, screen):
        """
Yemi belirtilen Pygame ekranına çizer.

        Args:
            screen (pygame.Surface): Yemin çizileceği Pygame ekran nesnesi.
        """
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, rect)
