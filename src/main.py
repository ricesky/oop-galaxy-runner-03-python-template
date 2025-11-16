import pygame
from .core.game import Game


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Galaxy Runner - Stage 3")

    clock = pygame.time.Clock()
    game = Game(screen_width, screen_height)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # detik per frame

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        # Update game state
        game.update(dt)

        # Draw ke layar
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
