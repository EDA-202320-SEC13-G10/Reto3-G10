"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import folium as fol
from tabulate import tabulate
import traceback
import requests
import webbrowser

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    pass


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    return controller.load_data(control,"earthquakes//temblores-utf8-small.csv")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("Req No. 1 Input".center(130,"="))

    initialDate =  input("Start date: ")
    finalDate =  input("End date: ")

    

    initialDate = "1999-03-21T05:00"
    finalDate = "2004-10-23T17:30"
    l1,l2,l3,foliumsLista= controller.req_1(control,initialDate,finalDate)
    print("Req No. 1 Results".center(130,"="))
    print(("Total different dates: " +str(l3)))
    print(("Total events between dates: " +str(l2)))

    # TODO: Imprimir el resultado del requerimiento 1
    if l3 > 6:
        print("Consults size: "+ str(l3) +" Only first and last '3' results are:")
    else:
        print("Consults size: "+ str(l3))
 
    print(tabulate(lt.iterator(l1),headers="keys", tablefmt = "grid", showindex=False))
    m = fol.Map(tiles="cartodbpositron")

    geojson_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
).json()
    fol.GeoJson(geojson_data, name="hello world").add_to(m)

    fol.LayerControl().add_to(m)

    for i in (foliumsLista):
            fol.Marker(
                location=i,
                icon=fol.Icon(icon="cloud"),
            ).add_to(m)
    m.save("footprint.html")
    webbrowser.open("footprint.html")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("Req No. 2 Input".center(130,"="))
    mag_i =  float(input("Magnitud inicial: "))
    mag_f =  float(input("Magnitud final: "))
    print("Req No. 2 Results".center(130,"="))
    l1,l2,l3= controller.req_2(control,mag_i,mag_f)

    print(("Total different magnitudes: " +str(l2)))
    print(("Total events between magnitudes: " +str(l3)))
    print("Consults has "+ "'"+str(l2)+"'"+" results")
    if l3 > 6:
        
        print("Consults size: "+ str(l2) +" Only first and last '3' results are:")
    else:
        print("Consults size: "+ str(l2))
    print(tabulate(lt.iterator(l1),headers="keys", tablefmt = "grid", showindex=False))

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control, sig_min, gap_max):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    cant, sig_y_max = controller.req_4(control, sig_min, gap_max)
    print(cant)
    # print(tabulate(lt.iterator(sig_y_max),headers="keys", tablefmt = "grid", showindex=False))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    print("Req No. 6 Input".center(130,"="))
    anio =  (input("Año: "))
    lat =  (input("lat: "))
    long =  (input("long: "))
    radio =  float(input("Radio: "))
    n =  int(input("Numero de sismos cercanos: "))

    print("Req No. 6 Results".center(130,"="))
    l1,l2,l3= controller.req_6(control,anio,lat,long,radio,n)

    print("Terremotos totales en el area para el año "+ str(anio)+": " +str(l3))
    print("Terremoto mas significativo")
    print(tabulate(l1,headers="keys", tablefmt = "grid", showindex=False))
    print("Los 5 terremotos mas proximos cronologicamente")
    print(print(tabulate(lt.iterator(l2),headers="keys", tablefmt = "grid", showindex=False)))


def print_req_7(control, year, area, prop, bi):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    cant_year, cant_hist, min_value, max_value, hist_list = controller.req_7(control, year, area, prop, bi)
    print(cant_year)
    print(cant_hist)
    print(min_value)
    print(max_value)
    print(tabulate(lt.iterator(hist_list),headers="keys", tablefmt = "grid", showindex=False))

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = controller.new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            print("".center(100,"-"))
            print("eartquake event size: " + str(lt.size(data["datos_lobby"])))
            print("".center(100,"-"))
            print("\n")
            print("".center(100,"="))
            print("EARTHQUAKE RECORDS REPORT")
            print("".center(100,"="))
            print("Printing the first 5 and last 5 records...\n")
            z = controller.primernos_fiuankes(data["mag_lobby"])
            print(tabulate(lt.iterator(z),headers="keys", tablefmt = "grid", showindex=False))
        elif int(inputs) == 2:
            print_req_1(control)


        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control, 300, 45)

        elif int(inputs) == 6:
            print_req_5(control, 23, 38)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control, 2020, "Alaska", "mag", 10)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
