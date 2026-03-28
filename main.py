import pygame
import sys

pygame.init()


TILE_SIZE = 40
FPS = 60

level_map = [
    "........ww..........",
    "........w...........",
    "...ww...w...........",
    "....w...w.....w.....",
    "....w.........w.....",
    "w.............w.....",
    "w....p........w.....",
    "w.............w.....",
    "........ww.........w",
    ".........w.........w",
    ".........ww........w",
    "...w..........ww....",
    "...wwww........w....",
    "......w........w....",
    "......w.............",
    "....................",
    ".ww............wwww.",
    "...............w....",
    "......wwww..........",
]

ROWS = len(level_map)
COLS = len(level_map[0])

WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()


def load_image(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

player_img = load_image("player.png", (TILE_SIZE, TILE_SIZE))
wall_img = load_image("wall.jpg", (TILE_SIZE, TILE_SIZE))
bullet_img = load_image("bullet.png", (10, 10))
background_img = load_image("background.png", (WIDTH, HEIGHT))

class GameObject:
    def __init__(self, x, y, size, image=None, color=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = image
        self.color = color

    def draw(self):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, image=player_img, color=(0, 200, 0))
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
        size = 30
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.speed = 8
        self.direction = direction
        self.image = pygame.transform.scale(bullet_img, (size, size))

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def draw(self):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, (200, 0, 0), self.rect)


class Obstacle(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, image=wall_img, color=(100, 100, 100))




def load_level(level_map):
    obstacles = []
    player = None

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if cell == "w":
                obstacles.append(Obstacle(x, y))

            elif cell == "p":
                player = Player(x, y)

    return player, obstacles


player, obstacles = load_level(level_map)
bullets = []
player_health = 5
bullet_count = 3
bullet_cool = 0

while True:
    clock.tick(FPS)
    
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((255, 255, 255))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_count >= 1:
                    bullet_count -= 1
                    bullets.append(player.shoot())

    if bullet_count < 3:
        bullet_cool += 1
        if bullet_cool >=100:
            bullet_cool = 0 
            bullet_count += 1

    
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

    
    for bullet in bullets[:]:
        bullet.move()

        
        if not screen.get_rect().colliderect(bullet.rect):
            bullets.remove(bullet)
            continue

        
        for obs in obstacles:
            if bullet.rect.colliderect(obs.rect):
                bullets.remove(bullet)
                break

    
    player.draw()

    for obs in obstacles:
        obs.draw()

    for bullet in bullets:
        bullet.draw()

    for i in range(player_health):
        pygame.draw.rect(screen, (255, 0, 0), (60 + i * 35, 15, 40, 15))
    for i in range(bullet_count):
        pygame.draw.rect(screen, (0, 191, 255), (60 + i * 35, 33, 30, 15))
    pygame.display.flip()