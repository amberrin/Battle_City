import pygame
import random
import sys

pygame.init()
#Налаштування
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
    ".ww......e.....wwww.",
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

#Завантаження текстур
def load_image(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

wall_img = load_image("wall.jpg", (TILE_SIZE, TILE_SIZE))
bullet_img = load_image("bullet.png", (10, 10))
background_img = load_image("background.png", (WIDTH, HEIGHT))
enemy_left_img = load_image("enemyl.png", (TILE_SIZE, TILE_SIZE))
enemy_right_img = load_image("enemyr.png", (TILE_SIZE, TILE_SIZE))
enemy_up_img = load_image("enemy.png", (TILE_SIZE, TILE_SIZE))
enemy_down_img = load_image("enemy_d.png", (TILE_SIZE, TILE_SIZE))
player_left_img = load_image("playerl.png", (TILE_SIZE, TILE_SIZE))
player_right_img = load_image("playerr.png", (TILE_SIZE, TILE_SIZE))
player_up_img = load_image("player.png", (TILE_SIZE, TILE_SIZE))
player_down_img = load_image("player_d.png", (TILE_SIZE, TILE_SIZE))
class Button():
    def __init__(self, color, x, y, w, h, text, fsize, txt_color):

        self.width = w
        self.height = h
        self.color = color

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((color))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.fsize = fsize
        self.text = text
        self.txt_color = txt_color
        self.txt_image = pygame.font.Font(None, fsize).render(text, True, txt_color)
    def draw(self, shift_x, shift_y): # цей метод малює кнопку із тектом в середині. Сам текст зміщенний на величини shift_x та shift_y
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.txt_image, (self.rect.x + shift_x, self.rect.y + shift_y))

background=load_image(("tmenu.png"),(800,800))
btn_start = Button((66, 49, 133, 1), 260, 350, 280, 70, 'START GAME',50, (255, 255, 255))
btn_end = Button((66, 49, 133, 1), 260, 445, 280, 70,'CLOSE' ,50, (255,255,255))
btn_menu = Button((255, 29, 109, 10), 260, 350, 280, 70, 'MENU',50, (255, 255, 255))
btn_end1 = Button((0, 180, 0, 0), 260, 445, 280, 70,'CLOSE' ,50, (255,255,255))
btn_restart = Button((255, 29, 109, 10), 260, 445, 280, 70,'RESTART' ,50, (255,255,255))
kill = False
menu = True
game = False
while menu:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            menu=False
            pygame.quit()
            sys.exit()
    screen.blit(background,(0,0))
    btn_start.draw(15,5)
    btn_end.draw(15,5)
    pygame.display.update()
    pygame.time.delay(50)
    pos_x, pos_y = pygame.mouse.get_pos()
    if e.type == pygame.MOUSEBUTTONDOWN:
        if btn_start.rect.collidepoint((pos_x, pos_y)) and e.type == pygame.MOUSEBUTTONDOWN:
            menu = False
            game = True
            kill = False
        if btn_end.rect.collidepoint((pos_x, pos_y)) and e.type == pygame.MOUSEBUTTONDOWN:
            menu = False
            game = False
            kill = False
            win = False
            pygame.quit()
            sys.exit()
#Класи
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
    
    def move(self, dx, dy, obstacles, speed=5):
        new_rect = self.rect.move(dx * speed, dy * speed)


        if new_rect.left < 0 or new_rect.right > WIDTH:
            return
        if new_rect.top < 0 or new_rect.bottom > HEIGHT:
            return


        for obs in obstacles:
            if new_rect.colliderect(obs.rect):
                return

        self.rect = new_rect


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, image=player_right_img, color=(0, 200, 0))
        self.speed = 5
        self.direction = (0, -1)

    def move(self, dx, dy, obstacles):
        super().move(dx, dy, obstacles, self.speed)

        if dx != 0 or dy != 0:
            self.direction = (dx, dy)

        if dx < 0:
            self.image = player_left_img
        elif dx > 0:
            self.image = player_right_img

        if dy < 0:
            self.image = player_up_img
        elif dy > 0:
            self.image = player_down_img

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



class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, image=enemy_up_img, color=(0, 200, 0))
        self.speed = 3
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.change_dir_timer = 0
        self.health = 3

        #Таймер стрельбы
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000

    def update(self, obstacles, player, enemy_bullets):
        self.change_dir_timer += 1

        if self.change_dir_timer > 60:
            self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            self.change_dir_timer = 0

        dx, dy = self.direction
        self.move(dx, dy, obstacles, self.speed)

        if dx < 0:
            self.image = enemy_left_img
        elif dx > 0:
            self.image = enemy_right_img

        if dy < 0:
            self.image = enemy_up_img
        elif dy > 0:
            self.image = enemy_down_img

        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time

            #Направление на игрока
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            if abs(dx) > abs(dy):
                dx = 1 if dx > 0 else -1
                dy = 0
            else:
                dy = 1 if dy > 0 else -1
                dx = 0

            enemy_bullets.append(Bullet(self.rect.centerx, self.rect.centery, (dx, dy)))



#Завантаження рівня
def load_level(level_map):
    obstacles = []
    player = None
    enemies = []

    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if cell == "w":
                obstacles.append(Obstacle(x, y))

            elif cell == "p":
                player = Player(x, y)
            
            elif cell == "e":
                enemies.append(Enemy(x, y))

    return player, obstacles, enemies


player, obstacles, enemies = load_level(level_map)
bullets = []
enemy_bullets = []
player_health = 5
bullet_count = 3
bullet_cool = 0
points = 0
spawn_delay = 15000 
last_spawn_time = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()
if current_time - last_spawn_time > spawn_delay:
    last_spawn_time = current_time
game_over = False
font = pygame.font.Font(None, 36)
text1 = font.render(f"Points: {points}", True, (255, 255, 255))
#Цикл
while True:
    if game_over:
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 80)
        text = font.render("GAME OVER", True, (255, 0, 0))

        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        continue
    if points >=5:
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 80)
        text = font.render("WIN", True, (0, 255, 0))

        screen.blit(text, (WIDTH//2 - 50, HEIGHT//2 - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        continue
    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time > spawn_delay:
        last_spawn_time = current_time

        for _ in range(20):
            x = random.randint(0, COLS - 1) * TILE_SIZE
            y = random.randint(0, ROWS - 1) * TILE_SIZE

            new_enemy = Enemy(x, y)

            collision = False
            for obs in obstacles:
                if new_enemy.rect.colliderect(obs.rect):
                    collision = True
                    break

            if not collision:
                enemies.append(new_enemy)
                break
    clock.tick(FPS)
    #Фон
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((255, 255, 255))

    #Події
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

    #Управління
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

    #Рух пуль
    for bullet in bullets[:]:
        bullet.move()

        #Видалення пуль за межами
        if not screen.get_rect().colliderect(bullet.rect):
            bullets.remove(bullet)
            continue

        #Зіткнення пуль зі стінами
        for obs in obstacles:
            if bullet.rect.colliderect(obs.rect):
                for bullet in bullets[:]:
                    bullets.remove(bullet)
                    break
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                for bullet in bullets[:]:
                    bullets.remove(bullet)
                    enemy.health -= 1
                    break
            if enemy.health <1:
                enemies.remove(enemy)
                points += 1
                text1 = font.render(f"Points: {points}", True, (255, 255, 255))
    for bullet in enemy_bullets[:]:
        bullet.move()

        # удаление за экраном
        if not screen.get_rect().colliderect(bullet.rect):
            enemy_bullets.remove(bullet)
            continue

        # попадание в игрока
        if bullet.rect.colliderect(player.rect):
            enemy_bullets.remove(bullet)
            player_health -= 1

        for obs in obstacles:
            if bullet.rect.colliderect(obs.rect):
                for bullet in enemy_bullets[:]:
                    enemy_bullets.remove(bullet)
                    break
    
    if player_health <= 0:
        game_over = True
    #Малювання
    player.draw()
    for enemy in enemies:
        enemy.update(obstacles, player, enemy_bullets)
    for enemy in enemies:
        enemy.draw()
    for obs in obstacles:
        obs.draw()

    for bullet in bullets:
        bullet.draw()
    for bullet in enemy_bullets:
        bullet.draw()
    screen.blit(text1, (650, 20))

    for i in range(player_health):
        pygame.draw.rect(screen, (255, 0, 0), (60 + i * 35, 15, 40, 15))
    for i in range(bullet_count):
        pygame.draw.rect(screen, (0, 191, 255), (60 + i * 35, 33, 30, 15))
    pygame.display.flip()