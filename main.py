import pygame
import random
import math


pygame.init()
screen_width, screen_height = 2160, 1215
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("kite")

bg_img = pygame.image.load("midlane.png")
bg_img = pygame.transform.scale(bg_img,(screen_width, screen_height))


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
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
    def __init__(self, start_x, start_y, angle):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.x = start_x + 25 * math.cos(angle)
        self.rect.y = start_y + 25 * math.sin(angle)
        self.speed = 20
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

class enemies(pygame.sprite.Sprite):
    def __init__(self, width, height, player):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill("white")
        self.rect = self.image.get_rect()

        #this is to choose what side the enemies spawn from 
        side = random.choice(["left", "right", "up", "down"])
        if side == "left":
            self.rect.x = -width
            self.rect.y = random.randint(0, screen_height - height)
        elif side == "right":
            self.rect.x = screen_width
            self.rect.y = random.randint(0, screen_height - height)
        elif side == "up":
            self.rect.x = random.randint(0, screen_width - width)
            self.rect.y = -height
        else:
            self.rect.x = random.randint(0, screen_width - width)
            self.rect.y = screen_height
        self.player = player

    def update(self):
        angle = math.atan2(self.player.rect.centery - self.rect.centery, self.player.rect.centerx - self.rect.centerx)
        speed = 5
        self.rect.x += speed * math.cos(angle)
        self.rect.y += speed * math.sin(angle)

        

player = Player(50, 50, 100, 100)
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = pygame.sprite.Group()
enemy = enemies(50, 50, player)
enemy_group.add(enemy)

q_group = pygame.sprite.Group()

running = True
while running:
    screen.blit(bg_img, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and event.type == pygame.KEYDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx)
            q = bullet(player.rect.centerx, player.rect.centery, angle)
            q_group.add(q)
            
    player_group.draw(screen)
    

    enemy_group.draw(screen)
    enemy_group.update()
    
    

    player.move(pygame.key.get_pressed)

    q_group.update()
    q_group.draw(screen)

    
    
    pygame.display.update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

        