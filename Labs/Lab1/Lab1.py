import csv
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


'''def Relative_freq(filepath: str) -> list:
    """
    Asignacion: 1
    Calcula las frecuencias relativas en el archivo.csv
    param filepath: direccion del archivo.csv
    return: Una lista con la frecuencia relativa de compra
    """
    relative_frequencies = []
    a_count, b_count, c_count, d_count = 0, 0, 0, 0
    a, b, c, d = 0, 0, 0, 0
    total = 0
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            elements = row[0].split(',')
            # ignore first line
            if (elements[0] == "Cliente"):
                pass
            else:
                # print('linea: {} A: {}'.format(elements[0],elements[1]))
                a, b = int(elements[1]), int(elements[2])
                c, d = int(elements[3]), int(elements[4])
                total += 1
                if (a):
                    a_count += 1
                if (b):
                    b_count += 1
                if (c):
                    c_count += 1
                if (d):
                    d_count += 1
                # print('count A = {} B = {}'.format(a_count, b_count))
    relative_frequencies.append(a_count/total)
    relative_frequencies.append(b_count/total)
    relative_frequencies.append(c_count/total)
    relative_frequencies.append(d_count/total)
    print(relative_frequencies)
    return relative_frequencies'''


def bar_graph(cantidad_compras: list) -> None:
    """
    Asignacion: 2
    Realiza un grafico de barras a partir de una lista
    de frecuencias relativas
    param cantidad_compras: lista con la cantidad de compras por producto
    """
    # Agrega la lista de frecuencias relativas y los índices al dataframe
    index = ['A', 'B', 'C', 'D']
    plt.bar(index, cantidad_compras)
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
    # Se calcula la frecuencia de aparicion de cada elemento
    # Utilizando la funcion value_counts
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
    cantidad_compras = [a_count[1], b_count[1], c_count[1], d_count[1]]
    print(cantidad_compras)
    # Las frecuencias relativas se reciben como un arreglo
    # a_relative_f[0] contiene la frecuencia relativa de la no compra(0)
    # a_relative_f[1] contiene la frecuencia relativa de la compra (1)
    relative_frequencies = \
        [a_relative_f[1], b_relative_f[1], c_relative_f[1], d_relative_f[1]]
    return cantidad_compras


def combination_relative_freq(filepath: str) -> list:
    """
    Asignacion: 3
    Calcula las frecuencias relativas de cada combinacion de 
    compra por cliente
    """
    # Cantidad de combinaciones
    combinations = 16
    # Lista con la cantidad de apariciones de cada combinacion
    frecuencias = [0]*combinations
    
    # Numeros enteros con la combinacion de productos comprados
    a, b, c, d = 0, 0, 0, 0
    # Num es un numero pensado en binario para indicar la combinacion
    # donde A es el bit mas significativo y B el menos significativo
    num = 0
    # total es la cantidad de personas que compraron los productos
    total = 0
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            elements = row[0].split(',')
            # ignore first line
            if (elements[0] == "Cliente"):
                pass
            else:
                # print('linea: {} A: {}'.format(elements[0],elements[1]))
                a, b = int(elements[1]), int(elements[2])
                c, d = int(elements[3]), int(elements[4])
                total+=1
                num = d + 2*c + 4*b + 8*a
                frecuencias[num]+=1
        for i in range(len(frecuencias)):
            frecuencias[i]/=total
    print(combinations)
    print(frecuencias)


#cantidad_compras = relative_freq()
#bar_graph(cantidad_compras)
combination_relative_freq('compras.csv')

