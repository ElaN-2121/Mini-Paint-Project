from OpenGL.GL import *

def initialize():
    glClearColor(1.0, 1.0, 1.0, 1.0)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    glFlush()