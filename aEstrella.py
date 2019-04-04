#!/usr/bin/python
# -*- coding: utf-8 -*-

import mapas
import simRobot
from Queue import Queue

## Tamaño de un cuadrado 4cm
tCuadrado = 4

## Implementación del algoritmo A*

## Declaración de estados
estados = []

for i in range(len(mapas.get_mundo())):
    for j in range(len(mapas.get_mundo())):
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

def sucesor(estado, operador):
    if (operador == arriba):
        return aplicaArriba(estado)
    elif(operador == abajo):
        return aplicaAbajo(estado)
    elif (operador == izquierda):
        return aplicaIzquierda(estado)
    elif (operador == derecha):
        return aplicaDerecha(estado)
    else:
        print "ERROR: Aplicando operador desconocido --> ", operador
        return [-1, -1]

## Funciones que aplican los diferentes operadores
## TODO: Completar operadores verficando si es seguro
## TODO: Aplicar costes y heurísticas a los nodos devueltos
## TODO: Añadir operador de camino
def aplicaArriba(estado):
    return [estado[0], estado[1] - 1]

def aplicaAbajo(estado):
    return [estado[0], estado[1] + 1]

def aplicaIzquierda(estado):
    return [estado[0] - 1, estado[1]]

def aplicaDerecha(estado):
    return [estado[0] + 1, estado[1]]

## Función que verifica si hemos alcanzado el estado final
def es_estado_final(estado):
    return (estado[0] == estado_final[0] and estado[1] == estado_final[1])

def sucesores(nodo):
    colaSucesores = Queue()
    for i in [arriba, abajo, izquierda, derecha]:
        colaSucesores.put(sucesores(nodo, i))
    return colaSucesores

## Algoritmo principal
def algoritmoAEstrella():
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
            while (~NUEVOS_SUCESORES.empty()):
                nodoSucesor = NUEVOS_SUCESORES.get()
                ABIERTOS.put(nodoSucesor)
            ## TODO: ORDENAR ABIERTOS en función de coste-más-heurística
            ## TODO: Verificar que en ABIERTOS no están esos nodos