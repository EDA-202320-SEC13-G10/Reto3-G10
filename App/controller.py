﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    data = model.new_data_structs()
    return data


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    earthquakes_file = cf.data_dir + filename
    input_file = csv.DictReader(open(earthquakes_file,encoding="utf8"),
                                delimiter=",")

    for evento in input_file:
        model.add_data(control,evento)
    return control

def primernos_fiuankes (control):
    return model.first_last5(control)
# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control,initialDate,finalDate):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    L1, L2, L3, foliumsLista = model.req_1(control,initialDate,finalDate)
    if L3 >6:
        L1 = model.first_last3(L1)

    return L1, L2, L3, foliumsLista


def req_2(control,mag_i,mag_f):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    L1, L2, L3 = model.req_2(control,mag_i,mag_f)
    if L2 >6:
            L1 = model.first_last3(L1)

    return L1, L2, L3

def req_3(control,mag_i,depth_max):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    L1, L2, L3 = model.req_3(control,mag_i,depth_max)
    if L2 >6:
            L1 = model.first_last3(L1)

    return L1, L2, L3


def req_4(control, sig_min, gap_max):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    cant, sig_y_max = model.req_4(control, sig_min, gap_max)
    return cant, sig_y_max

def req_5(control, min_depth, min_nst):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    cant, dep_y_nst = model.req_5(control, min_depth, min_nst)
    return cant, dep_y_nst

def req_6(control,anio,lat,long,radio,n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    L1, L2, L3 = model.req_6(control,anio,lat,long,radio,n)

    return L1, L2, L3



def req_7(control, year, area, prop, bi):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    cant_year, cant_hist, min_value, max_value, hist_list = model.req_7(control, year, area, prop, bi)
    return cant_year, cant_hist, min_value, max_value, hist_list


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
