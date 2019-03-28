# Script para grabar imagenes desde la camara del robot epuck
from ePuck import ePuck
import sys
import re
import time
from PIL import ImageStat

valorLimiteMenorProximidad = 200
errorProximidad = 100
### Funciones de la practica 2 de utilidad
import math
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

def log(text):
    """	Show @text in standart output with colors """
    blue = '\033[1;34m'
    off = '\033[1;m'
    print(''.join((blue, '[Log] ', off, str(text))))


def error(text):
    red = '\033[1;31m'
    off = '\033[1;m'
    print(''.join((red, '[Error] ', off, str(text))))


def run(mac):

    print('Connecting with the ePuck')
    try:
        robot = ePuck(mac)
        robot.connect()
        robot.enable('camera', 'motor_position', 'motor_speed', 'floor', 'proximity')

        robot.set_camera_parameters('RGB_365', 40, 40, 4)
        log('Conection complete. CTRL+C to stop')
        log('Library version: ' + robot.version)

    except Exception, e:
        error(e)
        sys.exit(1)

    try:
        counter = 0
        robot.set_motors_speed(0, 0)
        robot.set_motor_position(0, 0)
        tant = time.clock()

        # busca una pared para chocarse
        positionFound = True
        while positionFound:
            sensoresProximidad = robot.get_proximity()
            robot.step()
            if (max(sensoresProximidad) < 3000):
                move(robot, 20, 0.4)
            else:
                positionFound = False
            print("Sensores: ", sensoresProximidad)
        positionFound = True
        while positionFound:
            sensoresProximidad = robot.get_proximity()
            robot.step()
            if (sensoresProximidad[3] < max(sensoresProximidad) and sensoresProximidad[4] < max(sensoresProximidad)):
                gira(robot, 20, 0.5)
            else:
                move(robot, 100, 2)
                positionFound = False
        #while True:
            #sensoresProximidad = robot.get_proximity()
            #robot.step()

            ## Calculo de imagenes y colores
            # image = robot.get_image()
            # if (time.clock() - tant > 1):
            #     print('tiempo por step:', time.clock() - tant)
            #     tant = time.clock()
            #     if image != None:
            #         # Do something with the image
            #         stat = ImageStat.Stat(image)
            #         media = stat.mean
            #         limite = 80
            #         limite2 = 70
            #         print('Color:', media)
            #         color = "ninguno"
            #         if (media[0] > media[1] and media[0] > media[2]):
            #             color = "rojo"
            #             if(media[0] < limite and (media[1] > limite2 or media[2] > limite2)):
            #                 gira(robot, 20, 0.5)
            #         elif(media[1] > media[0] and media[1] > media[2]):
            #             color = "verde"
            #             gira(robot, 20, 0.5)
            #         elif (media[2] > media[0] and media[2] > media[1]):
            #             color = "azul"
            #             gira(robot, 20, 0.5)
            #
            #         print('Color mayoritario:', color, max(media))
            #         counter += 1
            ## Fin calculo de imagen
            #print("Sensores: ", sensoresProximidad)

        robot.stop()
        robot.step()

        time.sleep(1)

    except KeyboardInterrupt:
        log('Stoping the robot. Bye!')
        robot.close()
        sys.exit()
    except Exception, e:
        error(e)

    return 0


run('10:00:e8:ad:78:35')
