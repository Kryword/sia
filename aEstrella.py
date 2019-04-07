#!/usr/bin/python
# -*- coding: utf-8 -*-

import mapas
import numpy
import simRobot
from Queue import Queue

## Tamaño de un cuadrado 4cm
tCuadrado = 4

# Asignamos el mapa en el que se va a mover el robot
mapa_mundo = mapas.get_mundo()

## Implementación del algoritmo A*

## Declaración de estados
estados = []

for i in range(len(mapa_mundo)):
    for j in range(len(mapa_mundo)):
        estados.append([i, j])

## Declaración de operadores
arriba = '^'
abajo = 'v'
izquierda = '<'
derecha = '>'

estado_final = [15, 15]
nodo_inicial = {
    "coste": 0,
    "heurística": 0,
    "camino": [],
    "estado": [6, 6]} # se obtendrá del filtro de particulas


matrizCosteMasHeuristica = numpy.zeros([len(mapa_mundo), len(mapa_mundo)])

def sucesor(nodo, operador):
    if (operador == arriba):
        return aplicaArriba(nodo)
    elif(operador == abajo):
        return aplicaAbajo(nodo)
    elif (operador == izquierda):
        return aplicaIzquierda(nodo)
    elif (operador == derecha):
        return aplicaDerecha(nodo)
    else:
        print "ERROR: Aplicando operador desconocido --> ", operador
        nodo['estado'] = [-1, -1]
        return nodo

## Funciones que aplican los diferentes operadores
## TODO: Completar operadores verficando si es seguro
## TODO: Aplicar costes y heurísticas a los nodos devueltos

def aplicaArriba(nodo):
    if(matrizCosteMasHeuristica != 2000):
        nodo['estado'] = [nodo['estado'][0], nodo['estado'][1] - 1]
        nodo['camino'].append(arriba)
        #nodo['coste'] =
        #nodo['heuristica'] =
    else:
        nodo['estado'] = [-1,-1]
    return nodo

def aplicaAbajo(estado):
    return [estado[0], estado[1] + 1]

def aplicaIzquierda(estado):
    return [estado[0] - 1, estado[1]]

def aplicaDerecha(estado):
    return [estado[0] + 1, estado[1]]

## Función que verifica si hemos alcanzado el estado final
def es_estado_final(nodoActual):
    return (nodoActual['estado'][0] == estado_final[0] and nodoActual['estado'][1] == estado_final[1])

def sucesores(nodo):
    colaSucesores = Queue()
    for i in [arriba, abajo, izquierda, derecha]:
        rtaSucesor = sucesor(nodo, i)
        if(rtaSucesor['estado'] == [-1,-1]):
            colaSucesores.put(rtaSucesor)
    return colaSucesores

def gestionar_cola(ABIERTOS, NUEVOS_SUCESORES):
    colaOrdenada = Queue()
    while (~NUEVOS_SUCESORES.empty()):
        nodoSucesor = NUEVOS_SUCESORES.get()
        colaOrdenada.put(nodoSucesor)
    ## TODO: ORDENAR ABIERTOS en función de coste-más-heurística
    ## TODO: Verificar que en ABIERTOS no están esos nodos
    return colaOrdenada

## Algoritmo principal
def algoritmoAEstrella(matrizCostHeu):
    matrizCosteMasHeuristica = matrizCostHeu
    ABIERTOS = Queue()
    CERRADOS = Queue()
    NUEVOS_SUCESORES = Queue()

    # Hacer ABIERTOS la "cola" formada por el nodo inicial
    ABIERTOS.add(nodo_inicial)
    while(~ABIERTOS.empty()):
        ACTUAL = ABIERTOS.get()
        CERRADOS.add(ACTUAL)
        if(es_estado_final(ACTUAL)):
            return ACTUAL
        else:
            NUEVOS_SUCESORES = sucesores(ACTUAL)
            ABIERTOS = gestionar_cola(ABIERTOS,NUEVOS_SUCESORES)
