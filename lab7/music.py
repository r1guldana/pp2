import pygame

pygame.init()

pygame.display.set_mode((300, 200))

songs = ["music1.mp3", "music2.mp3", "music3.mp3"]
crnt_sng = 0

pygame.mixer.init()
pygame.mixer.music.load(songs[crnt_sng])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE:

                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                crnt_sng = (crnt_sng + 1) % len(songs)
                pygame.mixer.music.load(songs[crnt_sng])
                pygame.mixer.music.play()
            elif event.key == pygame.K_p:
                crnt_sng = (crnt_sng - 1) % len(songs)
                pygame.mixer.music.load(songs[crnt_sng])
                pygame.mixer.music.play()

pygame.quit()