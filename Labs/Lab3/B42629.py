'''
Universidad de Costa Rica
Escuela de Ingeniería Eléctrica
IE0405 - MPSS
2022 - II

Proyecto 3

Dualok Fonseca Monge
B42629

Análisis de datos de demanda eléctrica del país
-----------------------------------------------

[Incluir aquí una explicación de lo que hace el script.]

Recomendaciones [¡borrar luego!]:

- La elección de nombres de variables y funciones
apropiados es, en sí, un esfuerzo de documentación.
	- Ejemplo de nombres de variables apropiados:
		No: V = 120
		Sí: tension_ac = 120
	- Ejemplo de nombres de funciones apropiados:
		No: def h(x, y):
		Sí: def hipotenusa(cat_1, cat_2):

- Es buena práctica habilitar un autocorrector de
PEP8 en el IDE. Por ejemplo, en Sublime el comando
CTRL + SHIFT + 8 hace la corrección automática. En
VS Code es CTRL + SHIFT + F, etc. (es necesario
instalar los paquetes correspondientes).

- El estricto apego a un estilo de docstrings (Google
Style, NumPy Style, ReST, etc.) permite generar 
documentación automáticamente en la forma de páginas web
o archivos PDF, usando herramientas como Sphinx (no será
realizado en este proyecto).

'''
import numpy as np
import scipy
from fitter import Fitter
import pandas as pd
import random
import matplotlib.pyplot as plt
from typing import NewType
import requests
import json


# Declaracion de variables globales y tipo de datos
file = 'arboles.csv'
# Se define un nuevo tipo de datos
dataframe = NewType("dataframe type", pd.DataFrame())

# Funcion que importa los datos de demanda MW directamente desde el API del CENCE en formato JSON
def datos_demanda(fecha_inicio: int, fecha_fin: int) -> dataframe:
	'''
	Esta funcion sirve para generar un archivo en formato json a partir de los datos
	obtenidos del CENCE de los MW por hora consumidos en Costa Rica haciendo un request al
	API que expone el CENCE y utilizando las librerias request y json

	Parameters
    ----------
    fecha_inicio : int
    fecha_fin : int

	Return
	------
	df : dataframe
		Un dataframe con los datos json obtenidos mediante el request
	'''

	# Crea el url de acceso a la base de datos del CENCE
	api_url = "https://apps.grupoice.com/CenceWeb/data/sen/json/DemandaMW?inicio=" + str(fecha_inicio) + "&fin=" + str(fecha_fin)
	requested_data = requests.get(api_url)
	requested_data = requested_data.json()
	json_string = json.dumps(requested_data)
	json_file = open("data.json", "w")
	json_file.write(json_string)
	json_file.close()
	json_data = json.load(open('data.json'))
	df = pd.DataFrame(json_data["data"])
	print(df)
	return df


# funcion que obtiene los datos de consumo de potencia de una hora particular (0 - 24) a lo largo de todo el período de días disponible	
def datos_hora(hora):
	#hace algo lol
	print("dh")

def asignacion_horas(digitos):
    '''Elige una hora A en periodo punta
    y una hora B de los otros periodos,
    con los dígitos del carné como "seed"
    '''
    
    random.seed(digitos)
    punta = [11, 12, 18, 19, 20]
    valle = [7, 8, 9, 10, 13, 14, 15, 16, 17]
    nocturno = [21, 22, 23, 0, 1, 2, 3, 4, 5, 6]
    otro = valle + nocturno
    hora_A = random.choice(punta)
    hora_B = random.choice(otro)
    return hora_A, hora_B


# Programa principal que llama al resto de metodos ordenadamente
def main():
	fecha_inicio = 20190101 	#input("Fecha inicio (YYYYMMDD): ")
	fecha_fin = 20200101 		#input("Fecha final (YYYYMMDD): ")
	digitos_carne = 42629 		#input("¿Cuáles son los dígitos del carné?: ")
	horas = asignacion_horas(42629)
	print(f'Las horas asignadas son {horas[0]} y {horas[1]}.')
	df = datos_demanda(fecha_inicio, fecha_fin)
	

main()
	
	

