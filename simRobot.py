# Clase simepuck
# Simula en comportamiento del robot epuck
# Los parametros estan en centimetros


import math
import random
import copy

class simepuck:
    # constructor
    def __init__(self):
        # definicion de caracteristicas fisicas del robot
        self.L = 5.3
        self.radius = 2.05
        self.motor_speed = (0,0)

        # posicion y orientacion de los sensores en el sistema de coordenadas del robot
        self.ps_x = [3.5, 2.5, 0.0, -3.5, -3.5, 0.0, 2.5, 3.5]
        self.ps_y = [-1.0, -2.5, -3.0, -2.0, 2.0, 2.0, 2.5, 1.0]
        self.ps_theta = [350, 320, 270, 200, 160, 90, 40, 10]
        self.ps_value = [3750, 2200, 676, 306, 245, 120]

        # posicion de los sensores del suelo
        self.fsl_x = 3.0
        self.fsl_y = 0.85
        self.fsc_x = 3.0
        self.fsc_y = 0.0
        self.fsr_x = 3.0
        self.fsr_y = -0.85

        # Posicion del robot en el sistema de coordenadas referencial
        self.x = 0
        self.y = 0
        self.theta = 0

        # Parametros de ruido ruido 
        self.motor_noise = 0.050
        self.ps_noise = 20
        self.fs_noise = 10

        # definicion de los mapas
        self.floor_map = []
        self.map = []
        self.sensor_map = []
        self.floor_map = []
        self.map_pixelsize = 0
        self.mundo_limX = 0
        self.mundo_limY = 0

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.theta))

    # Metodo para asignar la posicion del robot(en coordenadas del sistema referencial)    
    def set_estado(self, x,y,theta):
        self.x = x
        self.y = y
        self.theta = theta

    # Metodo que devuelve la posicion del robot (en coordenadas del sistema referencial)
    def get_estado(self):
        return (self.x, self.y, self.theta)

    # Metodo que devuelve si esa posicion es posible. Se compruebe si el centro del robot
    # o algun sensor estan en casillas ocupadas 
    def es_posible(self):
        R = [[math.cos(self.theta), - math.sin(self.theta)], [math.sin(self.theta), math.cos(self.theta)]]
        for sensor in range(0,8,1):
            s_x_ref = self.x + sum(a * b for a, b in zip(R[0][:], [self.ps_x[sensor], self.ps_y[sensor]]))
            s_y_ref = self.y + sum(a * b for a, b in zip(R[1][:], [self.ps_x[sensor], self.ps_y[sensor]]))
            # forzar a que esten dentro de los limites
            if s_x_ref < 0:
                s_x_ref = 0
            if s_y_ref < 0:
                s_y_ref = 0
            if s_x_ref > self.mundo_limX:
                s_x_ref = self.mundo_limX-0.01
            if s_y_ref > self.mundo_limY:
                s_y_ref = self.mundo_limY-0.01
            fil_s, col_s = self.fromMundo2Map(s_x_ref, s_y_ref)
            if self.map[fil_s][col_s] == 1:
                return False
        return True


    # Metodo para asignar un mapa en forma de matriz, en el que cada casilla representa si el espacio
    # esta libre u ocupado
    def set_map(self, mapa, pixelsize):
        self.map = copy.deepcopy(mapa)
        self.mundo_limX = len(self.map[0])*pixelsize
        self.mundo_limY = len(self.map)*pixelsize
        self.map_pixelsize = pixelsize

    # Metodo para asignar un mapa con los colores del suelo, cada casilla representa el color del suelo
    def set_floor_map(self, mapasuelo):
        self.floor_map = mapasuelo
     

    # Metodo que devuelve el valor de los sensores de suelo.
    def get_floor_sensors(self):
        # Calculamos la posicion del sensor de suelo en las coordenadas del sistema referencial
        # y se transforman a las posiciones de la matriz del mapa del suelo

        R = [[math.cos(self.theta), - math.sin(self.theta)], [math.sin(self.theta), math.cos(self.theta)]]
        fs_x_ref = self.x + sum(a * b for a, b in zip(R[0][:], [self.fsl_x, self.fsl_y]))
        fs_y_ref = self.y + sum(a * b for a, b in zip(R[1][:], [self.fsl_x, self.fsl_y]))
        fil_mapa, col_mapa = self.fromMundo2Map(fs_x_ref, fs_y_ref)
        floor_sensor_left = self.floor_map[fil_mapa][col_mapa]

        fs_x_ref = self.x + sum(a * b for a, b in zip(R[0][:], [self.fsc_x, self.fsc_y]))
        fs_y_ref = self.y + sum(a * b for a, b in zip(R[1][:], [self.fsc_x, self.fsc_y]))
        fil_mapa, col_mapa = self.fromMundo2Map(fs_x_ref, fs_y_ref)
        floor_sensor_center = self.floor_map[fil_mapa][col_mapa]

        fs_x_ref = self.x + sum(a * b for a, b in zip(R[0][:], [self.fsr_x, self.fsr_y]))
        fs_y_ref = self.y + sum(a * b for a, b in zip(R[1][:], [self.fsr_x, self.fsr_y]))
        fil_mapa, col_mapa = self.fromMundo2Map(fs_x_ref, fs_y_ref)
        floor_sensor_right = self.floor_map[fil_mapa][col_mapa]
        

        floor_sensor_left += random.gauss(0, self.fs_noise)
        floor_sensor_center += random.gauss(0, self.fs_noise)
        floor_sensor_right += random.gauss(0, self.fs_noise)
        
        return [floor_sensor_left, floor_sensor_center, floor_sensor_right]

    # Funcion que transforma las coordenadas del mapa a las coordenadas en el sistema referencial
    def fromMap2Mundo(self, fil_mapa, col_mapa):
        x = col_mapa * self.map_pixelsize
        y = (len(self.map) - (fil_mapa + 1)) * self.map_pixelsize
        return x,y

    # Funcion de transforma las corrdenadas del sistema referencial a las coordenadas del mapa
    def fromMundo2Map(self, x, y):
        col_mapa = math.floor(x / self.map_pixelsize)
        fil_mapa = len(self.map) - math.floor(y / self.map_pixelsize)-1
        return int(fil_mapa),int(col_mapa)

    # El metodo set_motors_speed actualiza el estado del robot despues de mover las ruedas a las velocidades
    # l_motor y r_motor durante un delta_t 
    # Las velocidades de los motores se pasan en la misma escala que al epuck (entre -1000 y 1000)
    def set_motors_speed(self, l_motor, r_motor, delta_t):
        # Calcular el nuevo estado del robot despues de aplicar la velocidad
        # a los motores despues de un periodo de tiempo
        Desp_r_l = (((2 * math.pi) / 1000.0) * l_motor) * delta_t * (self.radius)
        Desp_r_r = (((2 * math.pi) / 1000.0) * r_motor) * delta_t * (self.radius)

        Desp_r_l += random.gauss(0, self.motor_noise*Desp_r_l)
        Desp_r_r += random.gauss(0, self.motor_noise*Desp_r_r)

        Desp = (Desp_r_r + Desp_r_l) / 2.0
        Delta_theta = (Desp_r_r - Desp_r_l) / (self.L)

        x_old = self.x
        y_old = self.y
        theta_old = self.theta

        self.x = x_old + Desp * math.cos(theta_old + Delta_theta / 2.0)
        self.y = y_old + Desp * math.sin(theta_old + Delta_theta / 2.0)
        self.theta = theta_old + Delta_theta

    # En este metodo utilizando las ecuaciones de la odometria, este metodo actualiza
    # el estado del robot despues que el robot ha avanzado unos ticks_l en la rueda izquierda y 
    # ticks_r en la rueda derecha. Incluye el termino aleatorio para representar que el movimiento
    # no es exacto.
    def motion_odometry_model(self, ticks_l, ticks_r):

        Desp_r_l = (((2 * math.pi) / 1000.0) * ticks_l) * (self.radius)
        Desp_r_r = (((2 * math.pi) / 1000.0) * ticks_r) * (self.radius)

        Desp_r_l += random.gauss(0, self.motor_noise*Desp_r_l)
        Desp_r_r += random.gauss(0, self.motor_noise*Desp_r_r)

        Desp = (Desp_r_r + Desp_r_l) / 2.0
        Delta_theta = (Desp_r_r - Desp_r_l) / (self.L)

        x_old = self.x
        y_old = self.y
        theta_old = self.theta

        self.x = x_old + Desp * math.cos(theta_old + Delta_theta / 2.0)
        self.y = y_old + Desp * math.sin(theta_old + Delta_theta / 2.0)
        self.theta = theta_old + Delta_theta
    # Metodo que devuelve los valores del sensores de proximidad en el mismo
    # rango que el epuck (4000-0)
    # Si el parametro show vale 1 imprime por pantalla el mapa con la posicion del 
    # robot y las casillas ocupadas que ven los sensores
    
    def get_proximity(self):
        self.sensor_map = copy.deepcopy(self.map)
        fil_r, col_r = self.fromMundo2Map(self.x,self.y)
        self.sensor_map[fil_r][col_r] = 'R'

        proximity = []
        for s in range(0,8,1):
            dist = self.get_distance_sensor(s)
            val = self.fromDist2value(dist) + random.gauss(0, self.ps_noise)
            proximity.append(val)
        return proximity

    # Metodo auxiliar que calcula el valor que devuelve un sensor si ha visto
    # un objeto a una distancia
    def fromDist2value(self, distancia):
        i = 0
        while distancia > i and i <= 5:
            i = i + 1
        value = (-(self.ps_value[i-1] - self.ps_value[i])) * (distancia - i) + self.ps_value[i]
        return value

    # Metodo auxiliar que devuelve una lista de puntos en la direccion que esta mirando
    # el sensor
    def get_points_in_range(self,sensor):
        # Suponemos que el maximo rango son 5 cm
        # Creamos una lista con 10 puntos entre el sensor y el rango maximo
        # Primero calculamos los puntos en el sistema de coordenadas fijo al robot
        rango_max = 5.0
        points = []
        for i in range(0,10,1):
            x = self.ps_x[sensor] + (rango_max / 10.0 )* (i+1)  * math.cos(self.ps_theta[sensor] * 2 * math.pi / 360)
            y = self.ps_y[sensor] + (rango_max / 10.0) * (i+1) * math.sin(self.ps_theta[sensor] * 2 * math.pi / 360)
            points.append([x,y])

        # Cambiar la lista de puntos a coordenadas del sistema referencial
        R = [[math.cos(self.theta), - math.sin(self.theta)], [math.sin(self.theta), math.cos(self.theta)]]
        p_ref = []
        for p in points:
            x_ref = self.x + sum(a * b for a, b in zip(R[0][:], p))
            y_ref = self.y + sum(a * b for a, b in zip(R[1][:], p))
            # forzar a que esten dentro de los limites
            if x_ref < 0:
                x_ref = 0
            if y_ref < 0:
                y_ref = 0
            if x_ref > self.mundo_limX:
                x_ref = self.mundo_limX-0.01
            if y_ref > self.mundo_limY:
                y_ref = self.mundo_limY-0.01
            # anadir a la lista
            p_ref.append([x_ref,y_ref])
        return p_ref

    # Metodo auxiliar que calcula la distancia a la que esta un objeto en la direccion que esta
    # mirando el sensor. Si no hay ningun objeto devuelve el rango maximo del sensor
    def get_distance_sensor(self, sensor):
        # funcion que devuelve la distancia en centimetros desde el sensor hasta el objeto mas cercano
        # si no encuentra nada devuelve 5cm (el rango maximo del sensor)
        # Primero calculamos las coordenadas del sensor en el sistema de coordenadas referencial
        R = [[math.cos(self.theta), - math.sin(self.theta)], [math.sin(self.theta), math.cos(self.theta)]]
        s_x_ref = self.x + sum(a * b for a, b in zip(R[0][:], [self.ps_x[sensor], self.ps_y[sensor]]))
        s_y_ref = self.y + sum(a * b for a, b in zip(R[1][:], [self.ps_x[sensor], self.ps_y[sensor]]))

        points = self.get_points_in_range(sensor)
        # ver si en la lista de puntos hay alguno ocupado
        dist = 5.0
        for p in points:
            fil_p, col_p = self.fromMundo2Map(p[0], p[1])
            if self.map[fil_p][col_p] == 1:
                d = math.sqrt((s_x_ref - p[0])**2 + (s_y_ref - p[1])**2)
                if d < dist:
                    self.sensor_map[fil_p][col_p] = 'ps' + str(sensor)
                    dist = d
        return dist
