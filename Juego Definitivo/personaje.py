import pygame
from entidad import Entidad
from constantes import gravedad, fuerza_salto
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(__file__)
def ruta(*caminos):
    return os.path.join(BASE_DIR, *caminos)

sonido_salto = pygame.mixer.Sound(ruta("audio", "salto.mp3"))

class Personaje(Entidad):
    def __init__(self, x, y, imagen):
        super().__init__(x, y, imagen)
        self.flip = False
        self.suelo = False
        self.gravedad = gravedad
        self.fuerza_salto = fuerza_salto

    def mover(self, direccion, obstaculos, letales):
        desplazamiento_x = 0
        if direccion == "izquierda":
            desplazamiento_x = -self.vx
            self.flip = True
        elif direccion == "derecha":
            desplazamiento_x = self.vx
            self.flip = False
        
        self.rect.x += desplazamiento_x
        for obstaculo in obstaculos:
            if obstaculo.colliderect(self.rect):
                if desplazamiento_x > 0:
                    self.rect.right = obstaculo.left
                elif desplazamiento_x < 0:
                    self.rect.left = obstaculo.right 

    def saltar(self):
        if self.suelo:
            sonido_salto.play()
            self.vy = self.fuerza_salto
            self.suelo = False
    
    def update(self, obstaculos, letales):
        self.vy += self.gravedad
        self.rect.y += self.vy
        self.suelo = False
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                if self.vy > 0:
                    self.rect.bottom = obstaculo.top
                    self.vy = 0
                    self.suelo = True
                elif self.vy < 0:
                    self.rect.top = obstaculo.bottom
                    self.vy = 0

    def dibujar(self, ventana):
        mostrar_imagen = pygame.transform.flip(self.image, self.flip , False)
        ventana.blit(mostrar_imagen, self.rect)
