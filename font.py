import pygame

_ = pygame.init()
screen = pygame.display.set_mode((1900, 1200))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    title = pygame.font.Font("pacman_font.ttf", 100)
    play = title.render("HIGHSCORES", True, (255, 255, 0))
    # play_hovered = title.render("P", True, (255, 155, 0))
    _ = screen.blit(play, (200, 200))
    # _ = screen.blit(play_hovered, (200, 300))
    pygame.image.save(play, "assets/highscores.png")
    # pygame.image.save(play_hovered, "assets/play_hovered.png")
    pygame.display.flip()
