import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((420, 780))
pygame.display.set_caption("WriterPro")

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((18, 18, 24))

    font = pygame.font.Font(None, 48)

    text = font.render(
        "WriterPro",
        True,
        (245, 245, 245)
    )

    screen.blit(text, (140, 350))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
