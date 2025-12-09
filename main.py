import pygame
import sys
import random
from snake import Snake
from food import Food
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, INITIAL_SNAKE_LENGTH, SNAKE_COLOR, FOOD_COLOR, BACKGROUND_COLOR, TEXT_COLOR, FPS

pygame.init()

# Ekranı ayarla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Yılan Oyunu")

clock = pygame.time.Clock()

def reset_game():
    global snake, food, score, game_over
    snake = Snake(INITIAL_SNAKE_LENGTH)
    food = Food()
    score = 0
    game_over = False

reset_game()

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

def display_message(message, color, y_displace=0):
    font_style = pygame.font.SysFont(None, 50)
    mes = font_style.render(message, True, color)
    text_rect = mes.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displace))
    screen.blit(mes, text_rect)

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                    snake.change_direction(0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                    snake.change_direction(0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                    snake.change_direction(-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                    snake.change_direction(GRID_SIZE, 0)
            else:
                if event.key == pygame.K_r:
                    reset_game()

    if not game_over:
        snake.move()

        # Yem yendi mi?
        if snake.head[0] == food.position[0] and snake.head[1] == food.position[1]:
            food.randomize_position()
            snake.grow()
            score += 1

        # Duvar çarpması
        if (snake.head[0] < 0 or snake.head[0] >= SCREEN_WIDTH or
                snake.head[1] < 0 or snake.head[1] >= SCREEN_HEIGHT):
            game_over = True

        # Kendine çarpma
        for segment in snake.body[1:]: # Baş hariç diğer segmentleri kontrol et
            if snake.head[0] == segment[0] and snake.head[1] == segment[1]:
                game_over = True
                break

    # Ekranı çiz
    screen.fill(BACKGROUND_COLOR)
    # draw_grid() # İsteğe bağlı ızgara çizimi
    snake.draw(screen)
    food.draw(screen)

    # Skoru göster
    font_style = pygame.font.SysFont(None, 35)
    value = font_style.render("Skor: " + str(score), True, TEXT_COLOR)
    screen.blit(value, [0, 0])

    if game_over:
        display_message("Oyun Bitti!", TEXT_COLOR, -30)
        display_message("Tekrar oynamak için 'R'ye basın", TEXT_COLOR, 30)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
sys.exit()