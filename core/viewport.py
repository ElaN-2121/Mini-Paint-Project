from OpenGL.GL import *

def setup_viewport(width, height):
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(
        0,
        width,
        height,
        0,
        -1,
        1
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()