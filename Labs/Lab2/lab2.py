import numpy as np
import tikzplotlib
import scipy
from fitter import Fitter
import pandas as pd
import random
import matplotlib.pyplot as plt
from typing import NewType


# Declaracion de variables globales y tipo de datos
file = 'arboles.csv'
global_bins = 30
dataframe = NewType("dataframe type", pd.DataFrame())


def cantidad_arboles(df: dataframe) -> None:
    """
    Asignación: 1
    Determina la cantidad de especies de arboles en
    el archivo arboles.csv y las lista en orden alfabetico
    param df: dataframe con los datos del archivo arboles.csv
    """
    # Ordena los datos segun la columna de nombres en orden alfabetico
    df.sort_values(by=['Nombre común'], inplace=True)
    # Se muestran los primeros y ultimos nombres para probar que se ordenaron
    print(df['Nombre común'][0:10])
    # Cuenta la cantidad total de elementos en la columna
    cantidad = df['Nombre común'].count()
    # Cuenta la cantidad de especies distintas de arboles
    especies_distintas = df['Nombre común'].nunique()
    # Guarda una lista con el nombre de cada especie unica
    nombre_especies = df['Nombre común'].unique()
    print(df['Nombre común'][cantidad-10:cantidad])
    print("cantidad de especies distintas: ", especies_distintas)
    print("Nombre de todas las especes: \n", nombre_especies)


def histograma_Arboles(df: dataframe, nombres: list) -> None:
    """
    Asignacion: 2
    Se elijen 10 arboles y se grafica un histograma de la distribucion
    del diametro
    param df: dataframe con los datos del archivo arboles.csv
    param nombres: lista con el nombre de los 10 arboles a los
    cuales queremos hacer el histograma
    """

    ''' ['Secuencia', 'Nombre común', 'Diámetro (cm)', 'Altura total (m)',
       'Altura comercial (m)', 'Volumen comercial (m3)',
       'Valor comercial aproximado (CRC)'] '''

    ''' Se puede usar esto para obtener los diametros del arbol[i]
      i = 0
    diametros = []

    for x in range(df['Nombre común'].count()):
        if(df['Nombre común'][x] == nombres[i]):
            diametros.append(df['Diámetro (cm)'][x])
            i+=1
    print(diametros)
    '''

    # para cada nombre en la lista de los 10 arboles
    for x in nombres:
        # nuevo_df: dataframe auxiliar con los datos de un solo tipo de arbol
        nuevo_df = df[df['Nombre común'] == x]
        # Se hace el histograma con 30 divisiones
        nuevo_df['Diámetro (cm)'].plot(kind='hist', bins=30)
        # Se da formato a los ejes y se muestra la figura
        plt.xlabel('Diametro (cm)')
        plt.ylabel('Frecuencia')
        plt.title('Histograma de {}'.format(x))
        plt.show()


def mejor_ajuste(df: dataframe, mis_arboles: list) -> tuple:
    """
    Asignacion: 3
    Determina los parametros de mejor ajuste de mis 2 arboles
    obtenidos con la funcion asignacion() y se grafica este modelo
    en conjunto con el histograma respectivo
    param df: dataframe con los datos del archivo arboles.csv
    param mis_arboles: lista con los arboles asignados con la funcion asign()
    """
    # para cada nombre en la lista con 2 arboles
    for x in mis_arboles:
        # nuevo_df: dataframe auxiliar con los datos de un solo tipo de arbol
        nuevo_df = df[df['Nombre común'] == x]
        # Se transforma de objeto series a un array de numpy
        data = np.array(nuevo_df['Diámetro (cm)'])
        # Se utiliza fitter para encontrar los parametros de mejor ajuste
        f = Fitter(data, distributions=['kappa3', 'skewnorm'])
        # Realizar el ajuste para las distribuciones seleccionadas
        f.fit()
        # Mostrar principales resultados y gráfica
        f.summary()
        parametros = f.fitted_param
        print(parametros, type(parametros))
        archivo = x+".tex"
        # Se da formato a los ejes y se muestra la figura
        plt.xlabel('Diametro (cm)')
        plt.ylabel('Frecuencia')
        plt.title('Histograma de {}'.format(x))
        # tikzplotlib.save(archivo) # Tira error
        plt.show()
    return parametros


def asignaciones(digitos):
    '''Función que asigna un árbol y una
    combinación de dos árboles a cada persona
    con base en los dígitos de su carné.
    '''
    arboles = pd.read_csv('arboles.csv')
    random.seed(digitos)
    lista = arboles['Nombre común'].unique()
    return (random.choice(lista), random.choices(lista, k=2))


# Llamada a funciones
digitos = 42629
mis_arboles = asignaciones(digitos)
arboles_asign3 = [mis_arboles[1][0], mis_arboles[1][1]]
print('Mis dos árboles son: {} y {}.'.format(arboles_asign3[0],
                                             arboles_asign3[1]))
print('Mi árbol es: {}.'.format(mis_arboles[0]))
arboles = pd.read_csv(file)
df = pd.DataFrame(arboles)
''' Asignacion 1'''
# cantidad_arboles(df)

''' Asignacion 2'''
Arboles_histo = ['guapinol', 'balsa', 'gallinazo', 'higuerón', 'malacahuite',
                 'mora', 'tamarindo', 'aceituno', 'laurel', 'guarumo']
# histograma_Arboles(df, Arboles_histo)

'''Asignacion 3'''
mejor_ajuste(df, arboles_asign3)
