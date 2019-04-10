#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from funcionesMovimientoSimulado import gira, move
import matplotlib.pyplot as plt
import mapas

## Declaración de operadores
arriba = '^'
abajo = 'v'
izquierda = '<'
derecha = '>'

def recorreCamino(camino, orientacion, robot, final):
    for direccion in camino:
        if direccion == arriba:
            mueveArriba(orientacion, robot)
        elif direccion == abajo:
            mueveAbajo(orientacion, robot)
        elif direccion == izquierda:
            mueveIzquierda(orientacion, robot)
        elif direccion == derecha:
            mueveDerecha(orientacion, robot)
        else:
            print("ERROR: No existe la dirección en la que se está intentando dirigir el robot")
        orientacion = direccion
        plot_robot_part(mapas.get_mundo(), 4.0, robot, final)


def mueveArriba(orientacion, robot):
    if (orientacion != arriba):
        if (orientacion == abajo):
            gira(robot, 180, 0.5)
        elif (orientacion == izquierda):
            gira(robot, 90, 0.5)
        elif (orientacion == derecha):
            gira(robot, -90, 0.5)
    move(robot, 40, 0.5)

def mueveAbajo(orientacion, robot):
    if (orientacion != abajo):
        if (orientacion == arriba):
            gira(robot, 180, 0.5)
        elif (orientacion == izquierda):
            gira(robot, -90, 0.5)
        elif (orientacion == derecha):
            gira(robot, 90, 0.5)
    move(robot, 40, 0.5)

def mueveIzquierda(orientacion, robot):
    if (orientacion != izquierda):
        if (orientacion == derecha):
            gira(robot, 180, 0.5)
        elif (orientacion == abajo):
            gira(robot, 90, 0.5)
        elif (orientacion == arriba):
            gira(robot, -90, 0.5)
    move(robot, 40, 0.5)

def mueveDerecha(orientacion, robot):
    if (orientacion != derecha):
        if (orientacion == izquierda):
            gira(robot, 180, 0.5)
        elif (orientacion == abajo):
            gira(robot, -90, 0.5)
        elif (orientacion == arriba):
            gira(robot, 90, 0.5)
    move(robot, 40, 0.5)



def plot_robot_part(mapa, ps, robot, final):
    mapa_imp = [[1 for j in range(len(mapa[0]))] for i in range(len(mapa))]
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            mapa_imp[i][j] = mapa_imp[i][j] - mapa[i][j]

    plt.scatter(robot.x / ps, robot.y / ps, marker='o', s=1000, c='r')
    plt.scatter(final[0], final[1], marker='x', s=100, c='b')
    plt.imshow(mapa_imp, origin='upper', extent=(0, len(mapa[0]), 0, len(mapa)))
    plt.gray()
    plt.show()