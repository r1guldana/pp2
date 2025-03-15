import pygame
pygame.init()

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
x = 500//2
y = 500//2
radius = 25
speed = 20
run = True
while run:
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 255), (x, y), radius)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x - radius > 0:
            x -= speed
        if keys[pygame.K_RIGHT] and x + radius < 500 :
            x += speed
        if keys[pygame.K_UP] and y - radius > 0:
            y -= speed
        if keys[pygame.K_DOWN] and y + radius < 500:
            y += speed

        pygame.display.flip()
        clock.tick(30)

pygame.quit()