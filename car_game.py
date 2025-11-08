"""
Simple Car Dodge Game (Pygame)

Controls:
- Left arrow / Right arrow to move the car
- Esc or close window to quit

How to run (PowerShell):
python -m pip install pygame
python c:\\Users\\ROUNAK INFOTECH\\Downloads\\Debashish\\car_game.py

This is intentionally small and dependency-free beyond pygame.
"""

import random
import sys

# Helpful import check: give a clear message if pygame is missing instead of a confusing NameError.
try:
    import pygame
except Exception:
    print("Pygame is required to run this game. Install it with: python -m pip install pygame")
    sys.exit(1)

# --- Config ---
WIDTH, HEIGHT = 480, 640
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 80
OBSTACLE_WIDTH_MIN, OBSTACLE_WIDTH_MAX = 40, 120
OBSTACLE_HEIGHT = 30
SPAWN_INTERVAL = 800  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GRAY = (100, 100, 100)


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.move_speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        if keys[pygame.K_LEFT]:
            self.speed_x = -self.move_speed
        if keys[pygame.K_RIGHT]:
            self.speed_x = self.move_speed
        self.rect.x += self.speed_x
        # Keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        w = random.randint(OBSTACLE_WIDTH_MIN, OBSTACLE_WIDTH_MAX)
        self.image = pygame.Surface((w, OBSTACLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - w)
        self.rect.y = -OBSTACLE_HEIGHT
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car Dodge")
    clock = pygame.time.Clock()

    # Groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Spawn timer
    pygame.time.set_timer(pygame.USEREVENT + 1, SPAWN_INTERVAL)

    running = True
    score = 0
    obstacle_base_speed = 3
    spawn_interval = SPAWN_INTERVAL

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                # spawn obstacle, speed slightly increases with score
                speed = obstacle_base_speed + (score // 10)
                obs = Obstacle(speed)
                all_sprites.add(obs)
                obstacles.add(obs)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update
        all_sprites.update()

        # collisions
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            # End game
            running = False

        # Increase score for every frame survived
        score += 1

        # Draw
        screen.fill(GRAY)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score // 10}", 30, WIDTH // 2, 10, WHITE)
        pygame.display.flip()

    # Game over screen
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4, RED)
    draw_text(screen, f"Final Score: {score // 10}", 36, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press any key to exit", 24, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()

    # Wait for key or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                waiting = False

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
