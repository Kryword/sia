#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from funcionesMovimiento import gira, move

## Declaración de operadores
arriba = '^'
abajo = 'v'
izquierda = '<'
derecha = '>'

def recorreCamino(camino, orientacion, robot):
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