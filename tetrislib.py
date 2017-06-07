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
blockSize = 0.2
initialX = 0
initialY = 9


class Bloco:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def render(self):
        gl.glPushMatrix()
        gl.glTranslatef(self.x * blockSize, self.y * blockSize, 0.0)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT,  [self.color['r'], self.color['g'], self.color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [self.color['r'], self.color['g'], self.color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [self.color['r'], self.color['g'], self.color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 100.0)
        glut.glutSolidCube(blockSize)
        # gl.glColor3f(self.color['r'], self.color['g'], self.color['b'])
        # glut.glutWireCube(blockSize)
        gl.glPopMatrix()

    def checkDown(self, tabuleiro):
        return tabuleiro.podeMover(self.x, self.y-1)
    
    def checkUp(self, tabuleiro):
        return tabuleiro.podeMover(self.x, self.y+1)
    
    def checkLeft(self, tabuleiro):
        return tabuleiro.podeMover(self.x-1, self.y)
    
    def checkRight(self, tabuleiro):
        return tabuleiro.podeMover(self.x+1, self.y)

    def moveDown(self):
        self.y -= 1

    def moveUp(self):
        self.y += 1

    def moveLeft(self):
        self.x -= 1

    def moveRight(self):
        self.x += 1

class Peca:
    def render(self):
        for bloco in self.blocos:
            bloco.render()

    def moveDown(self, tabuleiro):
        canMove = True
        for bloco in self.blocos:
            canMove = canMove and bloco.checkDown(tabuleiro)
        if canMove:
            for bloco in self.blocos:
                bloco.moveDown()
            return True
        return False
    
    def moveUp(self, tabuleiro):
        canMove = True
        for bloco in self.blocos:
            canMove = canMove and bloco.checkUp(tabuleiro)
        if canMove:
            for bloco in self.blocos:
                bloco.moveUp()
            return True
        return False
    
    def moveLeft(self, tabuleiro):
        canMove = True
        for bloco in self.blocos:
            canMove = canMove and bloco.checkLeft(tabuleiro)
        if canMove:
            for bloco in self.blocos:
                bloco.moveLeft()
            return True
        return False
    
    def moveRight(self, tabuleiro):
        canMove = True
        for bloco in self.blocos:
            canMove = canMove and bloco.checkRight(tabuleiro)
        if canMove:
            for bloco in self.blocos:
                bloco.moveRight()
            return True
        return False

class PecaT(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + 1, y, color))
        self.blocos.append(Bloco(x + 2, y, color))
        self.blocos.append(Bloco(x + 1, y + 1, color))
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
        self.blocos.append(Bloco(x + 1, y, color))
        self.blocos.append(Bloco(x + 2, y, color))
        self.blocos.append(Bloco(x + 3, y, color))
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
        self.blocos.append(Bloco(x + 1, y, color))
        self.blocos.append(Bloco(x, y + 1, color))
        self.blocos.append(Bloco(x + 1, y + 1, color))
    def rotateClock(self):
        pass
    def rotateAntiClock(self):
        pass

class PecaL(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + 1, y, color))
        self.blocos.append(Bloco(x + 2, y, color))
        self.blocos.append(Bloco(x + 2, y + 1, color))
        self.pos = 0


    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveUp()
            self.blocos[0].moveRight()
            self.blocos[2].moveLeft()
            self.blocos[2].moveDown()
            self.blocos[3].moveDown()
            self.blocos[3].moveDown()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveRight()
            self.blocos[0].moveDown()
            self.blocos[2].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[3].moveLeft()
            self.blocos[3].moveLeft()
            self.pos = 2
        elif self.pos == 2:
            self.blocos[0].moveDown()
            self.blocos[0].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[2].moveRight()
            self.blocos[3].moveUp()
            self.blocos[3].moveUp()
            self.pos = 3
        elif self.pos == 3:
            self.blocos[0].moveLeft()
            self.blocos[0].moveUp()
            self.blocos[2].moveRight()
            self.blocos[2].moveDown()
            self.blocos[3].moveRight()
            self.blocos[3].moveRight()
            self.pos = 0

    def rotateAntiClock(self):
        for i in range(3): self.rotateClock()

class PecaJ(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x + 1, y, color))
        self.blocos.append(Bloco(x + 2, y, color))
        self.blocos.append(Bloco(x + 2, y - 1, color))
        self.pos = 0


    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveUp()
            self.blocos[0].moveRight()
            self.blocos[2].moveLeft()
            self.blocos[2].moveDown()
            self.blocos[3].moveLeft()
            self.blocos[3].moveLeft()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveRight()
            self.blocos[0].moveDown()
            self.blocos[2].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[3].moveUp()
            self.blocos[3].moveUp()
            self.pos = 2
        elif self.pos == 2:
            self.blocos[0].moveDown()
            self.blocos[0].moveLeft()
            self.blocos[2].moveUp()
            self.blocos[2].moveRight()
            self.blocos[3].moveRight()
            self.blocos[3].moveRight()
            self.pos = 3
        elif self.pos == 3:
            self.blocos[0].moveLeft()
            self.blocos[0].moveUp()
            self.blocos[2].moveRight()
            self.blocos[2].moveDown()
            self.blocos[3].moveDown()
            self.blocos[3].moveDown()
            self.pos = 0

    def rotateAntiClock(self):
        for i in range(3): self.rotateClock()

class PecaS(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x, y + 1, color))
        self.blocos.append(Bloco(x + 1, y + 1, color))
        self.blocos.append(Bloco(x + 1, y + 2, color))
        self.pos = 0


    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveUp()
            self.blocos[0].moveUp()
            self.blocos[1].moveUp()
            self.blocos[1].moveRight()
            self.blocos[3].moveRight()
            self.blocos[3].moveDown()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveRight()
            self.blocos[0].moveRight()
            self.blocos[1].moveRight()
            self.blocos[1].moveDown()
            self.blocos[3].moveDown()
            self.blocos[3].moveLeft()
            self.pos = 2
        elif self.pos == 2:
            self.blocos[0].moveDown()
            self.blocos[0].moveDown()
            self.blocos[1].moveDown()
            self.blocos[1].moveLeft()
            self.blocos[3].moveLeft()
            self.blocos[3].moveUp()
            self.pos = 3
        elif self.pos == 3:
            self.blocos[0].moveLeft()
            self.blocos[0].moveLeft()
            self.blocos[1].moveLeft()
            self.blocos[1].moveUp()
            self.blocos[3].moveUp()
            self.blocos[3].moveRight()
            self.pos = 0

    def rotateAntiClock(self):
        for i in range(3): self.rotateClock()


class PecaZ(Peca):
    def __init__(self, x, y, color):
        self.blocos = []
        self.blocos.append(Bloco(x, y, color))
        self.blocos.append(Bloco(x, y + 1, color))
        self.blocos.append(Bloco(x - 1, y + 1, color))
        self.blocos.append(Bloco(x - 1, y + 2, color))
        self.pos = 0


    def rotateClock(self):
        if self.pos == 0:
            self.blocos[0].moveLeft()
            self.blocos[0].moveLeft()
            self.blocos[1].moveDown()
            self.blocos[1].moveLeft()
            self.blocos[3].moveDown()
            self.blocos[3].moveRight()
            self.pos = 1
        elif self.pos == 1:
            self.blocos[0].moveUp()
            self.blocos[0].moveUp()
            self.blocos[1].moveLeft()
            self.blocos[1].moveUp()
            self.blocos[3].moveDown()
            self.blocos[3].moveLeft()
            self.pos = 2
        elif self.pos == 2:
            self.blocos[0].moveRight()
            self.blocos[0].moveRight()
            self.blocos[1].moveUp()
            self.blocos[1].moveRight()
            self.blocos[3].moveLeft()
            self.blocos[3].moveUp()
            self.pos = 3
        elif self.pos == 3:
            self.blocos[0].moveDown()
            self.blocos[0].moveDown()
            self.blocos[1].moveRight()
            self.blocos[1].moveDown()
            self.blocos[3].moveUp()
            self.blocos[3].moveRight()
            self.pos = 0

    def rotateAntiClock(self):
        for i in range(3): self.rotateClock()

class Tabuleiro:
    def __init__(self):
        gray = {'r':0.5, 'g':0.5, 'b':0.5}
        barreiraInferior = [Bloco(-5 + i, -10, gray) for i in range(10)]
        barreiraEsquerda = [Bloco(-6, -10 + i, gray) for i in range(20)]
        barreiraDireita  = [Bloco(5, -10 + i,  gray) for i in range(20)]
        self.blocos = barreiraDireita + barreiraInferior + barreiraEsquerda
    def moverBlocos(self, peca):
        for bloco in peca.blocos:
            self.blocos.append(bloco)
    def render(self):
        for bloco in self.blocos:
            bloco.render()
    def podeMover(self, x, y):
        for bloco in self.blocos:
            if bloco.x == x and bloco.y == y:
                return False
        return True


def gerarPeca(shape='R', x='default', y='default', color='default'):
    if shape == 'R':
        shape = random.choice(['T', 'O', 'I', 'L', 'J', 'S', 'Z'])

    if x == 'default':
        x = initialX

    if y == 'default':
        y = initialY

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
