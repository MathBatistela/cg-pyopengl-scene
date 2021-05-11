#!/usr/bin/env python
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from objloader import *

rx, ry = (0,0)
tx, ty = (0,0)
tz = 0
rotate = move = False
objects = {}

import numpy

def IdentityMat44(): return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')
view_mat = IdentityMat44()


def init():
    global objects, view_mat
    pygame.init()
    viewport = (800,600)
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    width, height = viewport

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width/float(height)), 0.1, 50.0)

  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()

    
    for _, obj in objects.items():
        obj.generate()

    objects['chair'].loadTexture('chibi.png')

def display():
    global objects, view_mat

    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glLoadIdentity()

    # # RENDER OBJECT
    # glTranslate(tx/20., ty/20., - tz)
    # glRotate(ry, 1, 0, 0)
    # glRotate(rx, 0, 1, 0)
    # objects['chair'].render()

    # glTranslate(tx/20., ty/20., - tz)
    # glRotate(ry, 1, 0, 0)
    # glRotate(rx, 0, 1, 0)
    # objects['monkey'].render()

    glPushMatrix()
    glLoadIdentity()
    glTranslatef(tx,ty,tz)
    glRotatef(ry, 0, 1, 0)
    glRotate(rx, 0, 1, 0)
    glMultMatrixf(view_mat)

    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    objects['monkey'].render()
    glPopMatrix()

def update():
    clock = pygame.time.Clock()
    while 1:
        clock.tick(30)
        inputEvents()
        display()
        pygame.display.flip()

def inputEvents():
    global rotate, rx, ry, tz, tx, ty, move

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
            elif event.key == pygame.K_UP:    rx =  1.0
            elif event.key == pygame.K_DOWN:  rx = -1.0
        elif event.type == pygame.KEYUP: 
            if   event.key == pygame.K_a     and tx > 0: tx = 0
            elif event.key == pygame.K_d     and tx < 0: tx = 0
            elif event.key == pygame.K_w     and tz > 0: tz = 0
            elif event.key == pygame.K_s     and tz < 0: tz = 0
            elif event.key == pygame.K_RIGHT and ry > 0: ry = 0.0
            elif event.key == pygame.K_LEFT  and ry < 0: ry = 0.0
            elif event.key == pygame.K_UP    and rx > 0: rx = 0.0
            elif event.key == pygame.K_DOWN  and rx < 0: rx = 0.0

        # elif event.type == MOUSEBUTTONDOWN:
        #     if event.button == 4: tz = max(1, tz-1)
        #     elif event.button == 5: tz += 1
        #     elif event.button == 1: rotate = True
        #     elif event.button == 3: move = True
        # elif event.type == MOUSEBUTTONUP:
        #     if event.button == 1: rotate = False
        #     elif event.button == 3: move = False
        # elif event.type == MOUSEMOTION:
        #     i, j = event.rel
        #     if rotate:
        #         rx += i
        #         ry += j
        #     if move:
        #         tx += i
        #         ty -= j



    # for e in pygame.event.get():
    #     if e.type == QUIT:
    #         sys.exit()
    #     elif e.type == KEYDOWN and e.key == K_ESCAPE:
    #         sys.exit()
    #     elif e.type == MOUSEBUTTONDOWN:
    #         if e.button == 4: tz = max(1, tz-1)
    #         elif e.button == 5: tz += 1
    #         elif e.button == 1: rotate = True
    #         elif e.button == 3: move = True
    #     elif e.type == MOUSEBUTTONUP:
    #         if e.button == 1: rotate = False
    #         elif e.button == 3: move = False
    #     elif e.type == MOUSEMOTION:
    #         i, j = e.rel
    #         if rotate:
    #             rx += i
    #             ry += j
    #         if move:
    #             tx += i
    #             ty -= j

def main():
    global objects
    objects['chair'] = OBJ('chibi.obj', swapyz=True)
    objects['monkey'] = OBJ('monkey.obj', swapyz=True)
    
    init()
    update()

main()