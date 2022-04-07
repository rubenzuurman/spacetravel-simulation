# Remove CreateDC warning at the start.
import os
try:
    del os.environ['DISPLAY']
except:
    pass

# Import OpenGL and GLUT.
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def render_square():
    glBegin(GL_QUADS)
    glVertex2f(100, 100) # Coordinates for the bottom left point
    glVertex2f(200, 100) # Coordinates for the bottom right point
    glVertex2f(200, 200) # Coordinates for the top right point
    glVertex2f(100, 200) # Coordinates for the top left point
    glEnd()

def iterate():
    glViewport(0, 0, 500,500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Reset graphics position?
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 3.0)
    # Render square.
    render_square()
    # Swap buffers.
    glutSwapBuffers()

def main():
    # Init glut.
    glutInit()
    
    # Color display mode
    glutInitDisplayMode(GLUT_RGBA)
    
    # Set window size
    glutInitWindowSize(500, 500)
    
    # Set window position
    glutInitWindowPosition(0, 0)
    
    # Create window.
    window = glutCreateWindow("Window Title")
    
    # Tell opengl to call showscreen continuously.
    glutDisplayFunc(show_screen)
    
    # Draw graphics in show_screen function.
    glutIdleFunc(show_screen)
    
    # Start main loop.
    glutMainLoop()

if __name__ == "__main__":
    main()