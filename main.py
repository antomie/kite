import pygame
import random
import math
import os
import sys

pygame.init()  #initialize pygame (ESSENTIAL)
pygame.font.init()
font = pygame.font.Font(None, 48)
screen_width, screen_height = 2160, 1215 #set screen width and height
screen = pygame.display.set_mode((screen_width, screen_height)) #inplement screen width and height
pygame.display.set_caption("kite") #this is bascically the name of the application
score = 0
score_incra = 10

bg_img = pygame.image.load("pngs/midlane.png")   #load bg image
bg_img = pygame.transform.scale(bg_img,(screen_width, screen_height))  #scale image to the screen width and height


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, speed, fire_rate, movement_delay): #constructor
        super().__init__() #__init__ is a subclass of sprite, and you need the sprite functions 
        self.image = pygame.image.load("pngs/playah.png").convert_alpha() #load the player img
        self.rect = self.image.get_rect() #make a box for the player (like a hitbox)
        self.rect.center = [pos_x, pos_y] #center the player
        self.rect.topleft = (pos_x,pos_y)
        self.target_pos = (pos_x, pos_y) #this is for movement, when you right click it will move to the target position
        self.speed = speed #speed of player

        #elements to delay rapid fire q's
        self.fire_rate = fire_rate  
        self.last_shot_time = 0
        self.movement_delay = movement_delay
        self.last_shoot_time = 0
        self.last_movement_time = 0
        self.is_shooting = False

    def update(self):

        current_time = pygame.time.get_ticks()

        # Handle shooting logic
        if self.is_shooting and current_time - self.last_shoot_time >= self.fire_rate:
            self.last_shoot_time = current_time
            self.is_shooting = False

        if current_time - self.last_movement_time >= self.movement_delay:
            dx, dy, = self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y
            distance = abs(dx) + abs(dy)
            if distance > 0:
                move_x = dx / distance * self.speed
                move_y = dy / distance * self.speed
                move_x = min(move_x, abs(dx))
                move_y = min(move_y, abs(dy))
                self.rect.x += move_x
                self.rect.y += move_y

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.fire_rate:
            self.last_shot_time = current_time
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
            q = bullet(self.rect.centerx, self.rect.centery, angle)
            q_group.add(q)

    

class bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, angle):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.x = start_x + 25 * math.cos(angle)
        self.rect.y = start_y + 25 * math.sin(angle)
        self.speed = 30
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


class balls(pygame.sprite.Sprite):
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
        self.angle = math.atan2(self.player.rect.centery - self.rect.centery, self.player.rect.centerx - self.rect.centerx)


    def update(self):
        
        speed = 5
        self.rect.x += speed * math.cos(self.angle)
        self.rect.y += speed * math.sin(self.angle)

        # Respawn if the enemy is out of the screen
        '''if self.rect.left > screen_width or self.rect.right < 0 or \
           self.rect.top > screen_height or self.rect.bottom < 0:'''
        

player = Player(50, 50, screen_width /2, screen_height /2, 10, 1000, 500)
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = pygame.sprite.Group()
enemy = enemies(50, 50, player)
enemy_group.add(enemy)

ball_group = pygame.sprite.Group()

q_group = pygame.sprite.Group()


enemy_spawn_timer = pygame.time.get_ticks()
spawn_delay = 2000
running = True
while running:
    screen.blit(bg_img, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and event.type == pygame.KEYDOWN:
            player.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = pygame.mouse.get_pos()
            player. target_pos = (x - 50// 2,  y - 50 // 2)

    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_timer >= spawn_delay:

        enemy = enemies(50, 50, player)
        enemy_group.add(enemy)
        ball = balls(20, 20, player)
        ball_group.add(ball)
        enemy_spawn_timer = current_time
        spawn_delay -= 20


    coll = pygame.sprite.spritecollide(player, enemy_group, False)
    if coll:
        print("hit")

    bcoll = pygame.sprite.groupcollide(q_group, enemy_group, True, True)
    if bcoll:
        print("hit")
        score += score_incra


    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    player_group.draw(screen)

    enemy_group.draw(screen)
    enemy_group.update()
    

    player.update()

    q_group.update()
    q_group.draw(screen)

    ball_group.draw(screen)
    ball_group.update()
    
    pygame.display.update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

        