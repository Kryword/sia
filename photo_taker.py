# Script para grabar imagenes desde la camara del robot epuck
from ePuck import ePuck
import sys
import re
import time
from PIL import ImageStat

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
        while True:

            robot.step()
            image = robot.get_image()
            print('tiempo por step:', time.clock()-tant)
            tant = time.clock()
            time.sleep(1)
            if image != None:
                # Do something with the image
                stat = ImageStat.Stat(image)
                media = stat.mean
                print('Color:', media)
                color = "ninguno"
                if (media[0] > media[1] and media[0] > media[2]):
                    color = "rojo"
                elif(media[1] > media[0] and media[1] > media[2]):
                    color = "verde"
                elif (media[2] > media[0] and media[2] > media[1]):
                    color = "azul"

                print('Color mayoritario:', color, max(media))
                counter += 1
            #else:
            #	log('No image received!')

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
