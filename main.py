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
score_incra = 10
score = 0
bg_img = pygame.image.load("pngs/midlane.png")   #load bg image
bg_img = pygame.transform.scale(bg_img,(screen_width, screen_height))  #scale image to the screen width and height


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, fire_rate, movement_delay): #constructor
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
    
    def reset(self, pos_x, pos_y):
        self.rect.center = [pos_x, pos_y]
    

class bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, angle):
        super().__init__()
        self.image = pygame.image.load("pngs/plasma.png").convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = start_x + 25 * math.cos(angle)
        self.rect.y = start_y + 25 * math.sin(angle)
        self.speed = 30
        self.angle = angle
        self.max_distance = 600
        self.distance_travelled = 0

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        self.distance_travelled += abs(self.speed)

        if self.distance_travelled >= self.max_distance:
                self.kill()


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
        
class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = [x, y] 
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

player = Player(screen_width /2, screen_height /2, 10, 1000, 500)
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
q_group = pygame.sprite.Group()

enemy_spawn_timer = pygame.time.get_ticks()
spawn_delay = 2000
running = True
start = 0
running = 1
dead =  2
game_state = start

while running:
    #screen.blit(bg_img, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == start and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = running
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and event.type == pygame.KEYDOWN:
            player.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = pygame.mouse.get_pos()
            player.target_pos = (x - 50// 2,  y - 50 // 2)

    if game_state == start:
        screen.fill("white")

        # Draw start screen text
        text = font.render("Welcome to My Game", True, "black")
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text, text_rect)

        instructions = font.render("Press SPACE to Start", True, "black")
        instructions_rect = instructions.get_rect(center=(screen_width// 2, screen_height // 2 + 50))
        screen.blit(instructions, instructions_rect)
    
    elif game_state == running:

        screen.blit(bg_img, (0,0))
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_q] and event.type == pygame.KEYDOWN:
            player.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = pygame.mouse.get_pos()
            player. target_pos = (x - 50// 2,  y - 50 // 2)

        font = pygame.font.Font(None, 36)
        text = font.render('Score: {}'.format(score), True, "WHITE")
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

        coll1 = pygame.sprite.spritecollide(player, enemy_group, False)
        if coll1:
            print("hit by enemy")
            player_group.remove(player)
            player.kill()
            player_group.empty()
            enemy_group.empty()
            ball_group.empty()
            q_group.empty()
            game_state = dead

        coll2 = pygame.sprite.spritecollide(player, ball_group, False)
        if coll2:
            print("hit by balls")
            player_group.remove(player)
            player.kill()
            player_group.empty()
            enemy_group.empty()
            ball_group.empty()
            q_group.empty()
            game_state = dead

        bcoll = pygame.sprite.groupcollide(q_group, enemy_group, True, True)
        if bcoll:
            print("kill")
            score += score_incra
        
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        player_group.add(player)
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer >= spawn_delay:
            enemy = enemies(50, 50, player)
            enemy_group.add(enemy)
            ball = balls(20, 20, player)
            ball_group.add(ball)
            enemy_spawn_timer = current_time
            spawn_delay -= 20
        
        player_group.draw(screen)
        enemy_group.draw(screen)
        enemy_group.update()
        player.update()
        q_group.update()
        q_group.draw(screen)
        ball_group.draw(screen)
        ball_group.update()

    elif game_state == dead:
        screen.fill("white")
        player_group.empty()
        player.kill()
        score = 0
        # Draw start screen text    
        text = font.render("You dead", True, "black")
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text, text_rect)

        score_text = font.render(f'Score: {score}', True, "black")
        screen.blit(score_text, score_text.get_rect(center = (screen_width //2, screen_height //2)))

        button = Button(screen_width //2, screen_height //2 + 100, 300, 100, "black", 'retry', 'white')
        button.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click is inside the button
            if button.rect.collidepoint(event.pos):
                print('Button Clicked!')
                player = Player(screen_width /2, screen_height /2, 10, 1000, 500)
                game_state = running

    pygame.display.flip()
    pygame.display.update()
    
    pygame.time.Clock().tick(60)

pygame.quit()

        