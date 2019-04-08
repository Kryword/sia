#!/usr/bin/python
# -*- coding: utf-8 -*-

import mapas
import numpy
import simRobot
from Queue import Queue, Empty
from nodo import Nodo
import copy

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
nodo_inicial = Nodo([6, 6]) # Del filtro de partículas

matrizCoste = numpy.zeros([len(mapa_mundo), len(mapa_mundo)])
matrizHeuristica = numpy.zeros([len(mapa_mundo), len(mapa_mundo)])
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
        nodo.estado = [-1, -1]
        return nodo

def esSeguro(estado):
    return (mapa_mundo[estado[0]][estado[1]] != 1)

## Funciones que aplican los diferentes operadores

def aplicaArriba(nodo):
    nodo.estado[1] -= 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(arriba)
        nodo.coste += 1
        nodo.heuristica = matrizHeuristica[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaAbajo(nodo):
    nodo.estado[1] += 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(abajo)
        nodo.coste += 1
        nodo.heuristica = matrizHeuristica[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaIzquierda(nodo):
    nodo.estado[0] -= 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(izquierda)
        nodo.coste += 1
        nodo.heuristica = matrizHeuristica[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaDerecha(nodo):
    nodo.estado[0] += 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(derecha)
        nodo.coste += 1
        nodo.heuristica = matrizHeuristica[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

## Función que verifica si hemos alcanzado el estado final
def es_estado_final(estado):
    return (estado[0] == estado_final[0] and estado[1] == estado_final[1])

def sucesores(nodo):
    colaSucesores = Queue()
    for i in [arriba, abajo, izquierda, derecha]:
        nodoAux = copy.deepcopy(nodo)
        rtaSucesor = sucesor(nodoAux, i)
        if(rtaSucesor['estado'] != [-1,-1]):
            colaSucesores.put(rtaSucesor)
    return colaSucesores

def gestionar_cola(ABIERTOS, NUEVOS_SUCESORES):
    colaOrdenada = Queue()

    listaAuxAbiertos = []
    listaFinal = []

    try:
        while (~ABIERTOS.empty()):
            nodoSucesor = ABIERTOS.get()
            listaAuxAbiertos.append(nodoSucesor)
            listaFinal.append(nodoSucesor)
    except Empty:
        pass

    while (~NUEVOS_SUCESORES.empty()):
        nodoSucesor = NUEVOS_SUCESORES.get()
        if (nodoSucesor not in listaAuxAbiertos):
            listaFinal.append(nodoSucesor)
    listaFinal.sort(key = lambda nodo: nodo.coste + nodo.heuristica, reverse = False)

    for i in listaFinal:
        colaOrdenada.put(i)    

    return colaOrdenada

## Algoritmo principal
def algoritmoAEstrella(matrizHeu, matrizCostHeu):
    matrizHeuristica = copy.deepcopy(matrizHeu)
    matrizCosteMasHeuristica = copy.deepcopy(matrizCostHeu)
    ABIERTOS = Queue()
    CERRADOS = Queue()
    NUEVOS_SUCESORES = Queue()

    # Hacer ABIERTOS la "cola" formada por el nodo inicial
    ABIERTOS.put(nodo_inicial)
    while(~ABIERTOS.empty()):
        ACTUAL = ABIERTOS.get()
        CERRADOS.put(ACTUAL)
        if(es_estado_final(ACTUAL.estado)):
            return ACTUAL
        else:
            NUEVOS_SUCESORES = sucesores(ACTUAL)
            ABIERTOS = gestionar_cola(ABIERTOS,NUEVOS_SUCESORES)
