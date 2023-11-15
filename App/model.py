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

    lista_tabla = lt.newList("ARRAY_LIST")
    d_dates = 0
    d_events = 0
    mp1 = om.newMap(omaptype = 'RBT')
    for l in lt.iterator(lst1):
        events_in_l = om.get(data_structs["mag_Index"],l)
        for y in events_in_l['value']['lst_events']["elements"]:
            if y["depth"] <= depth_max:
                fecha = (y["time"])[:16]
                entry = om.get(mp1,fecha)
                if entry is None:
                    fecha_entry = new_Data_Entry(y)
                    om.put(mp1,fecha,fecha_entry)
                else:
                    fecha_entry = me.getValue(entry)
                    lt.addLast(fecha_entry["lst_events"], y)
    lst_key_mp1 = om.keySet(mp1)
    d_dates = lt.size(lst_key_mp1)
    for key in lt.iterator(lst_key_mp1):
        dict_append = {}
        valor =  om.get(mp1,key)
        size = lt.size(valor['value']['lst_events'])
        dict_append["time"] = key
        dict_append["events"] = size
        d_events += size
        dict_append["details"] = []
        for y in lt.iterator(valor['value']['lst_events']):
                dict_new = {}
                dict_new["mag"] =  y["mag"]
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
                dict_append["details"].append(dict_new)
        dict_append["details"] =  tabulate(dict_append["details"], headers="keys", tablefmt="grid", showindex= False)
        lt.addLast(lista_tabla,dict_append)
    quk.sort(lista_tabla,compareDates_req1)    

    return lista_tabla,d_dates,d_events

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