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
    vel = angulo/t
    inversaV = inversa(0, 0, vel)
    fiR = inversaV[0]
    fiL = inversaV[1]
    ticksPorSegundoR = radToTick(fiR)
    ticksPorSegundoL = radToTick(fiL)
    t1 = time.clock()
    #print "Giro: ", vel, inversa, ticksPorSegundoR, ticksPorSegundoL
    while(time.clock() - t1 <= t):
        posicion = robot.get_motor_position()
        robot.set_motor_position(0, 0)
        robot.set_motors_speed(ticksPorSegundoL, ticksPorSegundoR)
        robot.step()
    robot.set_motors_speed(0, 0)

def move(robot, dist, t):
    t = float(t)
    vel = dist/t
    inversaV = inversa(vel, 0, 0)
    fiR = inversaV[0]
    fiL = inversaV[1]
    ticksPorSegundo = radToTick(float(fiR))
    t1 = time.clock()
    while(time.clock() - t1 <= t):
        posicion = robot.get_motor_position()
        robot.set_motor_position(0, 0)
        robot.set_motors_speed(ticksPorSegundo, ticksPorSegundo)
        robot.step()
    robot.set_motors_speed(0, 0)