import pygame
import os
import sys
os.system(f"{sys.executable} -m pip install pygame")
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Apples!")

# Цвета (RGB)
SKY_BLUE = (135, 206, 235)  # Приятный голубой фон
BROWN = (139, 69, 19)       # Корзинка
RED = (220, 20, 60)         # Яблоки
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)       # Трава внизу

clock = pygame.time.Clock()
FPS = 60

# --- Класс Корзинки (Игрок) ---
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создаем прямоугольную корзинку
        self.image = pygame.Surface((100, 30))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# --- Класс Яблока ---
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Рисуем круглое яблоко
        pygame.draw.circle(self.image, RED, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -40)
        self.speed = 4  # Спокойная, невысокая скорость падения

    def update(self):
        self.rect.y += self.speed
        # Если яблоко упало на землю и мы его упустили
        if self.rect.top > HEIGHT:
            self.kill()
            global lives
            lives -= 1  # Теряем одну жизнь

# --- Инициализация групп ---
all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()

basket = Basket()
all_sprites.add(basket)

# Игровые переменные
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 28)
game_over = False

# --- Главный цикл ---
running = True
while running:
    clock.tick(FPS)

    # Проверка закрытия окна или перезапуска
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Нажмите R для перезапуска
                game_over = False
                all_sprites.empty()
                apples.empty()
                basket = Basket()
                all_sprites.add(basket)
                score = 0
                lives = 3

    if not game_over:
        # Редкий спавн яблок, чтобы они не летели сплошным потоком
        if random.random() < 0.02:
            apple = Apple()
            all_sprites.add(apple)
            apples.add(apple)

        # Обновление позиций
        all_sprites.update()

        # Проверяем, поймала ли корзинка яблоко
        # True означает, что пойманное яблоко исчезает
        caught_apples = pygame.sprite.spritecollide(basket, apples, True)
        for apple in caught_apples:
            score += 1  # Плюс одно очко за каждое пойманное яблоко

        # Если жизни кончились, игра останавливается
        if lives <= 0:
            game_over = True

    # --- Отрисовка ---
    screen.fill(SKY_BLUE)  # Рисуем небо
    
    # Рисуем зеленую траву в самом низу
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 20, WIDTH, 20))
    
    # Рисуем корзинку и яблоки
    all_sprites.draw(screen)

    # Отображение интерфейса
    if not game_over:
        score_text = font.render(f"Поймано: {score}", True, WHITE)
        lives_text = font.render(f"Жизни: {lives}", True, RED)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (WIDTH - 140, 20))
    else:
        end_text = font.render("ИГРА ОКОНЧЕНА! Нажмите 'R' для перезапуска", True, WHITE)
        text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(end_text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
