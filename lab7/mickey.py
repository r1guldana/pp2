import pygame
import time

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mickey Clock")

background = pygame.image.load("clock.png").convert()

background = pygame.transform.scale(background, (width, height))

hand1= pygame.image.load("leftarm.png").convert_alpha()
hand2 = pygame.image.load("rightarm.png").convert_alpha()

center = (width // 2, height // 2)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.localtime()
    seconds = now.tm_sec
    minutes = now.tm_min

    seconds_angle = (seconds / 60) * 360 - 90
    minutes_angle = (minutes / 60) * 360 - 90

    seconds_hands = pygame.transform.rotate(hand1, -seconds_angle)
    minutes_hands = pygame.transform.rotate(hand2, -minutes_angle)

    screen.blit(background, (0, 0))
    screen.blit(minutes_hands, minutes_hands.get_rect(center=center))
    screen.blit(seconds_hands, seconds_hands.get_rect(center=center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()