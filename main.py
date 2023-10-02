import pygame
import random


pygame.init()
screen_width, screen_height = 1280 , 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("kite")
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        #pygame.draw.rect(screen, "white", (player_pos.x, player_pos.y, 10, 10))
        self.image = pygame.Surface([width, height])
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def move(self, keys):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            self.rect.x -= 5

class bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface(5, 5)
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 20






player = Player(50, 50, 100, 100)
player_group = pygame.sprite.Group()
player_group.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")

    


    player.move(pygame.key.get_pressed)
    player_group.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

        