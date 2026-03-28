import pygame
import sys

pygame.init()

# Налаштування
TILE_SIZE = 40
FPS = 60

level_map = [
    "....................",
    "....................",
    "...ww...............",
    "....w.........w.....",
    "....w.........w.....",
    "..............w.....",
    ".....p........w.....",
    "..............w.....",
    "....................",
    "....................",
    "....................",
    "...w................",
    "...wwww.......ww....",
    "...............w....",
    "...............w....",
    "....................",
    "....................",
    "....................",
    "....................",
]

ROWS = len(level_map)
COLS = len(level_map[0])

WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

# Кольори
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)

# Класи

class GameObject:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, GREEN)
        self.speed = 5
        self.direction = (0, -1)

    def move(self, dx, dy, obstacles):
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        for obs in obstacles:
            if new_rect.colliderect(obs.rect):
                return

        self.rect = new_rect
        if dx != 0 or dy != 0:
            self.direction = (dx, dy)

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.centery, self.direction)


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 8
        self.direction = direction

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


class Obstacle(GameObject):
    pass


# Завантаження рівня
def load_level(level_map):
    obstacles = []
    player = None

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if cell == "w":
                obstacles.append(Obstacle(x, y, TILE_SIZE, GRAY))

            elif cell == "p":
                player = Player(x, y)

    return player, obstacles


player, obstacles = load_level(level_map)
bullets = []


# Головний цикл

while True:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.shoot())

    # Управління
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1

    player.move(dx, dy, obstacles)

    # Рух куль
    for bullet in bullets[:]:
        bullet.move()

        if not screen.get_rect().colliderect(bullet.rect):
            bullets.remove(bullet)
            continue

        for obs in obstacles:
            if bullet.rect.colliderect(obs.rect):
                bullets.remove(bullet)
                break

    # Малювання
    player.draw()

    for obs in obstacles:
        obs.draw()

    for bullet in bullets:
        bullet.draw()

    pygame.display.flip()