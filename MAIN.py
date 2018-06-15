# http://www.classicgaming.cc/classics/space-invaders/sounds
import pygame,sys
from pygame.locals import *
from random import randint
from clases import *
from clases import Invasor as Enemigo      # "as" es para poder utilizar la clase con otro nombre

ancho = 900
alto = 480
listaEnemigo = []

def cargarEnemigos():
    for i in range(300,601,300):
        enemigo = Enemigo(i, 0, 50, 'image/Marciano3A.jpg', 'image/Marciano3B.jpg')
        listaEnemigo.append(enemigo)
    for i in range(70,870,100):
        if (i/100)%2 == 0:
            enemigo =  Enemigo(i,80,50,'image/MarcianoA.jpg','image/MarcianoB.jpg')
            listaEnemigo.append(enemigo)
        else:
            enemigo2 =  Enemigo(i-10,80,50,'image/Marciano2A.jpg','image/Marciano2B.jpg')
            listaEnemigo.append(enemigo2)

def detenerTodo(jugador):
    for enemigo in listaEnemigo:
        enemigo.listaDisparo = []
        enemigo.conquista = True
        jugador.listaDisparo = []

##############################################
class Cursor(pygame.Rect):
    def __init__(self):    #(self,x,y,ancho,alto)
        pygame.Rect.__init__(self,0,0,1,1) #creo un rectangulo
    def update(self):
        self.left,self.top = pygame.mouse.get_pos()    # captura la posicion del cursor

class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x,y):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left,self.rect.top =(x,y)

    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.image_actual = self.imagen_seleccion
        else:
            self.image_actual = self.imagen_normal

        pantalla.blit(self.image_actual,self.rect)


def SpaceInvader():
    pygame.init()
    venta = pygame.display.set_mode((ancho,alto))

    pygame.display.set_caption("Space Invader")
    imagenFondo = pygame.image.load("image/Fondo.jpg")
    bot_Again1 = pygame.image.load("image/TRY_again_1.png")
    bot_Again2 = pygame.image.load("image/TRY_again_2.png")
    bot_Exit1 = pygame.image.load("image/exit_1.png")
    bot_Exit2 = pygame.image.load("image/exit_2.png")

    boton1 = Boton(bot_Again1, bot_Again2, 200, 300)
    boton2 = Boton(bot_Exit1,bot_Exit2,500,300)
    #pygame.mixer.music.load('sound/spaceinvaders1.mpeg')
    #pygame.mixer.music.play()

    destEnemigo = pygame.mixer.Sound('sound/Explosion_enemigo.wav')

    Mifuente = pygame.font.SysFont("Arial",120)
    textoPerdedor =  Mifuente.render("GAME OVER",0,(255,255,51))
    textoGanador = Mifuente.render("YOU WIN ", 0, (255,255,51))
    fuentereloj = pygame.font.SysFont("Arial", 30)

    jugador = naveEspacial(ancho,alto)
    cargarEnemigos()

    reloj = pygame.time.Clock()
    enJuego = True
    contr_disparo = 0
    cursor1 = Cursor()

    while True:
        reloj.tick(60) #  para regular los frames por segundo
        cursor1.update()
        tiempo = pygame.time.get_ticks()/1000   # el tiempo me lo dan en milisegundos

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        if enJuego == True:
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_LEFT:
                    jugador.movimienoIzquierda()
                elif evento.key  == K_RIGHT:
                    jugador.movimientoDerecha()
                elif evento.key ==  K_s:
                    if pygame.time.get_ticks()-contr_disparo >500 and pygame.time.get_ticks()>2000: ## SOLO SE PUEDE DISPARAR CADA MEDIO SEGUNDO
                        x,y = jugador.rect.center                     # recojo las coordenadas de la nave espacial
                        jugador.disparar(x,y)                         # lo mando al objeto jugador, que
                        contr_disparo = pygame.time.get_ticks()         # esta a su vez crea un objeto Proyectil que almacena en una lista



        venta.blit(imagenFondo,(0,0))
        jugador.dibujar(venta)

        if enJuego == False :
            boton1.update(venta,cursor1)
            boton2.update(venta,cursor1)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    return True
                if cursor1.colliderect(boton2.rect):
                    return False


        if len(jugador.listaDisparo)>0:
            for x in jugador.listaDisparo:
                x.Dibujar(venta)  #actualizo
                x.trayectoria()
                if x.rect.top<-1:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            destEnemigo.play()
                            listaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(x)


        if len(listaEnemigo)>0:
            for enemigo in listaEnemigo:
                enemigo.comportamiento(tiempo)
                enemigo.Dibujar(venta)
                if enemigo.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    enJuego = False
                    detenerTodo(jugador)

                if len(enemigo.listaDisparo)>0:
                    for x in enemigo.listaDisparo:
                        x.Dibujar(venta)  #actualizo
                        x.trayectoria()

                        if x.rect.colliderect(jugador.rect):
                            jugador.destruccion()
                            enJuego = False
                            detenerTodo(jugador)

                        if x.rect.top > 900:
                            enemigo.listaDisparo.remove(x)
                        else:
                            for disparo in jugador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(x)

        if enJuego == False and len(listaEnemigo)!=0:
            pygame.mixer.music.fadeout(3000) # en 3 milisegundos se va atenuando la pantalla
            venta.blit(textoPerdedor,(150,100))

        if len(listaEnemigo) != 0 and not(enemigo.conquista):
            contReloj = fuentereloj.render("Tiempo : " + str(tiempo), 0, (255, 255, 255))

        venta.blit(contReloj, (0, 0))

        if len(listaEnemigo) == 0:
            venta.blit(textoGanador,(200,100))
            jugador.velocidad = 0
            jugador.listaDisparo = []
            enJuego = False
        pygame.display.update()

x = SpaceInvader()
while x:
    listaEnemigo = [] # para limpiar los enemigos que quedaron sin matar
    x = SpaceInvader()