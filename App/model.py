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
import time as tm
import datetime
import math
import folium
from tabulate import tabulate

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
    data["anio_Index"] =  om.newMap(omaptype="BST")
    return data

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    data["mag"] = float(data["mag"])
    data["depth"] = float(data["depth"])
    lt.addLast(data_structs["datos"],data)
    lista_posible =[""," ", None]
    keys = ["mag","place","time","updated","tz","felt",
            "cdi","mmi","alert","status","tsunami","sig",
            "net","code","ids","sources","types","nst",
            "dmin","rms","gap","magType","type","title",
            "long","lat","depth"]    
    for i in keys:
        if data[i] in lista_posible:
            data[i] = "Unknown"
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
    update_anio_Index(data_structs["anio_Index"], data)
    
# Funciones para creacion de datos

def new_data(id, info):

    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def update_anio_Index(map, evento):
    ocurredTime  = (evento["time"])[:4]
    entry = om.get(map,ocurredTime)
    if entry is None:
        evento_entry = new_anio_Entry(evento)
        om.put(map,ocurredTime,evento_entry)
    else:
        evento_entry = me.getValue(entry)  
        lt.addLast(evento_entry["lst_events"], evento)
    
    return map

def update_Date_Index(map, evento):
    ocurredTime  = evento["time"]
    ocurredTime  = ocurredTime[:16]
    
    entry = om.get(map,ocurredTime)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,ocurredTime,evento_entry)
    else:
        evento_entry = me.getValue(entry)  
        lt.addLast(evento_entry["lst_events"], evento)      
    return map

def update_mag_Index(map, evento):
    mag  = float(evento["mag"])
    entry = om.get(map,mag)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,mag,evento_entry)
    else:
        evento_entry = me.getValue(entry)
        lt.addLast(evento_entry["lst_events"], evento)    
    return map

def new_anio_Entry(evento):
    entry = {"map_per_date" : om.newMap(omaptype="BST"),
             "lst_events": None}

    entry["lst_events"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lst_events"], evento)
    return entry

def update_gap_Index(map, evento):
    gap  = evento["gap"]
    entry = om.get(map,gap)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,gap,evento_entry)
    else:
        evento_entry = me.getValue(entry)    
    return map

def update_sig_Index(map, evento):
    sig  = evento["sig"]
    entry = om.get(map,sig)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,sig,evento_entry)
    else:
        evento_entry = me.getValue(entry)    
    return map

def update_depth_Index(map, evento):
    depth  = evento["depth"]
    entry = om.get(map,depth)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,depth,evento_entry)
    else:
        evento_entry = me.getValue(entry)    
    return map

def update_nst_Index(map, evento):
    nst  = evento["nst"]
    entry = om.get(map,nst)
    if entry is None:
        evento_entry = new_Data_Entry(evento)
        om.put(map,nst,evento_entry)
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
   
    lst = om.values(data_structs["date_Index"], initialDate, finalDate)
    lst1 = om.keys(data_structs["date_Index"], initialDate, finalDate)
    diferent_dates = lt.size(lst1)
    totalevents = 0
    h = lt.newList("ARRAY_LIST")
    lista_folium = []
    for l in lt.iterator(lst1):
        k = {}
        
        events_in_l = om.get(data_structs["date_Index"],l)
        k["time"] = l
        k["events"] = lt.size(events_in_l['value']['lst_events'])
        totalevents += lt.size(events_in_l['value']['lst_events'])
        k["details"] = []
        for y in events_in_l['value']['lst_events']["elements"]:
            dict_new = {}
            lista_per_lista =[y["lat"],y["long"]]


            lista_folium.append(lista_per_lista)    
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
        k["details"] =  tabulate(k["details"], headers="keys", tablefmt="grid", showindex= False)

        lt.addLast(h,k)
    quk.sort(h,compareDates_req1)
    
    return h, totalevents, diferent_dates, lista_folium

def req_2(data_structs, lim_inf,lim_sup):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    lst1 = om.keys(data_structs["mag_Index"], lim_inf, lim_sup)
    lst = om.values(data_structs["mag_Index"], lim_inf, lim_sup)
    totalevents = 0
    totalmags = lt.size(lst1)
    for lstdate in lt.iterator(lst):
        totalevents += lt.size(lstdate["lst_events"])
    h = lt.newList("ARRAY_LIST")
    for l in lt.iterator(lst1):
        k = {}
        events_in_l = om.get(data_structs["mag_Index"],l)
        k["mag"] = l
        k["events"] = lt.size(events_in_l['value']['lst_events'])
        k["details"] = lt.newList("ARRAY_LIST")
        for y in events_in_l['value']['lst_events']["elements"]:
            dict_new = {}
            dict_new["time"] =  y["time"]
            dict_new["lat"] =  y["lat"]
            dict_new["long"] =  y["long"]
            dict_new["depth"] =  y["depth"]
            dict_new["sig"] =  y["sig"]
            dict_new["gap"] =  y["gap"]
            dict_new["nst"] =  y["nst"]
            dict_new["title"] =  y["title"]
            dict_new["cdi"] =  y["cdi"]
            dict_new["mmi"] =  y["mmi"]
            dict_new["magType"] =  y["magType"]
            dict_new["type"] =  y["type"]
            dict_new["code"] =  y["code"]
            lt.addLast(k["details"],dict_new)
        quk.sort(k["details"],compareDates_req1)
        if lt.size(k["details"]) > 6:
            k["details"] = first_last3(k["details"])
        k["details"] =  tabulate(lt.iterator(k["details"]), headers="keys", tablefmt="grid", showindex= False)
        lt.addLast(h,k)
    
    quk.sort(h,compareMag_req2)

    return h , totalmags,totalevents

def req_3(data_structs, mag_min, depth_max):
    """
    Función que soluciona el requerimiento 3
    """
    lst1 = om.keys(data_structs["mag_Index"], mag_min, 10.000)

    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs, sig_min, gap_max):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    dat = data_structs["gap_Index"]
    datos = om.valueSet(dat)
    sig_y_gap = lt.newList("ARRAY_LIST")
    for i in lt.iterator(datos):
        for j in i["lst_events"]["elements"]:
            if j["gap"] != "Unknown" and j["sig"] != "Unknown":
                if float(j["gap"]) <= gap_max and float(j["sig"]) >= sig_min:
                    x = {}
                    x["time"] = j["time"]
                    x["mag"] = j["mag"]
                    x["lat"] = j["lat"]
                    x["long"] = j["long"]
                    x["depth"] = j["depth"]
                    x["sig"] = j["sig"]
                    x["gap"] = j["gap"]
                    x["nst"] = j["nst"]
                    x["title"] = j["title"]
                    x["cdi"] = j["cdi"]
                    x["magType"] = j["magType"]
                    x["type"] = j["type"]
                    x["code"] = j["code"]
                    lt.addLast(sig_y_gap, x)
    return lt.size(sig_y_gap), sig_y_gap
                

def req_5(data_structs, min_depth, min_nst):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    dat = data_structs["nst_Index"]
    datos = om.valueSet(dat)
    dep_nst = lt.newList("ARRAY_LIST")
    for i in lt.iterator(datos):
        for j in i["lst_events"]["elements"]:
            if j["depth"] != "Unknown" and j["nst"] != "Unknown":
                if float(j["depth"]) >= min_depth and float(j["nst"]) >= min_nst:
                    x = {}
                    x["time"] = j["time"]
                    x["mag"] = j["mag"]
                    x["lat"] = j["lat"]
                    x["long"] = j["long"]
                    x["depth"] = j["depth"]
                    x["sig"] = j["sig"]
                    x["gap"] = j["gap"]
                    x["nst"] = j["nst"]
                    x["title"] = j["title"]
                    x["cdi"] = j["cdi"]
                    x["magType"] = j["magType"]
                    x["type"] = j["type"]
                    x["code"] = j["code"]
                    lt.addLast(dep_nst, x)
    return lt.size(dep_nst), dep_nst

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Radius of the Earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c # Distance in km
    return d

def req_6(data_structs,anio,lat,long,radio,n):
    """
    Función que soluciona el requerimiento 6
    """

    # TODO: Realizar el requerimiento 6
    data =  data_structs["anio_Index"]
    maps_date  = om.newMap(omaptype="BST")
    anio_lst = om.get(data,anio)
    presentacion = lt.newList()
    for valor in lt.iterator(anio_lst['value']['lst_events']):
        valor_haversine = haversine(float(lat),float(long),float(valor["lat"]),float(valor["long"]))
        if valor_haversine <=  radio:
            ocurredTime  = valor["time"]
            ocurredTime  = ocurredTime[:16] 
            entry = om.get(maps_date,ocurredTime)
            if entry is None:
                evento_entry = new_Data_Entry(valor)
                om.put(maps_date,ocurredTime,evento_entry)
            else:
                evento_entry = me.getValue(entry)  
                lt.addLast(evento_entry["lst_events"], valor)
    mayor = 0            
    tamanio = 0            
    for i in lt.iterator(om.keySet(maps_date)):
        tamanio += 1 
        valor_new =  om.get(maps_date,i)
        dict_append = {}
        dict_append["time"] = i
        dict_append["size"] = 0
        dict_append["details"] = []
        for y in lt.iterator(valor_new['value']['lst_events']):
                dict_append["size"] += 1 
                dict_new = {}   
                if float(y["mag"]) > mayor:
                    mayor = float(y["mag"])
                dict_new["mag"] =  y["mag"]
                dict_new["time"] =  y["time"]
                dict_new["cdi"] =  y["cdi"]
                dict_new["mmi"] =  y["mmi"]
                dict_new["code"] =  y["code"]
                dict_new["nst"] =  y["nst"]
                dict_new["gap"] =  y["gap"]
                dict_new["magType"] =  y["magType"]
                dict_new["type"] =  y["type"]
                dict_new["title"] =  y["title"]
                dict_new["lat"] =  y["lat"]
                dict_new["long"] =  y["long"]
                dict_new["depth"] =  y["depth"]
                dict_new["sig"] =  y["sig"]    
                dict_append["details"].append(dict_new)
        lt.addLast(presentacion,dict_new)
    pos = 0
    pos_i = 0
    for i in lt.iterator(presentacion):
        pos += 1
        
        if i["mag"] == mayor:
            pos_i = pos
            principal = []
            principal.append(i)
    lt.deleteElement(presentacion,pos_i)
    if lt.size(presentacion) > n:
        presentacion = sublista(presentacion,1,n)
    return principal, presentacion, tamanio


def req_7(data_structs, year, area, prop, bi):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    dat = data_structs["date_Index"]
    datos = om.valueSet(dat)
    hist_list = lt.newList("ARRAY_LIST")
    values = []
    cant_year = 0
    cant_hist = 0
    for i in lt.iterator(datos):
        for j in i["lst_events"]["elements"]:
            if j["time"] != "Unknown" and j["title"] != "Unknown" and j[prop] != "Unknown":
                if float(j["time"][:4]) == year:
                    cant_year += 1
                    if area in j["title"]:
                        cant_hist += 1
                        x = {}
                        x["time"] = j["time"]
                        x["mag"] = j["mag"]
                        x["lat"] = j["lat"]
                        x["long"] = j["long"]
                        x["depth"] = j["depth"]
                        x["sig"] = j["sig"]
                        x["gap"] = j["gap"]
                        x["nst"] = j["nst"]
                        x["title"] = j["title"]
                        x["code"] = j["code"]
                        x[prop] = j[prop]
                        lt.addLast(hist_list, x)
                        values.append(float(j[prop]))
    return cant_year, cant_hist, min(values), max(values), hist_list

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
    primeros = sublista(data_structs,1,3)
    ultimos = sublista(data_structs,data_sizel(data_structs)-2,3)
    for i in lt.iterator(ultimos):
        lt.addLast(primeros,i)
    return primeros

def first_last5(data_structs):
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
def compareDates_req1(date1, date2):
    """
    Compara dos fechas
    """
    return (date1["time"] > date2["time"])
def compareMag_req2(date1, date2):
    """
    Compara dos fechas
    """
    return (date1["mag"] > date2["mag"])