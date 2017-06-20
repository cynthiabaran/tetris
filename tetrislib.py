from __future__ import division
from __future__ import print_function

import sys
import copy
import time
import random

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

# constantes
blockSize = 0.2
initialX = 0
initialY = 9
proximaX = 8
proximaY = 8
alturaTabuleiro = 20
larguraTabuleiro = 10

class Tetris:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.peca = self.gerarPeca()
        self.proximaPeca = self.gerarPeca(x=proximaX, y=proximaY)
        self.refreshDelay = 1
        self.oldRefreshDelay = 0
        self.nivel = 1
        self.timer = 0
        self.cameraX = 0
        self.cameraY = 0
        self.pontos = 0
        self.oldPontos = 0
        self.gameOver = False

    def render(self):
        gl.glPushMatrix()
        if not self.refreshDelay:
            gl.glRotatef(self.cameraX, 0, self.cameraY, 0)
            self.cameraX += 1
            self.cameraY += 1
            if self.gameOver:
                self.renderizarTexto(-1.0, 0, "GAME OVER", z = 1, color = {'r':1, 'g':0, 'b':0})
            else:
                self.renderizarTexto(-0.6, 0, "PAUSE", z = 1)

            self.renderizarTexto(-0.2, -1.0, str(self.pontos), z = 1)
            self.renderizarTexto(-0.2, -2.0, str(self.nivel), z = 1)
        else:
            holograma = copy.deepcopy(self.peca)
            while self.moveDown(holograma): pass
            self.peca.render()
            holograma.render(True)
            self.proximaPeca.render()
            self.renderizarTexto(-2.5, 1.5, str(self.pontos))
            self.renderizarTexto(-2.5, 0.5, str(self.nivel))
        
        self.tabuleiro.render()
        gl.glPopMatrix()

    def idle(self):
        if self.refreshDelay and time.time() - self.timer > self.refreshDelay:
            self.timer = time.time()
            if not self.moveDown():
                self.novaPeca()
    
    def moveDown(self, peca=False):
        canMove = True
        if peca == False:
            peca = self.peca
        for bloco in peca.blocos:
            canMove = canMove and bloco.checkDown(self.tabuleiro)
        if canMove:
            for bloco in peca.blocos:
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
        pecaAux = copy.deepcopy(self.peca)
        
        pecaAux.rotateClock()
        if self.checarColisao(pecaAux): 
            self.peca.rotateClock()
            return True

        pecaAux.move(x=1)
        if self.checarColisao(pecaAux):
            self.peca.rotateClock()
            self.peca.move(x=1)
            return True
        
        pecaAux.move(x=1)
        if self.checarColisao(pecaAux): 
            self.peca.rotateClock()
            self.peca.move(x=2)
            return True

        pecaAux.move(x=-3)
        if self.checarColisao(pecaAux): 
            self.peca.rotateClock()
            self.peca.move(x=-1)
            return True

        pecaAux.move(x=-1)
        if self.checarColisao(pecaAux): 
            self.peca.rotateClock()
            self.peca.move(x=-2)
            return True

        return False

    
    def rotateAntiClock(self):
        pecaAux = copy.deepcopy(self.peca)
        
        pecaAux.rotateAntiClock()
        if self.checarColisao(pecaAux): 
            self.peca.rotateAntiClock()
            return True

        pecaAux.move(x=1)
        if self.checarColisao(pecaAux):
            self.peca.rotateAntiClock()
            self.peca.move(x=1)
            return True
        
        pecaAux.move(x=1)
        if self.checarColisao(pecaAux): 
            self.peca.rotateAntiClock()
            self.peca.move(x=2)
            return True

        pecaAux.move(x=-3)
        if self.checarColisao(pecaAux): 
            self.peca.rotateAntiClock()
            self.peca.move(x=-1)
            return True

        pecaAux.move(x=-1)
        if self.checarColisao(pecaAux): 
            self.peca.rotateAntiClock()
            self.peca.move(x=-2)
            return True
            
        return False

    def checarColisao(self, peca):
        for blocoPeca in peca.blocos:
            for blocoTab in self.tabuleiro.blocos:
                if blocoPeca.x == blocoTab.x and blocoPeca.y == blocoTab.y:
                    return False
        return True

    def pause(self):
        if self.refreshDelay:
            self.oldRefreshDelay = self.refreshDelay
            self.refreshDelay = 0
        else:
            self.refreshDelay = self.oldRefreshDelay
        if self.gameOver:
            self.__init__()


    def camera(self, x, y):
        self.cameraX = x
        self.cameraY = y

    def moverBlocos(self):
        for bloco in self.peca.blocos:
            self.tabuleiro.blocos.append(bloco)

    def novaPeca(self):
        self.moverBlocos()
        self.checaLinhas()
        self.peca = self.proximaPeca
        self.proximaPeca = self.gerarPeca(x=proximaX, y=proximaY)
        self.peca.move(x = (initialX - proximaX), y = (initialY - proximaY))
        if not self.checarColisao(self.peca):
            self.refreshDelay = 0
            self.gameOver = True

    def checaLinhas(self):
        linhas = {key: [] for key in range(int(-alturaTabuleiro/2 + 1), int(alturaTabuleiro/2))}
        for bloco in self.tabuleiro.blocos:
            if bloco.y in range(int(-alturaTabuleiro/2 + 1), int(alturaTabuleiro/2)):
                if bloco.x in range(int(-larguraTabuleiro/2), int(larguraTabuleiro/2)):
                    linhas[bloco.y].append(bloco)
        moveDown = []
        numeroLinhas = 0
        for key in linhas:
            linha = linhas[key]
            if len(linha) == larguraTabuleiro:
                numeroLinhas += 1
                for bloco in linha:
                    self.tabuleiro.blocos.remove(bloco)
                for bloco in self.tabuleiro.blocos:
                    if bloco.y >= key + 1:
                        moveDown.append(bloco)
        self.pontos += numeroLinhas*numeroLinhas
        for bloco in moveDown:
            bloco.moveDown()
        if self.pontos >= self.oldPontos + 10*self.nivel:
            self.nivel += 1
            self.refreshDelay /= 1.2
            self.oldPontos = self.pontos

    def gerarPeca(self, shape=False, x=False, y=False):

        if shape == False:
            shape = random.choice(['T', 'O', 'I', 'L', 'J', 'S', 'Z'])
        if x == False:
            x = initialX
        if y == False:
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


    def renderizarTexto(self, x, y, text, z = 0, tamanho = 0.002, color = {'r':1, 'g':1, 'b':1}):
        gl.glPushMatrix()
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT,  [color['r'], color['g'], color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [color['r'], color['g'], color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [color['r'], color['g'], color['b'], 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 100.0)
        gl.glTranslatef(x, y, z)
        gl.glScalef(tamanho, tamanho, tamanho)
        for ch in text:
            glut.glutStrokeCharacter( glut.GLUT_STROKE_MONO_ROMAN , glut.ctypes.c_int( ord(ch) ) )
        gl.glPopMatrix()

class Bloco:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def render(self, holograma = False):
        gl.glPushMatrix()
        gl.glTranslatef(self.x * blockSize, self.y * blockSize, 0.0)
        if holograma:
            gl.glColor3f(self.color['r'], self.color['g'], self.color['b'])
            glut.glutWireCube(blockSize)
        else:
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT,  [self.color['r'], self.color['g'], self.color['b'], 1.0])
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  [self.color['r'], self.color['g'], self.color['b'], 1.0])
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [self.color['r'], self.color['g'], self.color['b'], 1.0])
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 100.0)
            glut.glutSolidCube(blockSize)
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

class BlocoFixo(Bloco):
    def moveDown(self):
        pass

    def moveUp(self):
        pass

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

class Tabuleiro:
    def __init__(self):
        gray = {'r':0.5, 'g':0.5, 'b':0.5}
        barreiraInferior = [BlocoFixo(-larguraTabuleiro/2 + i, -alturaTabuleiro/2,     gray) for i in range(larguraTabuleiro)]
        barreiraEsquerda = [BlocoFixo(-larguraTabuleiro/2 - 1, -alturaTabuleiro/2 + i, gray) for i in range(alturaTabuleiro)]
        barreiraDireita  = [BlocoFixo( larguraTabuleiro/2,     -alturaTabuleiro/2 + i, gray) for i in range(alturaTabuleiro)]
        self.blocos = barreiraDireita + barreiraInferior + barreiraEsquerda
    def render(self):
        for bloco in self.blocos:
            bloco.render()
    def podeMover(self, x, y):
        for bloco in self.blocos:
            if bloco.x == x and bloco.y == y:
                return False
        return True

class Peca:
    def render(self, holograma = False):
        for bloco in self.blocos:
            bloco.render(holograma)
    def move(self, x=0, y=0):
        for bloco in self.blocos:
            bloco.x += x
            bloco.y += y


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

