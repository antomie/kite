import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up display constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Movement")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red color for the player sprite
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.rect.midtop = mouse_pos

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))  # Blue color for the enemy sprite
        self.rect = self.image.get_rect()

        # Spawn the enemy from a random side of the screen
        spawn_side = random.choice(["top", "bottom", "left", "right"])
        if spawn_side == "top":
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height
        elif spawn_side == "bottom":
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = SCREEN_HEIGHT
        elif spawn_side == "left":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        elif spawn_side == "right":
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

        # Set a random angle for movement
        self.angle = math.radians(random.randint(0, 360))

    def update(self):
        # Move the enemy sprite at a specific angle
        speed = 5
        self.rect.x += speed * math.cos(self.angle)
        self.rect.y += speed * math.sin(self.angle)

        # Respawn if the enemy is out of the screen
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0 or \
           self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
            self.__init__()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player sprite and add it to the sprite groups
player = Player()
all_sprites.add(player)

# Create enemy sprites and add them to the sprite groups
for _ in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        print("Player was hit!")
        running = False

    # Draw
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)

    # Refresh screen
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
