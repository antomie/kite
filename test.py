import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
WHITE = (255, 255, 255)
MOVEMENT_SPEED = 5
SHOOT_DELAY = 1000  # 1 second delay between shots (in milliseconds)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.target_pos = (x, y)
        self.last_shot_time = 0

    def update(self):
        dx = self.target_pos[0] - self.rect.x
        dy = self.target_pos[1] - self.rect.y
        distance = abs(dx) + abs(dy)
        if distance > 0:
            move_x = dx / distance * MOVEMENT_SPEED
            move_y = dy / distance * MOVEMENT_SPEED
            move_x = min(move_x, abs(dx))
            move_y = min(move_y, abs(dy))
            self.rect.x += move_x
            self.rect.y += move_y

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= SHOOT_DELAY:
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += 5  # Adjust the bullet speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Initialize Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Delayed Shooting Example')

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.target_pos = pygame.mouse.get_pos()
            player.shoot()

    # Update
    all_sprites.update()

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
