import pygame
import Proyectil

class naveEspacial(pygame.sprite.Sprite):
    # Clase para las naves
    def __init__(self,ancho,alto):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load('image/1nave.jpg')  # Cargar imagen
        self.imagenExplosion = pygame.image.load('image/explosion.jpg')

        self.rect = self.ImagenNave.get_rect()  #hacer un cuadro de la imagen
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30
        self.listaDisparo = []
        self.vida = True
        self.velocidad = 10
        self.sonidoDisparo = pygame.mixer.Sound('sound/shoot.wav')
        self.sonidoExplosion = pygame.mixer.Sound('sound/explosion.wav')

    def movimientoDerecha(self):
        self.rect.right += self.velocidad
        self.__movimiento()

    def movimienoIzquierda(self):
        self.rect.left -= self.velocidad
        self.__movimiento()

    def __movimiento(self): # PRIVADO  # Controlar que no se salga de la pantalla
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right > 900:
                self.rect.right =900

    def disparar(self,x,y):
        miProyectil=Proyectil.Proyectil(x-4,(y-55),'image/disparoa.jpg',True)
        self.listaDisparo.append(miProyectil)
        self.sonidoDisparo.play()

    def destruccion(self):
        self.sonidoExplosion.play()
        self.vida = False
        self.velocidad = 0
        self.ImagenNave = self.imagenExplosion

    def dibujar(self,superficie):
        superficie.blit(self.ImagenNave,self.rect)