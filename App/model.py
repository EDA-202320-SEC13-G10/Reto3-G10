"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data = {
        "datos" :None,
        "date_Index": None
    }
    data["datos"] = lt.newList("ARRAY_LIST")
    data["datos_lobby"] = lt.newList("ARRAY_LIST")
    data["date_Index"] =  om.newMap(omaptype="BST")
    data["mag_Index"] =  om.newMap(omaptype="BST")
    return data

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs["datos"],data)
    lista_posible =[""," ", None]
    keys = ["mag","place","time","updated","tz","felt",
            "cdi","mmi","alert","status","tsunami","sig",
            "net","code","ids","sources","types","nst",
            "dmin","rms","gap","magType","type","title",
            "long","lat","depth"]    
    for i in keys:
        if data[i] in lista_posible:
            data[i] = "Unkown"
    datos_lobby = {} 
    datos_lobby["code"] =  data["code"]
    datos_lobby["time"] =  (data["time"])[:16]
    datos_lobby["lat"] =  data["lat"]
    datos_lobby["long"] =  data["long"]
    datos_lobby["mag"] =  data["mag"]
    datos_lobby["title"] =  data["title"]
    datos_lobby["depth"] =  data["depth"]
    datos_lobby["felt"] =  data["felt"]
    datos_lobby["cdi"] =  data["cdi"]
    datos_lobby["mmi"] =  data["mmi"]
    if  data["tsunami"] == "0":
        datos_lobby["tsunami"] = "False"
    else:
        datos_lobby["tsunami"] = "True"

    lt.addLast(data_structs["datos_lobby"],datos_lobby)
    update_Date_Index(data_structs["date_Index"], data)
    update_mag_Index(data_structs["mag_Index"], data)
    


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def update_Date_Index(map, evento):
    ocurredTime  = evento["time"]
    ocurredTime  = ocurredTime[:16]
    eventoTime = datetime.datetime.strptime(ocurredTime,"%Y-%m-%dT%H:%M")
    entry = om.get(map,eventoTime.date())
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,eventoTime.date(),evento_entry)
    else:
        evento_entry = me.getValue(entry)    
    return map

def update_mag_Index(map, evento):
    mag  = evento["mag"]
    entry = om.get(map,mag)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,mag,evento_entry)
    else:
        evento_entry = me.getValue(entry)    
    return map

def new_Data_Entry(evento):
    entry = { "lst_events": None}

    entry["lst_events"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lst_events"], evento)
    return entry

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs,initialDate,finalDate):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    initialDate = datetime.datetime.strptime(initialDate, "%Y-%m-%dT%H:%M")
    finalDate = datetime.datetime.strptime(finalDate, "%Y-%m-%dT%H:%M")
    lst = om.values(data_structs["date_Index"], initialDate.date(), finalDate.date())
    lst1 = om.keys(data_structs["date_Index"], initialDate.date(), finalDate.date())
    totalevents = 0
    for lstdate in lt.iterator(lst):
        totalevents += lt.size(lstdate["lst_events"])
    h = lt.newList("ARRAY_LIST")

    for l in lt.iterator(lst1):
        k = {}
        events_in_l = om.get(data_structs["date_Index"],l)
        k["Line"] = l
        k["events"] = lt.size(events_in_l['value']['lst_events'])
        k["details"] = []
        for y in events_in_l['value']['lst_events']["elements"]:
            dict_new = {}
            dict_new["mag"] =  y["mag"]
            dict_new["lat"] =  y["lat"]
            dict_new["long"] =  y["long"]
            dict_new["depth"] =  y["depth"]
            dict_new["sig"] =  y["sig"]
            dict_new["gap"] =  y["gap"]
            dict_new["nst"] =  y["nst"]
            dict_new["title"] =  y["title"]
            dict_new["mmi"] =  y["mmi"]
            dict_new["magType"] =  y["magType"]
            dict_new["type"] =  y["type"]
            dict_new["code"] =  y["code"]
            k["details"].append(dict_new)
        lt.addLast(h,k)
        merg.sort(h,compareDates1)
    return h

def req_2(data_structs, lim_inf,lim_sup):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento
def data_sizel(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(data_structs) 

def sublista(data_structs, pos_i, num):
    s =  lt.subList(data_structs, pos_i, num)
    return s

def first_last3(data_structs):
    primeros = sublista(data_structs,1,5)
    ultimos = sublista(data_structs,data_sizel(data_structs)-4,5)
    for i in lt.iterator(ultimos):
        lt.addLast(primeros,i)
    return primeros

def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 < date2):
        return -1
    else:
        return 1
def compareDates1(date1, date2):
    """
    Compara dos fechas
    """
    return (date1["Line"] > date2["Line"])
