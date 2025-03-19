import pygame
pygame.init()
screen = pygame.display.set_mode((600,400))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    screen.fill((0,0,0))
pygame.quit()