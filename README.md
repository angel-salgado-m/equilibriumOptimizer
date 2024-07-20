# Equilibrium Optimizer (EO)

Repositorio de la implementación en Python del Equilibrium Optimizer para la asignatura de Optimización Computacional.

El Equilibrium Optimizer (EO) es un algoritmo de optimización metaheurístico inspirado en modelos de balance de masa de volumen de control utilizados para estimar estados dinámicos y de equilibrio. Cada partícula (solución) en el EO actúa como un agente de búsqueda que actualiza su concentración (posición) en relación con las mejores soluciones encontradas hasta el momento, conocidas como candidatos de equilibrio. El objetivo es alcanzar un estado de equilibrio que represente la solución óptima.

Esta implementación se hizo con un enfoque multi-objetivo para adaptarlo a problemas de optimización donde se tiene más de una funcion a maximizar o minimizar utilizando el método de Ɛ-Constraint.

## Sobre el optimizador

### Requerimientos:

Las dependencias necesarias para la ejecución correcta de todos los archivos son las siguientes:
* `random`: Para generar opciones aleatorias y numeros aleatorios.
* `NumPy`: Para manejo de numeros y distintos arrays.
* `Pandas`: Para el manejo de datos y archivos `.csv`.
* `MatPlotLib`: Para la graficación de los datos
* `Rich`: Para personalizar la salida de los datos.
* `re`: Para un mejor manejo de los archivos de salida.

### Ejecución de la implementación

La implementación actual del algoritmo se encuentra en el archivo `equilibriumOptimizerV2.ipynb`.

Ejecutar en orden las celdas, y ajustar parámetros para experimentar y/o replicar las ejecuciones.

___

Tambien se encuentra el archivo `equilibrium.py`, el cual contiene el código base de la implementación, con valores ya definidos y sin codigo de Nodo-Arco Consistencia ni análisis de datos.

Los parámetros que se pueden cambiar son:
* `a2`: Factor que afecta a la exploracion. Se tiene un valor fijo de 2
* `a1`: Factor que afecta a la explotacion. Se tiene un valor fijo de 1
* `GP`: Factor que equilibra la exploracion y explotacion. Valor fijo de 0.5
* `maxIter`: Numero maximo de iteraciones
* `n`: Cantidad de particulas a generar
* `epsilon`: para el epsilon-constraint. Refleja el valor maximo del presupuesto.


## Integrantes:
* Ignacio Salinas
* Angel Salgado