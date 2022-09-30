'''
IE0405 - MPSS

Descripción de una variable aleatoria
con las herramientas de scipy.stats

>>> Instalar tikzplotlib

$ pip install tikzplotlib

A todas las figuras generadas por
tikzplotlib (PDF.tex, CDF.tex, etc.)
se debe agregar manualmente:

\begin{axis}[
width=\columnwidth,	     <-- esto
height=0.6\columnwidth,  <-- y esto
'''

import numpy as np
from scipy.stats import expon, skew, kurtosis
import matplotlib.pyplot as plt
import tikzplotlib

# ¿Qué hacer?: 'ver' o 'guardar' las figuras
hacer = input('¿Desea ver las gráficas o guardar como Tikz? (ver/guardar): ')
print('¡Bueno, vamos a {}!'.format(hacer))

# Función para ver o guardar la figura
def figura(hacer, archivo):
	if hacer == 'guardar':
		tikzplotlib.save(archivo)

# Estilo de las gráficas
#plt.style.use('./mpss.mplstyle')

# Parámetros (¡elección arbitraria!, pero sensata)
lambd = 1

# Los parámetros de scipy.stats
loc = 0
scale = 1/lambd

# Variable aleatoria
va = expon(loc, scale)

# Límites y soporte en X
inf = va.ppf(0.01)
sup = va.ppf(0.99)
x = np.linspace(inf, sup, 60)

# ----
# Función de densidad de probabilidad
# ----

# PDF con distintos parámetros
plt.figure()
for i in [0.5, 1, 1.5]:
	plt.plot(x, expon(0, 1/i).pdf(x), label='$\lambda = {:0.2f}$'.format(i))
# Información de la gráfica
plt.xlabel('$x$')
plt.ylabel('$f_X(x)$')
plt.legend()

plt.savefig('PDF.svg', transparent=True)
# Visualizar o guardar como TikZ
figura(hacer, 'PDF.tex')

# ----
# Función acumulativa de probabilidad
# ----

# CDF junto a la SF
plt.figure()
plt.plot(x, va.cdf(x), label='$F_X(x)$')
plt.plot(x, va.sf(x), label='$S_X(x)$')

# Información de la gráfica
plt.xlabel('$x$')
plt.ylabel('Probabilidad')
plt.legend()

# Visualizar o guardar como TikZ
figura(hacer, 'CDF.tex')

# PPF junto a la ISF
plt.figure()
p = np.linspace(0, 1, 60)
plt.plot(p, va.ppf(p), label='$Q_X(p)$')
plt.plot(p, va.isf(p), label='$S_X^{-1}(p)$')

# Información de la gráfica
plt.xlabel('$p$')
plt.ylabel('$x$')
plt.legend()

# Visualizar o guardar como TikZ
figura(hacer, 'PPF.tex')

# ----
# Ejemplo de datos aleatorios
# ----

# Datos aleatorios
datos = va.rvs(500)

# Parámetros de ajuste
parametros = expon.fit(datos)
print('\nParámetros de modelo de ajuste: \n')
print('loc = {:0.4f}, \nscale = {:0.4f}'.format(parametros[0], parametros[1]))

# Datos aleatorios y curva de ajuste
plt.figure()
plt.hist(datos, 20, density=True, label='Datos aleatorios')
plt.plot(x, expon.pdf(x, parametros[0], parametros[1]), label='Modelo')

# Información de la gráfica
plt.xlabel('$x$')
plt.ylabel('$f_X(x)$')
plt.legend()

# Visualizar o guardar como TikZ
figura(hacer, 'histograma.tex')

# ----
# Cálculo de momentos
# ----

# Media del modelo
media = va.mean()

# Media de los datos
media_d = np.mean(datos)

# Varianza del modelo
varianza = va.var()

# Varianza de los datos
varianza_d = np.var(datos)

# Desviación estándar del modelo
desviacion = va.std()

# Varianza de los datos
desviacion_d = np.std(datos)

# Inclinación del modelo
inclinacion = va.stats(moments='s')

# Inclinación de los datos
inclinacion_d = skew(datos)

# Kurtosis del modelo
curtosis = va.stats(moments='k')

# Kurtosis de los datos
curtosis_d = kurtosis(datos)

# Imprimir resumen de datos
print('\nPrincipales momentos: \n')
print('Media (modelo): {:0.4f}'.format(media))
print('Media (datos): {:0.4f}'.format(media_d))
print('Varianza (modelo): {:0.4f}'.format(varianza))
print('Varianza (datos): {:0.4f}'.format(varianza_d))
print('Desviación estándar (modelo): {:0.4f}'.format(desviacion))
print('Desviación estándar (datos): {:0.4f}'.format(desviacion_d))
print('Inclinación (modelo): {:0.4f}'.format(inclinacion))
print('Inclinación (datos): {:0.4f}'.format(inclinacion_d))
print('Kurtosis (modelo): {:0.4f}'.format(curtosis))
print('Kurtosis (datos): {:0.4f}'.format(curtosis_d))

# Mostrar las figuras
if hacer == 'ver':
	plt.show()

# Deben cerrarse todas las ventanas de figuras para volver
# a ejecutar el código.