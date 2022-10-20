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

[Este programa tiene como finalidad introducir al estudiante en
temas relacionados con variable aleatoria múltiple, donde se utilizan
datos obtenidos del CENCE por medio del API expuesto y mediante
librerías de análisis de datos como scipy, numpy, pandas.
Se van a crear dataframes con los datos de consumo de potencia
en 2 horas específicas en Costa Rica, se van a calcular el modelo
y parámetros de mejor ajuste, así como hacer histogramas univariables y
bivariables, se calculara el coeficiente de correlación entre
ambas horas dadas.]


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


# Declaración de variables globales y tipo de datos
file = 'arboles.csv'
# Se define un nuevo tipo de datos
dataframe = NewType("dataframe type", pd.DataFrame())


def datos_demanda(fecha_inicio: int, fecha_fin: int) -> dataframe:
    '''
    Esta función sirve para generar un archivo en formato json a partir
    de los datos obtenidos del CENCE de los MW por hora consumidos en Costa Rica,
    haciendo un request al API que expone el CENCE y utilizando las
    librerías request y json

    Parameters
----------
fecha_inicio : int
fecha_fin : int

    Return
    ------
    df : dataframe
            Un dataframe con los datos json obtenidos mediante el request
    '''

    # verifica si el archivo ya se ha creado anteriormente
    try:

        # Si el archivo existe, se usa para crear el dataframe
        print("Creando dataframe a partir del json")

        # Se abre guardan los datos del archivo en formato json
        json_data = json.load(open('data.json'))

        # Se convierte de json a dataframe los datos
        df = pd.DataFrame(json_data["data"])
        return df
    except IOError:

        # Si el archivo no existe lo creamos al procesar esta excepción
        # Crea el url de acceso a la base de datos del CENCE utilizando las
        # fechas de inicio y final
        print("el archivo json no existe, se crea accediendo al API")
        api_url = "https://apps.grupoice.com/CenceWeb/data/sen/json/DemandaMW?inicio="
        api_url = api_url + str(fecha_inicio) + "&fin=" + str(fecha_fin)

        # Se realiza la obtención de los datos con request.get
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
	del año donde la hora coincide con una hora específica
	'''

    # lista con las fechas y horas del año coincidentes con la hora parámetro
    fechas_horas_filtradas = []

    # Se transforma de int a str y se calcula el número de dígitos
    hora_str = str(hora)
    digitos_hora = len(hora_str)

    # Si el número es de un solo dígito le agrega un 0 antes
    if (digitos_hora == 1):
        hora_str = '0' + hora_str

    # Se itera y se almacenan las fechas y horas coincidentes
    for i in range(len(fechas_horas)):
        if (fechas_horas[i][11:13] == hora_str):
            fechas_horas_filtradas.append(fechas_horas[i])

    ''' Ahora se crea un nuevo data frame con condición de estar en la
	lista de fechas y horas filtradas anteriormente
	'''
    df_hora_asignacion = df[df['fechaHora'].isin(fechas_horas_filtradas)]
    return df_hora_asignacion


# Función que obtiene el modelo probabílistico y parámetros de mejor ajuste
def modelo_hora(df_hora_asignacion: dataframe) -> list:
    '''
    Esta función determina un modelo probabilístico para una hora específica
        y sus parámetros de mejor ajuste
        Parameters
        ----------
        df_hora_asignacion : dataframe
                Un dataframe con los datos de consumo de potencia de una hora
                específica durante todo el año

        Return
        ------
        modelo_y_parametros: list
                lista con el nombre del modelo probabilístico
                y los parámetros de mejor ajuste

    '''

    modelo_y_parametros = []

    # Se convierte de dataframe a numpy array
    data = np.array(df_hora_asignacion['MW_P'])

# Se utiliza fitter para encontrar los parámetros de mejor ajuste
    f = Fitter(data, distributions=['loggamma'])

# Realizar el ajuste para las distribuciones seleccionadas
    f.fit()

    # Obtenemos el modelo de mejor ajuste como un diccionario y nos dejamos el nombre
    # mejor_modelo como llaves del diccionario
    mejor_modelo = f.get_best(method='sumsquare_error').keys()

    # Mejor modelo como lista
    mejor_modelo = list(mejor_modelo)

    # Se agrega el nombre del modelo a la lista final
    modelo_y_parametros.append(mejor_modelo[0])

    parametros = f.fitted_param[mejor_modelo[0]]
    for i in range(len(parametros)):
        modelo_y_parametros.append(parametros[i])
    return modelo_y_parametros


def estadisticas_hora(df_hora_asignacion: dataframe) -> None:
    '''
    Esta función determina los momentos de una variable aleatoria
    media, varianza, desviación estándar, inclinación y kurtosis

    Parameters
----------
df_hora_asignacion : dataframe
            Un dataframe con los datos de consumo de potencia de una hora
            específica durante todo el año

    '''

    # Cálculo de media, desviación estándar, inclinación y kurtosis
    media = df_hora_asignacion['MW_P'].mean()
    desviacion = df_hora_asignacion['MW_P'].std()
    varianza = df_hora_asignacion['MW_P'].var()
    inclinacion = df_hora_asignacion['MW_P'].skew()
    kurtosis = df_hora_asignacion['MW_P'].kurtosis()
    print(" \n Sus estadísticas son: \n - media: {}".format(media))
    print(" - desviación: {} \n - varianza: {}".format(desviacion, varianza))
    print("- inclinación:{} \n - kurtosis:{}".format(inclinacion, kurtosis))


def visualizacion_hora(
        df_hora: dataframe,
        mejor_modelo: str,
        hora: int) -> None:
    '''
    Esta función determina visualiza el histograma junto al modelo de
    mejor ajuste del consumo de potencia en 1 hora específica durante todo
    el año

    Parameters
----------
df_hora_asignacion : dataframe
            Un dataframe con los datos de consumo de potencia de una hora
            específica durante todo el año
    mejor_modelo : str
    hora : int
    '''

    # Se convierte de dataframe a numpy array
    data = np.array(df_hora['MW_P'])
    print("\n La visualización de los datos se muestra en la siguiente figura")
# Se utiliza fitter para encontrar los parametros de mejor ajuste
    f = Fitter(data, distributions=['{}'.format(mejor_modelo)])

# Realizar el ajuste para las distribuciones seleccionadas
    f.fit()

    # Mostrar principales resultados y gráfica
    f.summary()

# Se da formato a los ejes y se muestra la figura
    plt.xlabel('Potencia consumida MWh')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de consumo de potencia a la hora {}'.format(hora))
    plt.show()


def correlacion_horas(df_hora1: dataframe, df_hora2: dataframe) -> float:
    '''
    Esta función calcula el coeficiente de correlación de pearson
    a partir de 2 dataframes de consumo de potencia a dos horas
    distintas

    Parameters
----------
df_hora1 : dataframe
            Un dataframe con los datos de consumo de potencia de una hora
            específica durante todo el año
    df_hora1 : dataframe
            Un dataframe con los datos de consumo de potencia de otra hora
            específica durante todo el año
    Return
    ------
    correlacion: float
            Índice de correlación de Pearson
    '''

    # Se convierte del dataframe 1 a numpy array
    data1 = np.array(df_hora1['MW_P'])

    # Se convierte del dataframe 2 a numpy array
    data2 = np.array(df_hora2['MW_P'])

    # Se calcula el coeficiente de correlación de Pearson
    correlacion = scipy.stats.pearsonr(data1, data2)[0]
    return correlacion


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


def visualizacion_horas(df_hora1: dataframe, df_hora2: dataframe) -> None:
    '''
Esta función visualiza el hsitograna bivariado de disrtibucion
    de potencia
a partir de 2 dataframes de consumo de potencia a dos horas
distintas

Parameters
----------
df_hora1 : dataframe
        Un dataframe con los datos de consumo de potencia de una hora
        específica durante todo el año
df_hora1 : dataframe
        Un dataframe con los datos de consumo de potencia de otra hora
        específica durante todo el año
    '''
    # Se convierte del dataframe 1 a numpy array
    data1 = np.array(df_hora1['MW_P'])

    # Se convierte del dataframe 2 a numpy array
    data2 = np.array(df_hora2['MW_P'])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    hist, xedges, yedges = np.histogram2d(data1, data2, bins=40)
    xpos, ypos = np.meshgrid(
        xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()
    #ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    plt.show()

# Programa principal que llama al resto de métodos ordenadamente


def main():
    fecha_inicio = 20190101  # input("Fecha inicio (YYYYMMDD): ")
    fecha_fin = 20200101  # input("Fecha final (YYYYMMDD): ")
    digitos_carne = 42629  # input("¿Cuáles son los dígitos del carné?: ")
    horas = asignacion_horas(digitos_carne)
    print(f'Las horas asignadas son {horas[0]} y {horas[1]}.')
    df = datos_demanda(fecha_inicio, fecha_fin)

    # Se obtienen los dataframe para cada hora
    df_asignacion_hora0 = datos_hora(horas[0], df)
    df_asignacion_hora1 = datos_hora(horas[1], df)

    # Se obtienen los párametros y modelo de mejor ajuste para x hora
    modelo_y_parametros = modelo_hora(df_asignacion_hora0)

    # número que indica el último dato de la lista
    final_de_lista = len(modelo_y_parametros)
    print(
        "\nEl modelo de distribución de consumo de potencia para las {} horas".format(
            horas[0]))
    print("es {} con parámetros {}".format(
        modelo_y_parametros[0], modelo_y_parametros[1:final_de_lista]))
    estadisticas_hora(df_asignacion_hora0)
    visualizacion_hora(df_asignacion_hora0, modelo_y_parametros[0], horas[0])
    correlacion = correlacion_horas(df_asignacion_hora0, df_asignacion_hora1)
    print("\n El índice de correlación de Pearson entre la distribución de")
    print("las {} y las {} horas es:p = {}."
          .format(horas[0], horas[1], correlacion))
    print("La visualización de los datos se muestra en la figura")
    visualizacion_horas(df_asignacion_hora0, df_asignacion_hora1)


main()
