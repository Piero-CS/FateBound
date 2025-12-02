import constantes
import pygame

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos = []
        self.letales = []
        self.arenas = []
        self.puertas = []
        self.llaves = []
        self.pos_jugador1 = None
        self.pos_jugador2 = None

    def procesar_data(self, data, tile_list):
        self.i = len(data)
        for y, fila in enumerate(data):
            for x, tile in enumerate(fila):
                image_x = x * constantes.tile_size
                image_y = y * constantes.tile_size
                if tile >= 0 and tile < len(tile_list):
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_rect.topleft = (image_x, image_y)

                    # Evitar dibujar puertas desde map_tiles, se dibujarán aparte
                    if tile not in constantes.puerta:
                        tile_data = [image, image_rect, image_x, image_y]
                        self.map_tiles.append(tile_data)

                if tile in constantes.obstaculos:
                    self.obstaculos.append(image_rect)
                elif tile in constantes.letales:
                    self.letales.append(image_rect)
                elif tile in constantes.puerta:
                    self.puertas.append(image_rect)
                    self.obstaculos.append(image_rect)
                elif tile in constantes.llave:
                    self.llaves.append(image_rect)
                elif tile == 14:
                    self.pos_jugador1 = (image_x, image_y)
                elif tile == 15:
                    self.pos_jugador2 = (image_x, image_y)

    def dibujar(self, ventana):
        for tile in self.map_tiles:
            ventana.blit(tile[0], tile[1])

        # Dibujar puertas restantes
        puerta_img = pygame.image.load("assets/tiles/tile (12).png")  # Asumiendo que tile (12) es la puerta
        puerta_img = pygame.transform.scale(puerta_img, (constantes.tile_size, constantes.tile_size))
        for puerta in self.puertas:
            ventana.blit(puerta_img, puerta)

        
