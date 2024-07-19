# Equilibrium Optimizer (EO)

Repositorio de la implementación en Python del Equilibrium Optimizer para la asignatura de Optimización Computacional.

El Equilibrium Optimizer (EO) es un algoritmo de optimización metaheurístico inspirado en modelos de balance de masa de volumen de control utilizados para estimar estados dinámicos y de equilibrio. Cada partícula (solución) en el EO actúa como un agente de búsqueda que actualiza su concentración (posición) en relación con las mejores soluciones encontradas hasta el momento, conocidas como candidatos de equilibrio. El objetivo es alcanzar un estado de equilibrio que represente la solución óptima.

Esta implementación se hizo con un enfoque multi-objetivo para adaptarlo a problemas de optimización donde se tiene más de una funcion a maximizar o minimizar utilizando el método de Ɛ-Constraint.

## Sobre el optimizador

### Requerimientos:

Las dependencias necesarias para la ejecucion correcta de todos los archivos son las siguientes:
* `random`:
* `NumPy`:
* `Pandas`:
* `MatPlotLib`:
* `Rich`:
* `re`:

### Ejecucion de la implementacion

La implementación actual del algoritmo se encuentra en el archivo `equilibriumOptimizerV2.ipynb`.

Ejecutar en orden las celdas 

