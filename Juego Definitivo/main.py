import pygame
import constantes
import sys
from personaje import Personaje
import csv
import os
from mundo import Mundo
from pygame.mixer import *

pygame.init()

# ================================
# BASE DIR PARA RUTAS SEGURAS
# ================================
BASE_DIR = os.path.dirname(__file__)
def ruta(*caminos):
    return os.path.join(BASE_DIR, *caminos)

# Ventana
ventana = pygame.display.set_mode((constantes.ancho, constantes.alto))
pygame.display.set_caption("Fatebound")

# Fuentes
fuente = pygame.font.Font(ruta("assets", "fuentes", "Minecraft.ttf"), 50)
fuente_inicio = pygame.font.Font(ruta("assets", "fuentes", "Minecraft.ttf"), 80)
fuente_min = pygame.font.Font(ruta("assets", "fuentes", "Minecraft.ttf"), 20)

# Música
pygame.mixer.init()

sonido_muerte = pygame.mixer.Sound(ruta("audio", "muerte.mp3"))
sonido_victoria = pygame.mixer.Sound(ruta("audio", "victoria.mp3"))

# FPS
clock = pygame.time.Clock()

# Cargar imagen jugador
jugador2_i = pygame.image.load(ruta("assets", "personajes", "ninja2.png"))
jugador2_i = pygame.transform.scale(jugador2_i, (jugador2_i.get_width() * constantes.escala, jugador2_i.get_height() * constantes.escala))

jugador1_i = pygame.image.load(ruta("assets", "personajes", "ninja1.png"))
jugador1_i = pygame.transform.scale(jugador1_i, (jugador1_i.get_width() * constantes.escala, jugador1_i.get_height() * constantes.escala))

tile_list = []
for x in range(constantes.n_tiles):
    tile_image = pygame.image.load(ruta("assets", "tiles", f"tile ({x+1}).png"))
    tile_image = pygame.transform.scale(tile_image, (constantes.tile_size, constantes.tile_size))
    tile_list.append(tile_image)

# Mundo
def cargar_nivel(nivel):
    world_data = []
    for i in range(constantes.fila):
        filas = [0] * constantes.columna
        world_data.append(filas)

    ruta_csv = ruta("mapa", f"nivel{nivel}.csv")

    with open(ruta_csv, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                world_data[x][y] = int(columna)

    mundo = Mundo()
    mundo.procesar_data(world_data, tile_list)

    x1, y1 = mundo.pos_jugador1
    x2, y2 = mundo.pos_jugador2

    jugador1 = Personaje(x1, y1, jugador1_i)
    jugador2 = Personaje(x2, y2, jugador2_i)
    jugadores = pygame.sprite.Group(jugador1, jugador2)

    return mundo, jugador1, jugador2, jugadores

nivel = 1
niveles_superados = 0
mundo, jugador1, jugador2, jugadores = cargar_nivel(nivel)

# Ventana Inicio
def inicio():
    ventana.fill((0, 0, 0))
    texto = fuente_inicio.render("Fatebound", True, (255, 255, 255))
    subtexto = fuente.render("Pulse ESPACIO para comenzar", True, (255, 255, 255))
    minitex = fuente_min.render("Goty of the Year, FrayAlcca Studios", True, (255,255,255))

    ventana.blit(texto, (constantes.ancho/2 - texto.get_width()/2, constantes.alto/2 - 200))
    ventana.blit(subtexto, (constantes.ancho/2 - subtexto.get_width()/2, constantes.alto/2))
    ventana.blit(minitex, (constantes.ancho/2 - minitex.get_width()/2, constantes.alto/2 + 300))
    pygame.display.flip()

ventana_inicio = True
llave_tocada = False

while True:
    if ventana_inicio:
        inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ventana_inicio = False
                tiempo_inicio_total = pygame.time.get_ticks()   
                tiempo_inicio = tiempo_inicio_total       
                pygame.mixer_music.load(ruta("audio", "cancion_juego.mp3"))
                pygame.mixer_music.set_volume(0.4)
                pygame.mixer_music.play(-1)


    else:
        ventana.fill(constantes.fondo)
        mundo.dibujar(ventana)
        teclas = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

        # Jugador 1
        if teclas[pygame.K_a]:
            jugador1.mover("izquierda", mundo.obstaculos, mundo.letales)
        elif teclas[pygame.K_d]:
            jugador1.mover("derecha", mundo.obstaculos, mundo.letales)
        if teclas[pygame.K_w]:
            jugador1.saltar()

        # Jugador 2
        if teclas[pygame.K_LEFT]:
            jugador2.mover("izquierda", mundo.obstaculos, mundo.letales)
        elif teclas[pygame.K_RIGHT]:
            jugador2.mover("derecha", mundo.obstaculos, mundo.letales)
        if teclas[pygame.K_UP]:
            jugador2.saltar()

        jugador1.update(mundo.obstaculos, mundo.letales)
        jugador2.update(mundo.obstaculos, mundo.letales)

        for jugador in jugadores:
            jugador.dibujar(ventana)

        if jugador1.rect.colliderect(jugador2.rect):
            sonido_victoria.play()
            niveles_superados += 1
            nivel += 1
            if niveles_superados >= constantes.nivel_max:
                ventana.fill((0, 0, 0))

                # Texto principal
                texto = fuente_inicio.render("¡Ganaste!", True, (255, 255, 0))
                ventana.blit(texto, (constantes.ancho / 2 - texto.get_width() / 2, constantes.alto / 2 - 100))

                # Calcular tiempo total de la partida
                tiempo_final = pygame.time.get_ticks()
                tiempo_total = (tiempo_final - tiempo_inicio_total) / 1000  # segundos

                texto_tiempo_total = fuente.render(f"Tiempo total: {tiempo_total:.3f} s", True, (255, 255, 255))
                ventana.blit(texto_tiempo_total, (constantes.ancho / 2 - texto_tiempo_total.get_width() / 2, constantes.alto / 2 + 50))

                pygame.display.flip()
                pygame.time.delay(5000)
                sys.exit()


            mundo, jugador1, jugador2, jugadores = cargar_nivel(nivel)
            tiempo_inicio = pygame.time.get_ticks()
            llave_tocada = False
            continue

        for letal in mundo.letales:
            if letal.colliderect(jugador1.rect) or letal.colliderect(jugador2.rect):
                sonido_muerte.play()
                mundo, jugador1, jugador2, jugadores = cargar_nivel(nivel)
                tiempo_inicio = pygame.time.get_ticks()
                llave_tocada = False
                continue

        tiempo_actual = pygame.time.get_ticks()
        tiempo_limite = constantes.tiempos[nivel-1]
        tiempo_transcurrido = tiempo_actual - tiempo_inicio

        if tiempo_transcurrido >= tiempo_limite:
            mundo, jugador1, jugador2, jugadores = cargar_nivel(nivel)
            tiempo_inicio = pygame.time.get_ticks()
            llave_tocada = False
            continue

        tiempo_restante = (tiempo_limite - tiempo_transcurrido) / 1000
        texto_tiempo = fuente.render(f"{tiempo_restante:.3f}", True, (255, 255, 255))
        ventana.blit(texto_tiempo, (constantes.ancho/2 - constantes.tile_size, 30))

        if not llave_tocada:
            for llave in mundo.llaves:
                if jugador1.rect.colliderect(llave) or jugador2.rect.colliderect(llave):
                    llave_tocada = True
                    for puerta in mundo.puertas[:]:
                        if puerta in mundo.obstaculos:
                            mundo.obstaculos.remove(puerta)
                        mundo.puertas.remove(puerta)
                    mundo.llaves.remove(llave)
                    break

        clock.tick(constantes.fps)
        pygame.display.flip()
