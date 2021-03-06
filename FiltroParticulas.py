#!/usr/bin/python
# -*- coding: utf-8 -*-
# Algoritmo del filtro particulas
#

import math
import copy
import random
import numpy
# Importar el modulo donde esta la clase robot
import simRobot
# Importar el modulo donde tengo el mapa
import mapas
import matplotlib.pyplot as plt
import pprint
import aEstrella
import recorreCaminoSimulado
import funcionesMovimientoSimulado

## Declaración de operadores
arriba = '^'
abajo = 'v'
izquierda = '<'
derecha = '>'

## Datos posición iniciales
## MODIFICAR LA POSICIÓN DESDE AQUÍ
xI = 32
yI = 32
orientacionI = 0

## Generación de posición inicial aleatoria
# Orientación hacía la derecha
orientacionInicial = arriba

# Crear un objeto robot
r1 = simRobot.simepuck()
# Al imprimir el objeto se llama al metodo __repr__
print r1

# Asignamos el mapa en el que se va a mover el robot
mapa_mundo = mapas.get_mundo()
pixelsize = 4.0
mundo_limX = len(mapa_mundo[0]) * pixelsize
mundo_limY = len(mapa_mundo) * pixelsize

print mundo_limX, mundo_limY
mapa_suelo = mapas.get_suelo()
print mapa_mundo
print mapa_suelo

# FUNCIONES NECESARIAS:

# Necesitamos una funcion que calcule cuanto de parecido son dos mediciones (la que realiza el robot real y la que realiza la particula)
def similitud_Z(z1, z2):
    s = 0
    for i in range(len(z1)):
        s += ((z1[i] - z2[i])) ** 2
    s = (s ** 0.5) * 0.1
    return math.e ** (-s)


# Una funcion que calcula la posicion media de un conjunto de particulas
def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # hacer la orientacion media es dificil ya que es ciclica
        # normalizamos a partir de la primera particula para resolver el problema que 2pi = 0
        orientation += (((p[i].theta - p[0].theta + math.pi) % (2.0 * math.pi))
                        + p[0].theta - math.pi)
    return [x / len(p), y / len(p), orientation / len(p)]


# Imprimir robot en el mapa y todas las particulas
def plot_robot_part(mapa, ps, robot, part, col):
    mapa_imp = [[1 for j in range(len(mapa[0]))] for i in range(len(mapa))]
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            mapa_imp[i][j] = mapa_imp[i][j] - mapa[i][j]

    plt.scatter(robot.x / ps, robot.y / ps, marker='o', s=500, c='r')
    plt.scatter([part[i].x / ps for i in range(len(part))], [part[i].y / ps for i in range(len(part))], marker='o',
                s=20, c=col)
    plt.imshow(mapa_imp, origin='lower', extent=(0, len(mapa[0]), 0, len(mapa)))
    plt.gray()
    plt.show()


def dist(x, y, xp, yp):
    return math.sqrt((xp - x) ** 2 + (yp - y) ** 2)


# FILTRO PATICULAS:
# Primero vamos a crear una instancia de un robot que para nosotros va a ser el robot real:

real = simRobot.simepuck()
real.set_estado(xI, yI, orientacionI)
real.set_map(mapa_mundo, 4)
real.set_floor_map(mapa_suelo)

# Generar N particulas (instancias de robot) y colocarlas de forma aleatoria en lugares validos
N = 1000
particulas = []
i = 0
while i < N:
    # Crea una instancia de particula
    p = simRobot.simepuck()
    # 
    p.set_map(mapa_mundo, 4)
    p.set_floor_map(mapa_suelo)
    # Asignamos a todas las particulas la orientacion del robot real para que sea
    # mas sencillo localizar el robot
    theta = real.theta
    x = random.random() * mundo_limX
    y = random.random() * mundo_limY
    # theta = random.random() * 2 * math.pi
    p.set_estado(x, y, theta)
    if p.es_posible() == True:
        particulas.append(p)
        i += 1

# Imprimimos las particulas junto con el robot
plot_robot_part(mapa_mundo, pixelsize, real, particulas, 'b')

# Para comprobar el funcionamiento del algoritmo debes generar una serie de movimientos (por ejemplo 10) con el robot 'real', intenta que no se choque
# o acabe dentro de un obstaculo. Las velocidades de las ruedas se aplican durante un tiempo.

# Conjunto de movimientos que va a hacer el robot real:
Delta_t = 0.5
motions = [[400, 450, Delta_t], [-250, -450, Delta_t], [300, 450, Delta_t], [350, 450, Delta_t], [250, 450, Delta_t],
            [300, 350, Delta_t]]

def genera_nuevas_particulas(aParticulas, probabilidades):
    nuevasParticulas = []
    i = 0
    for i in range(N):
        numero = random.random()
        probAcumulada = probabilidades[0]
        j = 0
        while probAcumulada < numero:
            j += 1
            probAcumulada += probabilidades[j]

        if (probAcumulada >= numero):
            nuevasParticulas.append(copy.deepcopy(aParticulas[j]))

    return nuevasParticulas

# Bucle que simula el movimiento del robot.
# En cada movimiento se va actualizando las particulas mediante el remuestro. 
# Simulamos los movimientos del robot mediante un for.
posicionEstimada = [0, 0, 0]
for m in motions:
    # Primero mover el robot 'real'
    real.set_motors_speed(m[0], m[1], m[2])
    # Mover cada una de las particulas el mismo movimiento que el robot 'real'
    # Mirar si es posible el estado (si se choca). Si no es posible, mantener
    # la particula con el estado anterior.
    for p in particulas:
        pAnterior = p.get_estado()
        p.set_motors_speed(m[0], m[1], m[2])
        if (p.es_posible() == False):
            p.set_estado(pAnterior[0], pAnterior[1], pAnterior[2])
    # Realizar una medicion con el robot real
    zR = real.get_floor_sensors()

    # Realizar las mediciones de cada particula
    sumaPesos = 0
    i = 0
    w = numpy.zeros(N)
    probabilidades = numpy.zeros(N)
    while i < N:
        p = particulas[i]
        zP = p.get_floor_sensors()
        w[i] = similitud_Z(zR, zP)
        sumaPesos += w[i]
        i += 1
    # Calcular el peso de cada particula. El vector con todos los pesos debe
    # llamarse w.
    i = 0
    while i < N:
        probabilidades[i] = w[i] / sumaPesos
        i += 1
    # Calcular el nuevo conjunto de particulas utilizando la rueda de remuestreo
    nuevasparticulas = genera_nuevas_particulas(particulas, probabilidades)
    # Calcular la posicion media del conjunto de particulas
    posicionEstimada = get_position(particulas)
    print 'Posicion estimada:', posicionEstimada
    print 'Posición real: ', real.get_estado()
    # imprimir el robot y las particulas
    plot_robot_part(mapa_mundo, pixelsize, real, particulas, w)
    particulas = nuevasparticulas

# Cuando funcione el filtro particulas para detectar la poscion de la instancia 
# robot real, utiliza el codigo que has generado para localizar al robot epck
# sobre la cuadricula impresa.


# Obtener un camino válido y recorrerlo
# Posición a la que queremos llegar: x = 20, y = 20
print 'Posicion estimada final: ', posicionEstimada
print 'Posición real: ', real.get_estado()
posicionEnMapa = [0, 0]
posicionEnMapa[0] = math.floor(posicionEstimada[0]/4)
posicionEnMapa[1] = math.floor(posicionEstimada[1]/4)

posicionObjetivo = [12/4, 12/4] # posicion / pixelSize
matrizHeuristica = numpy.zeros([len(mapa_mundo), len(mapa_mundo)])
# Calculamos la atriz heuristica siguindo la distancia Manhattan
for i in range(len(mapa_mundo)):
    for j in range(len(mapa_mundo)):
        elem = mapa_mundo[i][j]
        if (elem == 1):
            matrizHeuristica[i][j] = 1000
        else:
            matrizHeuristica[i][j] = math.fabs(i - posicionObjetivo[0]) + math.fabs(j - posicionObjetivo[1])
print("Matriz de heurística:\n", matrizHeuristica)

print("////////////////////////////////////////////////")
print("//           Ejecutando algoritmo A*          //")
print("////////////////////////////////////////////////")
print("////////////////////////////////////////////////")

posicionEstimadaDiscretizada = [int(posicionEstimada[0]/4), int(posicionEstimada[1]/4)]
posicionObjetivoDiscretizada = [int(posicionObjetivo[0]), int(posicionObjetivo[1])]

print posicionEstimadaDiscretizada
print posicionObjetivoDiscretizada

resultadoAEstrella = aEstrella.algoritmoAEstrella(matrizHeuristica, posicionEstimadaDiscretizada, posicionObjetivoDiscretizada)
print("Camino obtenido: ", resultadoAEstrella.camino)

## TODO: Hacer una clase de recorreCamino para el simepuck, esta solo funcionaría con el epuck real
funcionesMovimientoSimulado.ajustarOrientacion(0, real)
recorreCaminoSimulado.recorreCamino(resultadoAEstrella.camino, orientacionInicial, real, posicionObjetivoDiscretizada)