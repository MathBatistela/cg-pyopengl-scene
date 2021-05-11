import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *

import numpy

def IdentityMat44(): return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')

def main():
    pygame.init()
    tx = 0
    ty = 0
    tz = 0
    ry = 0

    viewport = (800,600)
    width, height = viewport
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width/float(height)), 0.1, 50.0)

    view_mat = IdentityMat44()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()
    obj = OBJ('chibi.obj', swapyz=True)
    obj.generate()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if   event.key == pygame.K_a:     tx =  0.1
                elif event.key == pygame.K_d:     tx = -0.1
                elif event.key == pygame.K_w:     tz =  0.1
                elif event.key == pygame.K_s:     tz = -0.1
                elif event.key == pygame.K_RIGHT: ry =  1.0
                elif event.key == pygame.K_LEFT:  ry = -1.0
            elif event.type == pygame.KEYUP: 
                if   event.key == pygame.K_a     and tx > 0: tx = 0
                elif event.key == pygame.K_d     and tx < 0: tx = 0
                elif event.key == pygame.K_w     and tz > 0: tz = 0
                elif event.key == pygame.K_s     and tz < 0: tz = 0
                elif event.key == pygame.K_RIGHT and ry > 0: ry = 0.0
                elif event.key == pygame.K_LEFT  and ry < 0: ry = 0.0

        glPushMatrix()
        glLoadIdentity()
        glTranslatef(tx,ty,tz)
        glRotatef(ry, 0, 1, 0)
        glMultMatrixf(view_mat)

        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        obj.render()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)
main()