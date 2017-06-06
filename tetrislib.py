from __future__ import division
from __future__ import print_function

import sys
import time
import random

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
#oi
# constantes
refreshDelay = 1
blockSize = 0.3

#Diegoaqui

class Bloco:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def render(self):
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, 0.0)
        gl.glColor3f(self.color['r'], self.color['g'], self.color['b'])
        glut.glutWireCube(blockSize)
        gl.glPopMatrix()

    def moveDown(self):
        self.y -= blockSize

    def moveUp(self):
        self.y += blockSize

    def moveLeft(self):
        self.x -= blockSize

    def moveRight(self):
        self.x += blockSize

class Peca:
    def render(self):
        for bloco in self.blocos:
            bloco.render()

    def moveDown(self):
        for bloco in self.blocos:
            bloco.moveDown()

    def moveUp(self):
        for bloco in self.blocos:
            bloco.moveUp()

    def moveLeft(self):
        for bloco in self.blocos:
            bloco.moveLeft()

    def moveRight(self):
        for bloco in self.blocos:
            bloco.moveRight()

class PecaT(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y, color))
        self.blocos.append(Bloco(x + blockSize, y + blockSize, color))
        self.pos = 0

    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveUp()
            self.blocos[0].moveRight()
            self.blocos[2].moveLeft()
            self.blocos[2].moveDown()
            self.blocos[3].moveRight()
            self.blocos[3].moveDown()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveRight()
            self.blocos[0].moveDown()
            self.blocos[2].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[3].moveDown()
            self.blocos[3].moveLeft()
            self.pos = 2
        elif self.pos == 2:
            self.blocos[0].moveDown()
            self.blocos[0].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[2].moveRight()
            self.blocos[3].moveLeft()
            self.blocos[3].moveUp()
            self.pos = 3
        elif self.pos == 3:
            self.blocos[0].moveLeft()
            self.blocos[0].moveUp()
            self.blocos[2].moveRight()
            self.blocos[2].moveDown()
            self.blocos[3].moveUp()
            self.blocos[3].moveRight()
            self.pos = 0


    def rotateAntiClock(self):
        for i in range(3): self.rotateClock()

class PecaI(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y, color))
        self.blocos.append(Bloco(x + 3*blockSize, y, color))
        self.pos = 0
    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveUp()
            self.blocos[0].moveRight()
            self.blocos[2].moveDown()
            self.blocos[2].moveLeft()
            self.blocos[3].moveDown()
            self.blocos[3].moveLeft()
            self.blocos[3].moveDown()
            self.blocos[3].moveLeft()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveDown()
            self.blocos[0].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[2].moveRight()
            self.blocos[3].moveUp()
            self.blocos[3].moveRight()
            self.blocos[3].moveUp()
            self.blocos[3].moveRight()
            self.pos = 0
    def rotateAntiClock(self):
        self.rotateClock()

class PecaO(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + blockSize, y, color))
        self.blocos.append(Bloco(x, y + blockSize, color))
        self.blocos.append(Bloco(x + blockSize, y + blockSize, color))
    def rotateClock(self):
        pass
    def rotateAntiClock(self):
        pass

class PecaL(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y + blockSize, color))


class PecaJ(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y, color))
        self.blocos.append(Bloco(x + 2*blockSize, y - blockSize, color))


class PecaS(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x, y + blockSize, color))
        self.blocos.append(Bloco(x + blockSize, y + blockSize, color))
        self.blocos.append(Bloco(x + blockSize, y + 2*blockSize, color))



class PecaZ(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x, y + blockSize, color))
        self.blocos.append(Bloco(x - blockSize, y + blockSize, color))
        self.blocos.append(Bloco(x - blockSize, y + 2*blockSize, color))


def gerarPeca(shape='R', x=0, y=3, color='default'):
    if shape == 'R':
        shape = random.choice(['T', 'O', 'I', 'L', 'J', 'S', 'Z'])

    if shape == 'T':
        if color == 'default': color = {'r':1.0, 'g':0.0, 'b':0.0}
        return PecaT(x, y, color)

    elif shape == 'O':
        if color == 'default': color = {'r':0.0, 'g':1.0, 'b':0.0}
        return PecaO(x, y, color)

    elif shape == 'I':
        if color == 'default': color = {'r':1.0, 'g':1.0, 'b':1.0}
        return PecaI(x, y, color)

    elif shape == 'L':
        if color == 'default': color = {'r':1.0, 'g':0.0, 'b':1.0}
        return PecaL(x, y, color)

    elif shape == 'J':
        if color == 'default': color = {'r':0.0, 'g':1.0, 'b':1.0}
        return PecaJ(x, y, color)

    elif shape == 'S':
        if color == 'default': color = {'r':1.0, 'g':1.0, 'b':0.0}
        return PecaS(x, y, color)

    elif shape == 'Z':
        if color == 'default': color = {'r':0.0, 'g':0.0, 'b':1.0}
        return PecaZ(x, y, color)
