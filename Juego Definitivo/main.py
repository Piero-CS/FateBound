import pygame
import constantes
import sys
from personaje import Personaje
import csv
from mundo import Mundo
from pygame.mixer import *
pygame.init() #Inicia pygame

#Ventana
ventana = pygame.display.set_mode((constantes.ancho, constantes.alto)) #Muestra la ventana
pygame.display.set_caption("Fatebound") #Pone titulo

#Fuentes
fuente = pygame.font.Font("assets/fuentes/Minecraft.ttf", 50)
fuente_inicio = pygame.font.Font("assets/fuentes/Minecraft.ttf", 80)
fuente_min = pygame.font.Font("assets/fuentes/Minecraft.ttf", 20)

#Musica
pygame.mixer.init()

sonido_muerte = pygame.mixer.Sound("audio/muerte.mp3")
sonido_victoria = pygame.mixer.Sound("audio/victoria.mp3")

#FPS
clock = pygame.time.Clock()

#Cargar imagen jugador
jugador2_i = pygame.image.load("assets/personajes/ninja2.png") #Carga la imagen base
jugador2_i = pygame.transform.scale(jugador2_i, (jugador2_i.get_width() * constantes.escala, jugador2_i.get_height() * constantes.escala)) #Escala el personaje

jugador1_i = pygame.image.load("assets/personajes/ninja1.png") #Carga la imagen base
jugador1_i = pygame.transform.scale(jugador1_i, (jugador1_i.get_width() * constantes.escala, jugador1_i.get_height() * constantes.escala)) #Escala el personaje

tile_list = []
for x in range(constantes.n_tiles):
    tile_image = pygame.image.load(f"assets/tiles/tile ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (constantes.tile_size, constantes.tile_size))
    tile_list.append(tile_image)

#Mundo
def cargar_nivel(nivel):
    world_data = []
    for i in range(constantes.fila):
        filas = [0] * constantes.columna
        world_data.append(filas)

    ruta_csv = f"mapa/nivel{nivel}.csv"
    with open(ruta_csv, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                world_data[x][y] = int(columna)

    mundo = Mundo()
    mundo.procesar_data(world_data, tile_list)

    x1, y1 = mundo.pos_jugador1
    x2, y2 = mundo.pos_jugador2

    jugador1 = Personaje(x1, y1, jugador1_i) #Coloca el personaje en un (x, y) y que imagen tendrá
    jugador2 = Personaje(x2, y2, jugador2_i) #Coloca el personaje en un (x, y) y que imagen tendrá
    jugadores = pygame.sprite.Group(jugador1, jugador2)

    return mundo, jugador1, jugador2, jugadores

nivel = 1
niveles_superados = 0
mundo, jugador1, jugador2, jugadores = cargar_nivel(nivel)

#Ventana Inicio
def inicio():
    ventana.fill((0, 0, 0))
    texto = fuente_inicio.render("Fatebound", True, (255, 255, 255))
    subtexto = fuente.render("Pulse ESPACIO para comenzar", True, (255, 255, 255))
    minitex= fuente_min.render("Goty of the Year, FrayAlcca Studios", True, (255,255,255))
    ventana.blit(texto, (constantes.ancho/2 - texto.get_width()/2, constantes.alto/2-200))
    ventana.blit(subtexto, (constantes.ancho/2 - subtexto.get_width()/2, constantes.alto/2))
    ventana.blit(minitex,(constantes.ancho/2 - minitex.get_width()/2, constantes.alto/2 + 300))
    pygame.display.flip()

ventana_inicio = True
llave_tocada = False
#Llave
while True:
    if ventana_inicio:
        inicio()
        for event in pygame.event.get(): #Por cada evento del juego (Unica entrada)
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): #Cuando se cierra por el sistema o mediante la X
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #Cuando se presiona una tecla (Unica entrada)
                ventana_inicio = False
                tiempo_inicio = pygame.time.get_ticks()
                pygame.mixer_music.load("audio/cancion_juego.mp3")
                pygame.mixer_music.set_volume(0.4)
                pygame.mixer_music.play(-1)

    else:
        ventana.fill(constantes.fondo)  
        mundo.dibujar(ventana)
        teclas = pygame.key.get_pressed() #Registra cada que se mantiene la tecla 
        for event in pygame.event.get(): #Por cada evento del juego (Unica entrada)
            if event.type == pygame.QUIT: #Cuando se cierra por el sistema o mediante la X
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Cuando se presiona una tecla (Unica entrada) y es ESCAPE
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
                texto = fuente_inicio.render("¡Ganaste!", True, (255, 255, 0))
                ventana.blit(texto, (constantes.ancho / 2 - texto.get_width() / 2, constantes.alto / 2))
                pygame.display.flip()
                pygame.time.delay(4000)
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
                    # Elimina las puertas tanto de obstáculos como de la lista de puertas
                    for puerta in mundo.puertas[:]:  # Iterar sobre una copia para modificar la lista original
                        if puerta in mundo.obstaculos:
                            mundo.obstaculos.remove(puerta)
                        mundo.puertas.remove(puerta)
                    # Si quieres que la llave también desaparezca (opcional):
                    mundo.llaves.remove(llave)
                    break  # Salir del bucle tras recoger la llave

        clock.tick(constantes.fps)
        pygame.display.flip()