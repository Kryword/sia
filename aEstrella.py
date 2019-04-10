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

def sucesor(nodo, operador, matrizHeu):
    if (operador == arriba):
        return aplicaArriba(nodo, matrizHeu)
    elif(operador == abajo):
        return aplicaAbajo(nodo, matrizHeu)
    elif (operador == izquierda):
        return aplicaIzquierda(nodo, matrizHeu)
    elif (operador == derecha):
        return aplicaDerecha(nodo, matrizHeu)
    else:
        print "ERROR: Aplicando operador desconocido --> ", operador
        nodo.estado = [-1, -1]
        return nodo

def esSeguro(estado):
    return (mapa_mundo[estado[0]][estado[1]] != 1)

## Funciones que aplican los diferentes operadores

def aplicaArriba(nodo, matrizHeu):
    nodo.estado[1] -= 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(arriba)
        nodo.coste += 1
        nodo.heuristica = matrizHeu[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaAbajo(nodo, matrizHeu):
    nodo.estado[1] += 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(abajo)
        nodo.coste += 1
        nodo.heuristica = matrizHeu[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaIzquierda(nodo, matrizHeu):
    nodo.estado[0] -= 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(izquierda)
        nodo.coste += 1
        nodo.heuristica = matrizHeu[nodo.estado[0]][nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

def aplicaDerecha(nodo, matrizHeu):
    nodo.estado[0] += 1
    if(esSeguro(nodo.estado)):
        nodo.camino.append(derecha)
        nodo.coste += 1
        nodo.heuristica = matrizHeu[nodo.estado[0],nodo.estado[1]]
    else:
        nodo.estado = [-1,-1]
    return nodo

## Función que verifica si hemos alcanzado el estado final
def es_estado_final(estado, estado_final):
    return (estado[0] == estado_final[0] and estado[1] == estado_final[1])

def sucesores(nodo,matrizHeu):
    colaSucesores = Queue()
    for i in [arriba, abajo, izquierda, derecha]:
        nodoAux = copy.deepcopy(nodo)
        rtaSucesor = sucesor(nodoAux, i , matrizHeu)
        if(rtaSucesor['estado'] != [-1,-1]):
            colaSucesores.put(rtaSucesor)
    return colaSucesores

def gestionar_cola(ABIERTOS, NUEVOS_SUCESORES):
    colaOrdenada = Queue()

    listaAuxAbiertos = []
    listaFinal = []

    while (not ABIERTOS.empty()):
        nodoSucesor = ABIERTOS.get()
        listaAuxAbiertos.append(nodoSucesor)
        listaFinal.append(nodoSucesor)

    while (not NUEVOS_SUCESORES.empty()):
        nodoSucesor = NUEVOS_SUCESORES.get()
        if (nodoSucesor not in listaAuxAbiertos):
            listaFinal.append(nodoSucesor)
    listaFinal.sort(key = lambda nodo: nodo.coste + nodo.heuristica, reverse = False)

    for i in listaFinal:
        colaOrdenada.put(i)

    return colaOrdenada

## Algoritmo principal
def algoritmoAEstrella(matrizHeu, estado_inicial, estado_final):

    #matrizHeuristica = copy.deepcopy(matrizHeu)

    ABIERTOS = Queue()
    CERRADOS = Queue()
    NUEVOS_SUCESORES = Queue()

    # Hacer ABIERTOS la "cola" formada por el nodo inicial
    nodo_inicial = Nodo(estado_inicial)
    ABIERTOS.put(nodo_inicial)
    while(not ABIERTOS.empty()):
        ACTUAL = ABIERTOS.get()
        CERRADOS.put(ACTUAL)
        if(es_estado_final(ACTUAL.estado, estado_final)):
            print str(ACTUAL.camino)
            return ACTUAL
        else:
            NUEVOS_SUCESORES = sucesores(ACTUAL,matrizHeu)
            ABIERTOS = gestionar_cola(ABIERTOS,NUEVOS_SUCESORES)
