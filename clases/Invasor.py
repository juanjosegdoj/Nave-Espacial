import pygame
from random import randint
from clases import Proyectil

class Invasor(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagenUno,imagenDos):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA = pygame.image.load(imagenUno)
        self.imagenB = pygame.image.load(imagenDos)

        self.listaImagenes=[self.imagenA,self.imagenB]
        self.posImagen = 0
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        self.rect = self.imagenInvasor.get_rect()

        self.listaDisparo = []
        self.velocidad = 1
        self.rect.top = posy
        self.rect.left = posx

        self.rangoDisparo = 5
        self.tiempoCambio = 1

        self.conquista = False

        self.derecha = True
        self.contador = 0
        self.Maxdescenso = self.rect.top + 40

        self.limiteDerecha = posx + distancia
        self.limiteIzquierda = posx - distancia

    def Dibujar (self, superficie):
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        superficie.blit(self.imagenInvasor,self.rect)

    def comportamiento(self,tiempo):    # Puede ser inutil al principio tanto codigo para 2 imagenes
        if self.conquista == False:
            self.__movimientos()
            self.__ataque()
            if self.tiempoCambio == tiempo: # un objeto con mas animaciones solo hay que meterlo a la lista
                self.posImagen +=1
                self.tiempoCambio += 1
                if self.posImagen > len(self.listaImagenes)-1:
                    self.posImagen = 0

    def __movimientos(self):
        if self.contador<3:
            self.__movimientoLateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.Maxdescenso == self.rect.top:
            self.contador = 0
            self.Maxdescenso =self.rect.top + 40
        else:
            self.rect.top += 4   ##esta es la velocidad de descenso

    def __movimientoLateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left> self.limiteDerecha:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteIzquierda:
                self.derecha=  True

    def __ataque(self):
        if randint(0,300)<self.rangoDisparo: # para que se regulen las naves al disparar
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        miProyectil = Proyectil.Proyectil(x,y,'image/disparob.jpg',False)
        self.listaDisparo.append(miProyectil)
