import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
TILE_SIZE = 40
ROWS = 15
COLS = 20
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (26, 35, 126)
BLUE_DARK = (40, 53, 147)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (30, 60, 114)

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Пакмен - Мини Игра")
clock = pygame.time.Clock()

# Лабиринт (1 = стена, 0 = путь, 2 = монета, 3 = враг, 4 = финиш)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,2,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,2,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,2,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,2,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,2,1],
    [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,2,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,4,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Игрок
player = {
    'x': TILE_SIZE,
    'y': TILE_SIZE,
    'size': TILE_SIZE - 4,
    'speed': 3
}

coins = 0
game_over = False
game_won = False

def can_move(x, y):
    """Проверка возможности движения в указанную позицию"""
    col = int(x // TILE_SIZE)
    row = int(y // TILE_SIZE)
    
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False
    
    return maze[row][col] != 1  # Не стена

def check_collisions():
    """Проверка столкновений с монетами, врагами и финишем"""
    global coins, game_over, game_won
    
    col = int((player['x'] + player['size'] / 2) // TILE_SIZE)
    row = int((player['y'] + player['size'] / 2) // TILE_SIZE)
    
    if 0 <= row < ROWS and 0 <= col < COLS:
        # Сбор монет
        if maze[row][col] == 2:
            maze[row][col] = 0
            coins += 1
        
        # Столкновение с врагом
        if maze[row][col] == 3:
            game_over = True
        
        # Достижение финиша
        if maze[row][col] == 4:
            game_won = True
            game_over = True

def move_player(keys):
    """Движение игрока"""
    if game_over:
        return
    
    new_x = player['x']
    new_y = player['y']
    
    if keys[pygame.K_w]:
        new_y -= player['speed']
    if keys[pygame.K_s]:
        new_y += player['speed']
    if keys[pygame.K_a]:
        new_x -= player['speed']
    if keys[pygame.K_d]:
        new_x += player['speed']
    
    # Проверка столкновения со стенами
    if (can_move(new_x, new_y) and 
        can_move(new_x + player['size'], new_y) and 
        can_move(new_x, new_y + player['size']) and 
        can_move(new_x + player['size'], new_y + player['size'])):
        player['x'] = new_x
        player['y'] = new_y
    
    check_collisions()

def draw_maze():
    """Отрисовка лабиринта"""
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            if maze[row][col] == 1:
                # Стена
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLUE_DARK, (x, y, TILE_SIZE, TILE_SIZE), 2)
            elif maze[row][col] == 2:
                # Монета
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.circle(screen, GOLD, (x + TILE_SIZE//2, y + TILE_SIZE//2), 6)
            elif maze[row][col] == 3:
                # Враг
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, RED, (x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10))
                # Глаза врага
                pygame.draw.rect(screen, WHITE, (x + 10, y + 10, 6, 6))
                pygame.draw.rect(screen, WHITE, (x + 24, y + 10, 6, 6))
            elif maze[row][col] == 4:
                # Финиш
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, GREEN, (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                # Текст финиша
                font = pygame.font.Font(None, 30)
                text = font.render("🏁", True, WHITE)
                text_rect = text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
                screen.blit(text, text_rect)
            else:
                # Путь
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))

def draw_player():
    """Отрисовка игрока"""
    center_x = player['x'] + player['size'] // 2
    center_y = player['y'] + player['size'] // 2
    radius = player['size'] // 2
    
    # Тело игрока
    pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
    
    # Глаз игрока
    pygame.draw.circle(screen, BLACK, (center_x - 5, center_y - 5), 3)

def draw_ui():
    """Отрисовка интерфейса"""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Монеты: {coins}", True, WHITE)
    screen.blit(text, (10, 10))
    
    font_small = pygame.font.Font(None, 24)
    text_controls = font_small.render("WASD - движение", True, WHITE)
    screen.blit(text_controls, (10, WINDOW_HEIGHT - 30))

def draw_game_over():
    """Отрисовка экрана окончания игры"""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    font_title = pygame.font.Font(None, 72)
    font_message = pygame.font.Font(None, 48)
    font_button = pygame.font.Font(None, 36)
    
    if game_won:
        title = font_title.render("Поздравляем!", True, GREEN)
        message = font_message.render(f"Вы прошли игру!", True, WHITE)
        coins_text = font_message.render(f"Собрано монет: {coins}", True, GOLD)
    else:
        title = font_title.render("Игра окончена!", True, RED)
        message = font_message.render("Вы попали на врага!", True, WHITE)
        coins_text = font_message.render(f"Собрано монет: {coins}", True, GOLD)
    
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
    message_rect = message.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
    coins_rect = coins_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
    
    screen.blit(title, title_rect)
    screen.blit(message, message_rect)
    screen.blit(coins_text, coins_rect)
    
    restart_text = font_button.render("Нажмите R для перезапуска", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
    screen.blit(restart_text, restart_rect)

def restart_game():
    """Перезапуск игры"""
    global maze, player, coins, game_over, game_won
    
    maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,2,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,2,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
        [1,2,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,2,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,2,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,2,1],
        [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,2,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,4,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    
    player['x'] = TILE_SIZE
    player['y'] = TILE_SIZE
    coins = 0
    game_over = False
    game_won = False

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()
    
    keys = pygame.key.get_pressed()
    move_player(keys)
    
    # Отрисовка
    screen.fill(DARK_BLUE)
    draw_maze()
    draw_player()
    draw_ui()
    
    if game_over:
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

