from __future__ import division
from __future__ import print_function

import sys

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut


from tetrislib import *


def init() :
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glClearDepth(1.0)
    gl.glShadeModel(gl.GL_FLAT)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glEnable(gl.GL_DEPTH_TEST)


def display() :
    global tetris
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # luzes
    gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, [5.0, 10.0, 5.0, 1.0])
    gl.glLight(gl.GL_LIGHT0, gl.GL_DIFFUSE,  [1.0,  1.0, 1.0, 1.0])
    gl.glLight(gl.GL_LIGHT0, gl.GL_SPECULAR, [1.0,  1.0, 1.0, 1.0])

    gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    tetris.render()
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
    global tetris
    tetris.idle()
    glut.glutPostRedisplay()

def mouse(x, y):
    global tetris
    tetris.camera(x, y)
    glut.glutPostRedisplay()

def keyboard(key, x, y) :
    global tetris
    if key in ['w', '\x20'] and tetris.refreshDelay:
        while tetris.moveDown():
            pass
        tetris.novaPeca()
    elif key == 's' and tetris.refreshDelay:
        if not tetris.moveDown():
            tetris.novaPeca()
    elif key == 'a' and tetris.refreshDelay:
        tetris.moveLeft()
    elif key == 'd' and tetris.refreshDelay:
        tetris.moveRight()
    elif key in ['p', '\x0a', '\x0d']:
        tetris.pause()
    elif key == 'e' and tetris.refreshDelay:
        tetris.rotateClock()
    elif key == 'q' and tetris.refreshDelay:
        tetris.rotateAntiClock()
    elif key == "\x1b":
        exit()
    else :
        return
    glut.glutPostRedisplay()

def special(key, x, y):
    global tetris
    if key == glut.GLUT_KEY_UP and tetris.refreshDelay:
        tetris.rotateClock()
    elif key == glut.GLUT_KEY_DOWN and tetris.refreshDelay:
        if not tetris.moveDown():
            tetris.novaPeca()
    elif key == glut.GLUT_KEY_LEFT and tetris.refreshDelay:
        tetris.moveLeft()
    elif key == glut.GLUT_KEY_RIGHT and tetris.refreshDelay:
        tetris.moveRight()

def main() :
    global tetris
    tetris = Tetris()

    _ = glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)

    glut.glutInitWindowSize(600, 600)
    glut.glutInitWindowPosition(0, 100)
    _ = glut.glutCreateWindow('Tetris!!!')

    init()

    _ = glut.glutDisplayFunc(display)
    _ = glut.glutReshapeFunc(reshape)
    _ = glut.glutKeyboardFunc(keyboard)
    _ = glut.glutIdleFunc(idle)
    _ = glut.glutMotionFunc(mouse)
    _ = glut.glutSpecialFunc(special)

    glut.glutMainLoop()


if __name__ == "__main__" :
    main()
