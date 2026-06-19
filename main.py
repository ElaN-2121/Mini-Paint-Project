import pygame
from pygame.locals import *
from OpenGL.GL import *

from core.renderer import initialize
from core.renderer import render
from core.viewport import setup_viewport
from core.constants import *

def main():
    pygame.init()

    pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        DOUBLEBUF | OPENGL | RESIZABLE
    )

    pygame.display.set_caption(
        WINDOW_TITLE
    )

    setup_viewport(
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )

    initialize()

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:

                setup_viewport(
                    event.w,
                    event.h
                )
            elif event.type == pygame.KEYDOWN:
                print("Key Pressed:", event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse Click:", event.pos)

        render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()