
import os
import pygame
import random
from pygame.locals import *
from pygame.locals import QUIT

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

scrn_width = 600
scrn_height = 1000
disp = pygame.display.set_mode((scrn_width, scrn_height))
disp.fill((255, 255, 255))


pygame.display.set_caption("Game")
#red car
class Enemy(pygame.sprite.Sprite):
    def __init__(self, initial_speed=10):
        super().__init__()
        self.image = pygame.image.load("player2.webp".replace("\\",os.sep))
        self.image = pygame.transform.scale(self.image, (80, 160)) 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, scrn_width - 40), 0)
        self.speed = initial_speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 1000:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 600), 0)

    def increase_speed(self, increment): #увеличениe скорости
        self.speed += increment

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.value = random.choice([1, 5]) # Случайный выбор ценности монеты
        if self.value == 1:
             self.image = pygame.image.load("coins.jpg".replace("\\",os.sep))
             self.image = pygame.transform.scale(self.image, (50, 50))

        elif self.value == 5:
             self.image = pygame.image.load("silver_coin.jpg".replace("\\",os.sep))
             self.image = pygame.transform.scale(self.image, (75, 75))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, scrn_width - 90), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > 990:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 700), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#yellow car
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player1.jpg".replace("\\",os.sep))
        self.image = pygame.transform.scale(self.image, (80, 160)) 
        self.rect = self.image.get_rect()
        self.rect.center = (160, 700)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        #move players car with keys
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < scrn_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

player1 = Player()
player2 = Enemy()
coin1 = Coin()
score = 0
font = pygame.font.SysFont("Arial", 30) #font for score
speed_increase_threshold = 20 # Количество монет для увеличения скорости
speed_increment_value = 2 # Величина увеличения скорости

while True: #start game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    #background color
    disp.fill((255, 255, 255))

    
    player1.update()
    player2.move()
    coin1.move()

    if player1.rect.colliderect(coin1.rect):
        score += coin1.value
        coin1.rect.center = (random.randint(40, scrn_width - 40), 0)
        if score % speed_increase_threshold == 0 and score > 0:
            player2.increase_speed(speed_increment_value) # Увеличиваем скорость врага

    player1.draw(disp)
    player2.draw(disp)
    coin1.draw(disp)
    #count score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    disp.blit(score_text, (500, 30))
    if player1.rect.colliderect(player2.rect):
        print("Game Over!") 
        pygame.quit()
        exit() 
    pygame.display.update()

    FramePerSec.tick(FPS)
