import pygame
from constantes import vx, vy

class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()  #(300 (Ancho), 300 (Alto)) #self.rect = (0, 0, 300, 300)
        self.rect.center = (x, y) #(500 (x), 500 (y)) #self.rect = (500, 500, 300, 300) (x, y, ancho, alto)
        self.vx = vx 
        self.vy = vy