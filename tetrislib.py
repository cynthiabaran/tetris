from __future__ import division
from __future__ import print_function

import sys
import time
import random

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

# constantes
blockSize = 0.2
initialX = 0
initialY = 9
alturaTabuleiro = 20
larguraTabuleiro = 10

class Tetris:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.peca = self.gerarPeca()
        self.refreshDelay = 1
        self.oldRefreshDelay = 0
        self.timer = 0
        self.cameraX = 0
        self.cameraY = 0

    def render(self):
        gl.glPushMatrix()
        gl.glRotatef(self.cameraX, 0, self.cameraY, 0)
        self.peca.render()
        self.tabuleiro.render()
        gl.glPopMatrix()

    def idle(self):
        if self.refreshDelay and time.time() - self.timer > self.refreshDelay:
            self.timer = time.time()
            if not self.moveDown():
                self.novaPeca()
    
    def moveDown(self):
        canMove = True
        for bloco in self.peca.blocos:
            canMove = canMove and bloco.checkDown(self.tabuleiro)
        if canMove:
            for bloco in self.peca.blocos:
                bloco.moveDown()
            return True
        return False
    
    def moveUp(self):
        canMove = True
        for bloco in self.peca.blocos:
            canMove = canMove and bloco.checkUp(self.tabuleiro)
        if canMove:
            for bloco in self.blocos:
                bloco.moveUp()
            return True
        return False
    
    def moveLeft(self):
        canMove = True
        for bloco in self.peca.blocos:
            canMove = canMove and bloco.checkLeft(self.tabuleiro)
        if canMove:
            for bloco in self.peca.blocos:
                bloco.moveLeft()
            return True
        return False
    
    def moveRight(self):
        canMove = True
        for bloco in self.peca.blocos:
            canMove = canMove and bloco.checkRight(self.tabuleiro)
        if canMove:
            for bloco in self.peca.blocos:
                bloco.moveRight()
            return True
        return False
    
    def rotateClock(self):
        self.peca.rotateClock()
    
    def rotateAntiClock(self):
        self.peca.rotateAntiClock()

    def pause(self):
        if self.refreshDelay:
            self.oldRefreshDelay = self.refreshDelay
            self.refreshDelay = 0
        else:
            self.refreshDelay = self.oldRefreshDelay

    def camera(self, x, y):
        self.cameraX = x
        self.cameraY = y

    def moverBlocos(self):
        for bloco in self.peca.blocos:
            self.tabuleiro.blocos.append(bloco)

    def novaPeca(self):
        self.moverBlocos()
        self.peca = self.gerarPeca()

    # def checaLinhas(self):
    #     linhas = [[] for i in range(8)]
    #     for bloco in self.blocos:


    def gerarPeca(self):
        shape = random.choice(['T', 'O', 'I', 'L', 'J', 'S', 'Z'])

        x = initialX
        y = initialY

        if shape == 'T':
            color = {'r':1.0, 'g':0.0, 'b':0.0}
            return PecaT(x, y, color)

        elif shape == 'O':
            color = {'r':0.0, 'g':1.0, 'b':0.0}
            return PecaO(x, y, color)

        elif shape == 'I':
            color = {'r':1.0, 'g':1.0, 'b':1.0}
            return PecaI(x, y, color)

        elif shape == 'L':
            color = {'r':1.0, 'g':0.0, 'b':1.0}
            return PecaL(x, y, color)

        elif shape == 'J':
            color = {'r':0.0, 'g':1.0, 'b':1.0}
            return PecaJ(x, y, color)

        elif shape == 'S':
            color = {'r':1.0, 'g':1.0, 'b':0.0}
            return PecaS(x, y, color)

        elif shape == 'Z':
            color = {'r':0.0, 'g':0.0, 'b':1.0}
            return PecaZ(x, y, color)



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
        barreiraInferior = [Bloco(-larguraTabuleiro/2 + i, -alturaTabuleiro/2, gray) for i in range(larguraTabuleiro)]
        barreiraEsquerda = [Bloco(-larguraTabuleiro/2 - 1, -alturaTabuleiro/2 + i, gray) for i in range(alturaTabuleiro)]
        barreiraDireita  = [Bloco(larguraTabuleiro/2, -alturaTabuleiro/2 + i,  gray) for i in range(alturaTabuleiro)]
        self.blocos = barreiraDireita + barreiraInferior + barreiraEsquerda
    def render(self):
        for bloco in self.blocos:
            bloco.render()
    def podeMover(self, x, y):
        for bloco in self.blocos:
            if bloco.x == x and bloco.y == y:
                return False
        return True


