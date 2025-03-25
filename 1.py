import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
clock = pygame.time.Clock()
width = 400
height = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

enemy = pygame.image.load("images/enemy.png")
enemy = pygame.transform.scale(enemy, (60, 80))

player = pygame.image.load("images/player.png")
player = pygame.transform.rotate(player, 180)
player = pygame.transform.scale(player, (60, 80))

coin_img = pygame.image.load("images/coin.png")
coin_img.set_colorkey((255,255,255))
coin_img = pygame.transform.scale(coin_img, (30, 30))

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

background = pygame.image.load("images/road.png")
background = pygame.transform.scale(background, (width, height))

screen = pygame.display.set_mode((400, 600))
screen.fill((255, 255, 255))
pygame.display.set_caption("Racer")

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < width and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), random.randint(100, 500))

    def move(self):
        self.rect.move_ip(0, SPEED // 2)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, width - 40), 0)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

game_start_time = time.time()

while True:
    screen.blit(background, (0, 0))
    scores = font_small.render(f"Score: {SCORE}", True, (0, 0, 0))
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, (255, 215, 0))
    screen.blit(scores, (10, 10))
    screen.blit(coins_text, (width - 100, 10))

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        screen.fill((255, 0, 0))
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        C1.rect.center = (random.randint(40, width - 40), 0)

    pygame.display.update()
    clock.tick(FPS)
