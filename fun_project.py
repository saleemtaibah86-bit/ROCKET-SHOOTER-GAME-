import pygame
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - Professional OOP Edition")
clock = pygame.time.Clock()

BLACK = (15, 15, 25)
WHITE = (255, 255, 255)
CYAN = (0, 240, 255)
RED = (255, 50, 80)
YELLOW = (255, 220, 0)

font = pygame.font.SysFont("arial", 26, bold=True)
big_font = pygame.font.SysFont("arial", 50, bold=True)

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(50)]


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 8
        self.bullets = []
        self.cooldown = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        if self.cooldown == 0:
            new_bullet = Bullet(self.x + self.width // 2 - 2, self.y)
            self.bullets.append(new_bullet)
            self.cooldown = 10

    def update_bullets(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self, surface):
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(surface, CYAN, points)

        for bullet in self.bullets:
            bullet.draw(surface)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(20, WIDTH - 60)
        self.y = random.randint(-150, -40)
        self.width = 35
        self.height = 35
        self.speed = random.randint(3, 6)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width // 2, self.y + self.height)
        ]
        pygame.draw.polygon(surface, RED, points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


player = Player(WIDTH // 2 - 20, HEIGHT - 70)
enemies = [Enemy() for _ in range(6)]
score = 0
game_over = False

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player = Player(WIDTH // 2 - 20, HEIGHT - 70)
                enemies = [Enemy() for _ in range(6)]
                score = 0
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            player.shoot()

        player.update_bullets()

        for enemy in enemies:
            enemy.update()

            enemy_box = enemy.get_rect()
            for bullet in player.bullets[:]:
                if enemy_box.colliderect(bullet.get_rect()):
                    player.bullets.remove(bullet)
                    enemy.reset()
                    score += 10
                    break

            if enemy_box.colliderect(player.get_rect()):
                game_over = True

            if enemy.y > HEIGHT:
                enemy.reset()

    screen.fill(BLACK)

    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, star, 1)

    if not game_over:
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        score_surface = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_surface, (20, 20))
    else:
        msg1 = big_font.render("GAME OVER", True, RED)
        msg2 = font.render(f"Final Score: {score}", True, CYAN)
        msg3 = font.render("Press 'R' to Restart", True, WHITE)

        screen.blit(msg1, (WIDTH // 2 - 130, HEIGHT // 2 - 60))
        screen.blit(msg2, (WIDTH // 2 - 80, HEIGHT // 2))
        screen.blit(msg3, (WIDTH // 2 - 110, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()