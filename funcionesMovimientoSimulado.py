#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import time

r = 41/2.0
b = 53/2.0

def directa(fiR, fiL):
    x = r/2 * fiR + r/2*fiL
    y = 0
    o = r/(2*b) * fiR - r/(2*b) * fiL
    return [x, y, o]

def inversa(x, y, o):
    fiR = 1/r*x+b/r*o
    fiL = 1/r*x-b/r*o
    return [fiR, fiL]

def radToTick(velAngular):
    return velAngular * 1000/(2*math.pi)

def tickToRad(ticks):
    return ticks/1000.0 * 2 * math.pi
## Fin funciones de utilidad

def gira(robot, ang, t):
    t = float(t)
    angulo = ang/180.0*math.pi
    inversaV = inversa(0, 0, angulo)
    fiR = inversaV[0]
    fiL = inversaV[1]
    ticksR = radToTick(fiR)
    ticksL = radToTick(fiL)
    robot.set_motors_speed(ticksL, ticksR, t)
    print ticksR, ticksL, t
    print robot.get_estado()

def move(robot, dist, t):
    t = float(t)
    inversaV = inversa(dist, 0, 0)
    fiR = inversaV[0]
    fiL = inversaV[1]
    ticks = radToTick(fiR)
    robot.set_motors_speed(ticks, ticks, t)
    print ticks, ticks, t
    print robot.get_estado()

def ajustarOrientacion(ang, robot):
    angulo = ang/180.0*math.pi
    fallo = 0.2
    ticks = 1000
    t = 0.1
    estado = robot.get_estado()
    print estado
    print "angulo: ", angulo
    while (estado[2] < angulo - fallo or estado[2] > angulo + fallo):
        robot.set_motors_speed(ticks, -ticks, t)
        estado = robot.get_estado()
        print estado