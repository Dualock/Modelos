import csv
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


def bar_graph(purchase_amount: list) -> None:
    """
    Asignación: 2
    Realiza un gráfico de barras a partir de una lista
    de frecuencias relativas
    param purchase_amout: lista con la cantidad de compras por producto
    """
    # Agrega la lista de frecuencias relativas y los índices a la figura
    index = ['A', 'B', 'C', 'D']
    plt.bar(index, purchase_amount)
    plt.title("Compras por producto")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad de compras")
    # Se muestra la figura graficada
    plt.show()


def relative_freq() -> list:
    """
    Asignacion: 1
    Calcula las frecuencias relativas en el archivo.csv
    return: Una lista con las cantidad de compras por producto
    """
    # Se leen los datos del archivo.csv con la funcion de pandas read_csv
    # Se guardan los datos en la variable data
    data = pd.read_csv(r'compras.csv')
    # Se crea un objeto tipo DataFrame de pandas para cada columna
    data_frame_a = pd.DataFrame(data, columns=['A'])
    data_frame_b = pd.DataFrame(data, columns=['B'])
    data_frame_c = pd.DataFrame(data, columns=['C'])
    data_frame_d = pd.DataFrame(data, columns=['D'])
    '''Se calcula la frecuencia de aparición de cada elemento
    utilizando la función value_counts'''
    # Se usa sort = false para no ordenarlos por cantidad de apariciones
    # Se utiliza normalize para calcular la frecuencia relativa directamente
    a_relative_f = data_frame_a['A'].value_counts(normalize=True, sort=False)
    b_relative_f = data_frame_b['B'].value_counts(normalize=True, sort=False)
    c_relative_f = data_frame_c['C'].value_counts(normalize=True, sort=False)
    d_relative_f = data_frame_d['D'].value_counts(normalize=True, sort=False)
    a_count = data_frame_a['A'].value_counts(sort=False)
    b_count = data_frame_b['B'].value_counts(sort=False)
    c_count = data_frame_c['C'].value_counts(sort=False)
    d_count = data_frame_d['D'].value_counts(sort=False)
    purchase_amount = [a_count[1], b_count[1], c_count[1], d_count[1]]
    # Las frecuencias relativas se reciben como un arreglo
    # a_relative_f[0] contiene la frecuencia relativa de la no compra(0)
    # a_relative_f[1] contiene la frecuencia relativa de la compra (1)
    relative_frequencies = \
        [a_relative_f[1], b_relative_f[1], c_relative_f[1], d_relative_f[1]]
    print("Frecuencias relativas - A: {} B: {} C: {} D: {}"
          .format(relative_frequencies[0], relative_frequencies[1],
                  relative_frequencies[2], relative_frequencies[3]))
    return purchase_amount


def combination_relative_freq(filepath: str) -> list:
    """
    Asignación: 3
    Calcula las frecuencias relativas de cada combinación de
    compra por cliente
    """
    # Cantidad de combinaciones
    combinations = 16
    # Lista con la cantidad de apariciones de cada combinación
    frequencies = [0]*combinations
    # Números enteros con la combinación de productos comprados
    producto_a, producto_b, producto_c, producto_d = 0, 0, 0, 0
    '''Num es un número para indicar la combinación
    donde A es el bit mas significativo y D el menos significativo'''
    num = 0
    # total es la cantidad de personas que compraron los productos
    total = 0
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # Se lee cada fila en el csv
        for row in reader:
            # se separan los elementos por ','
            elements = row[0].split(',')
            # ignoramos la primer línea
            if (elements[0] == "Cliente"):
                pass
            else:
                producto_a, producto_b = int(elements[1]), int(elements[2])
                producto_c, producto_d = int(elements[3]), int(elements[4])
                total += 1  # Se aumenta el total de elementos
                # Se opera sobre los productos como con un número binario
                num = producto_d + 2*producto_c + 4*producto_b + 8*producto_a
                # Se aumenta la frecuencia de esa combinación
                frequencies[num] += 1
    for i in range(len(frequencies)):
        frequencies[i] /= total
    print(frequencies)
    return frequencies


def combination_bar_graph(combination_frequencies: list) -> None:
    """
    Asignación: 4
    Realiza un gráfico de barras a partir de una lista
    de frecuencias relativas
    param cantidad_compras: lista con la cantidad de compras por producto
    """
    titulo = "Frecuencia relativa de la combinación de productos comprados"
    # Se crean los indices de combinaciones
    index = ['Nothing', 'D', 'C', 'CD', 'B', 'BD', 'BC', 'BCD',
             'A', 'AD', 'AC', 'ACD', 'AB', 'ABD', 'ABC', 'ABCD']
    ''' Agrega la lista de frecuencias relativas de ocurrencia de cada
    combinación y los ídices al data frame '''
    df = pd.DataFrame({'Frecuencia de ocurrencia por combinación':
                       combination_frequencies}, index=index)
    ax = df.plot.barh()
    # Se agrega la rotulacion de los ejes y se muestra la figura
    ax.set_title(titulo)
    ax.set_xlabel("Frecuencia relativa")
    ax.set_ylabel("Combinaciones")
    plt.show()


# Se llaman las funciones
purchase_amount = relative_freq()
bar_graph(purchase_amount)
combination_frequencies = combination_relative_freq('compras.csv')
combination_bar_graph(combination_frequencies)
