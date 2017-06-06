from __future__ import division
from __future__ import print_function

import sys
import time

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

from tetrislib import *


def init() :
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    # gl.glClearDepth(1.0)
    gl.glShadeModel(gl.GL_FLAT)
    # gl.glShadeModel(gl.GL_SMOOTH)
    # gl.glEnable(gl.GL_LIGHTING)
    # gl.glEnable(gl.GL_LIGHT0)
    # gl.glEnable(gl.GL_DEPTH_TEST)


def display() :
    global peca
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    peca.render()
    glut.glutSwapBuffers()


def reshape(w, h) :
    gl.glViewport (0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity ()
    glu.gluPerspective(60.0, w/h, 1.0, 20.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    glu.gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def idle():
    global timer, peca, speed
    if time.time() - timer > refreshDelay:
        timer = time.time()
        peca.moveDown()
    display()


def keyboard(key, x, y) :
    global peca, refreshDelay
    if key == 'w':
        peca.moveUp()
    elif key == 's':
        peca.moveDown()
    elif key == 'a':
        peca.moveLeft()
    elif key == 'd':
        peca.moveRight()
    elif key == 'f':
        refreshDelay /= 1.1
    elif key == 'r':
        refreshDelay *= 1.1
    elif key == 'e':
        peca.rotateClock()
    elif key == 'q':
        peca.rotateAntiClock()
    else :
        return
    glut.glutPostRedisplay()


def main() :
    global peca, timer
    peca = gerarPeca(shape='I')
    timer = time.time()
    _ = glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)

    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(100, 100)
    _ = glut.glutCreateWindow('Tetris!!!')

    init()

    _ = glut.glutDisplayFunc(display)
    _ = glut.glutReshapeFunc(reshape)
    _ = glut.glutKeyboardFunc(keyboard)
    _ = glut.glutIdleFunc(idle)

    glut.glutMainLoop()


if __name__ == "__main__" :
    main()
