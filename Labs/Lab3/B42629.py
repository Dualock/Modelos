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

	#verifica si el archivo ya se ha creado anteriormente
	try:

		# Si el archivo existe, se usa para crear el dataframe
		print("Creando dataframe a partir del json")

		# Se abre guardan los datos del archivo en formato json
		json_data = json.load(open('data.json'))

		# Se convierte de json a dataframe los datos
		df = pd.DataFrame(json_data["data"])
		return df
	except IOError:

		# Si el archivo no existe lo creamos al procesar esta excepcion
		# Crea el url de acceso a la base de datos del CENCE utilizando las fechas de inicio y final
		print("el archivo json no existe, se crea accediendo al API")
		api_url = "https://apps.grupoice.com/CenceWeb/data/sen/json/DemandaMW?inicio=" + str(fecha_inicio) + "&fin=" + str(fecha_fin)

		# Se realiza la obtencion de los datos con request.get
		requested_data = requests.get(api_url)

		# Se obtiene el request_data en formato json
		requested_data = requested_data.json()

		# Se convierte a string para escribir en el archivo.json
		json_string = json.dumps(requested_data)

		# Se abre el archivo y se escribe en el
		json_file = open("data.json", "w")
		json_file.write(json_string)
		json_file.close()

		# Se abre guardan los datos del archivo en formato json 
		json_data = json.load(open('data.json'))

		# Se convierte de json a dataframe los datos
		df = pd.DataFrame(json_data["data"])
		return df
	


# funcion que obtiene los datos de consumo de potencia de una hora particular (0 - 24) a lo largo de todo el período de días disponible	
def datos_hora(hora: int, df: dataframe) -> dataframe:
	'''
	Esta funcion crea un dataframe con todos los datos de consumo
	de potencia para una hora especifica a partir del dataframe 
	completo para todas las horas en un periodo establecido
		Parameters
    ----------
    hora : int
    df : dataframe

	Return
	------
	df_hora_asignacion : dataframe
		Un dataframe con los datos de consumo de potencia de una hora
		especifica durante todo el año
	'''

	# Se convierte de dataframe a list
	fechas_horas = df['fechaHora'].values.tolist()

	'''fechas_horas_filtradas es una lista que almacena todas las fechas y horas
	del año donde la hora coincide con una hora especifica
	'''
	fechas_horas_filtradas = []

	# Se itera y se almacenan las fechas y horas coincidentes
	for i in range(len(fechas_horas)):
		if(fechas_horas[i][11:13] == str(hora)):
			fechas_horas_filtradas.append(fechas_horas[i])
	
	''' Ahora se crea un nuevo data frame con condicion de estar en la 
	lista de fechas y horas filtradas anteriormente
	'''
	df_hora_asignacion = df[df['fechaHora'].isin(fechas_horas_filtradas)]
	#print(df_hora_asignacion)
	return df_hora_asignacion


# Funcion que obtiene el modelo probabilistico y parametros de mejor ajuste
def modelo_hora(df_hora_asignacion: dataframe) -> list:
	'''
	Esta funcion determina un modelo probabilistico para una hora especifica
	y sus parametros de mejor ajuste
	Parameters
    ----------
    df_hora_asignacion : dataframe
		Un dataframe con los datos de consumo de potencia de una hora
		especifica durante todo el año

	Return
	------
	modelo_y_parametros: list
		lista con el nombre del modelo probabilistico 
		y los parametros de mejor ajuste
		
	'''

	modelo_y_parametros = []
	# Se convierte de dataframe a numpy array
	data = np.array(df_hora_asignacion['MW_P'])

    # Se utiliza fitter para encontrar los parametros de mejor ajuste
	f = Fitter(data)

    # Realizar el ajuste para las distribuciones seleccionadas
	f.fit()

	# Obtenemos el modelo de mejor ajuste como un diccionario y nos dejamos el nombre
	# mejor_modelo como llaves del diccionario
	mejor_modelo = f.get_best(method = 'sumsquare_error').keys()

	# Mejor modelo como lista
	mejor_modelo = list(mejor_modelo)

	# Se agrega el nombre del modelo a la lista final
	modelo_y_parametros.append(mejor_modelo[0])

    # Mostrar principales resultados y gráfica
	f.summary()
	parametros = f.fitted_param[mejor_modelo[0]]
	for i in range(len(parametros)):
		modelo_y_parametros.append(parametros[i])
	return modelo_y_parametros

def estadisticas_hora(df_hora_asignacion: dataframe):
	'''
	Esta funcion determina los momentos de una variable aleatoria
	media, varianza, desviacion estandar, inclinacion y kurtosis,
    ----------
    df_hora_asignacion : dataframe
		Un dataframe con los datos de consumo de potencia de una hora
		especifica durante todo el año

	Return
	------
	modelo_y_parametros: list
		lista con el nombre del modelo probabilistico 
		y los parametros de mejor ajuste
	'''

	# Calculo de media
	media = df_hora_asignacion['MW_P'].mean()
	desviacion = df_hora_asignacion['MW_P'].std()
	varianza = df_hora_asignacion['MW_P'].var()
	inclinacion = df_hora_asignacion['MW_P'].skew()
	kurtosis = df_hora_asignacion['MW_P'].kurtosis()
	print("Sus estadísticas son: \n - media: {}".format(media))
	print(" - desviación: {} \n - varianza: {}".format(desviacion, varianza))
	print("- inclinación:{} \n - kurtosis:{}".format(inclinacion, kurtosis))



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
	df_asignacion_hora0 = datos_hora(horas[0], df)
	modelo_y_parametros = modelo_hora(df_asignacion_hora0)
	final_de_lista = len(modelo_y_parametros)
	print("\nEl modelo de distribución de consumo de potencia para las {} horas".format(horas[0]))
	print("es {} con parámetros {}".format(modelo_y_parametros[0], 
	 								modelo_y_parametros[1:final_de_lista]))							
	estadisticas_hora(df_asignacion_hora0)
	

main()
	
	

