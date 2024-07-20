import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Problema:
  def __init__(self, epsilon):
    self.epsilon = epsilon
    self.dimensiones = 5
    self.limites = {
      'x1': (0, 15),
      'x2': (0, 10),
      'x3': (0, 25),
      'x4': (0, 4),
      'x5': (0, 30)
    }

    self.costos = {
      'x1': 170,
      'x2': 310,
      'x3': 60,
      'x4': 101,
      'x5': 11
    }

    self.presMaxTv = 3800
    self.presMaxDyR = 2800
    self.presMaxDyR = 3500

  def check(self, x):
    # Chequeo de restricciones de presupuesto
    costo_tv = self.costos['x1'] * x[0] + self.costos['x2'] * x[1]
    costo_print = self.costos['x3'] * x[2] + self.costos['x4'] * x[3]
    costo_combined = self.costos['x3'] * x[2] + self.costos['x5'] * x[4]
        
    if costo_tv > self.presMaxTv:
      return False
    if costo_print > self.presMaxDyR:
      return False
    if costo_combined > self.presMaxDyR:
      return False

    # Chequeo de límites de cantidad de anuncios
    for i, (c_min, c_max) in enumerate(self.limites.values()):
      if not (c_min <= x[i] <= c_max):
        return False

    # Chequeo de epsilon-constraint
    totalCosto = 170 * x[0] + 310 * x[1] + 60 * x[2] + 101 * x[3] + 11 * x[4]
    if totalCosto > self.epsilon:
      return False

    return True
  
  def checkCostos(self, x):
    totalCosto = 170 * x[0] + 310 * x[1] + 60 * x[2] + 101 * x[3] + 11 * x[4]
    return totalCosto
  
  def checkQuality(self, x):
     totalQuality = 70 * x[0] + 91 * x[1] + 50 * x[2] + 61 * x[3] + 21 * x[4]
     return totalQuality

  def eval(self, x):
    # Se evalua el fitness
    return 70 * x[0] + 91 * x[1] + 50 * x[2] + 61 * x[3] + 21 * x[4]
  

  def sigmoide(self, x, alpha, x0):
    return 1/(1+np.exp(-alpha*(x-x0)))
  
  def find_y_interval(self, y, intervals):
    interval_width = 1 / intervals
    for i in range(intervals):
        if i * interval_width <= y < (i + 1) * interval_width:
            return i
    return intervals - 1 if y == 1 else None
  
  def master_sigmoide(self, arreglo):
    parameters = [
      (0.6, 7.5, 16),    
      (1, 5, 11),        
      (0.35, 12.5, 26),  
      (2.5, 2, 5),       
      (0.3, 15, 31)      
    ]
    
    results_list = []
    for x, (alpha, x0, intervals) in zip(arreglo, parameters):
        y = self.sigmoide(x, alpha, x0)
        if intervals == 5: 
            if 0 <= y < 0.2:
                results_list.append(0)
            elif 0.2 <= y < 0.4:
                results_list.append(1)
            elif 0.4 <= y < 0.6:
                results_list.append(2)
            elif 0.6 <= y < 0.8:
                results_list.append(3)
            elif 0.8 <= y <= 1:
                results_list.append(4)
            else:
                results_list.append(None)
        else:
            results_list.append(self.find_y_interval(y, intervals))
    
    return np.array(results_list)
  

class Particula:
  def __init__(self, problema):
    self.problema = problema
    self.x = np.zeros(problema.dimensiones)
    self.inicializacion()


  def inicializacion(self):
    for j in range(self.problema.dimensiones):
      c_min, c_max = list(self.problema.limites.values())[j]
      self.x[j] = (c_min + random.random() * (c_max - c_min))

  def esFactible(self, x):
    return self.problema.check(self.x)

  def esMejorQue(self, comp):
    return self.fit() > comp.fit()

  def fit(self):
    return self.problema.eval(self.x)

  def __str__(self):
    # Representación en cadena de la partícula
    return f"fit:{self.fit()} x:{self.x}"


class EquilibriumOptimizer2:
    def __init__(self, problema, n, MAX_ITER, a1, a2, GP):
        self.problema = problema
        self.nParticulas = n
        self.maxIter = MAX_ITER
        self.a1 = a1
        self.a2 = a2
        self.GP = GP
        self.V = 1
        self.enjambre = []
        self.eq_candidatos = [Particula(problema) for _ in range(4)]

        self.lower_band = [ self.problema.limites[f"x{i+1}"][0] for i in range( len( self.problema.limites.keys() ) ) ]
        self.upper_band = [ self.problema.limites[f"x{i+1}"][-1] for i in range( len( self.problema.limites.keys() ) ) ]


    def inicializarPoblacion(self):
        print("Creacion de particulas: \n")
        for _ in range(self.nParticulas):
            while True:
                particula = Particula(self.problema)
                particula.x = self.problema.master_sigmoide(particula.x)
                print(particula.x)
                if particula.esFactible(particula.x):
                    self.enjambre.append(particula)
                    break
    
    def updateCandidatosEq(self):
        for particula in self.enjambre:
            for i in range(len(self.eq_candidatos)):
                if particula.esMejorQue(self.eq_candidatos[i]):
                    self.eq_candidatos[i] = particula
                    break
                
    def construirEqPool(self):
        eqPromedio = Particula(self.problema)
        eqPromedio.x = np.mean([ candidato.x for candidato in self.eq_candidatos ], axis = 0).tolist()
        eqPromedio.x = self.problema.master_sigmoide(eqPromedio.x)
        return self.eq_candidatos + [ eqPromedio ]
    
    def evolucion(self):

        for iter in range(1, self.maxIter + 1):
            
            self.updateCandidatosEq()
            eq_pool = self.construirEqPool()

            # Calcular t segun Eq. (9)
            t = (1 - iter / self.maxIter) ** ( self.a2 * iter/self.maxIter )

            for particula in self.enjambre:

                while True:

                    eq_candidato = random.choice(eq_pool)                        # Eleccion randomica de un candidato del eq_pool
                    vectorLambda = np.random.rand(self.problema.dimensiones)     # Valor randomico del 0 al 1 para la Eq. (11)
                    vectorR = np.random.rand(self.problema.dimensiones)          # valor randomico del 0 al 1 para la Eq. (11)

                    # Eq. (11)
                    F = self.a1 * np.sign(vectorR - 0.5) * ( np.exp(-vectorLambda * t) - 1 )

                    # Eq. (15)
                    GCP = np.where( np.random.rand(self.problema.dimensiones) >= self.GP , 0.5 * random.random(), 0 )

                    # Eq. (14)
                    G0 = GCP * ( eq_candidato.x - vectorLambda * particula.x )

                    # Eq. (13)
                    G = G0 * F

                    # Eq. (16)
                    particula.x = eq_candidato.x + ( (particula.x - eq_candidato.x) * F )  + (G / vectorLambda) * (1 - F)

                    particula.x = self.problema.master_sigmoide(particula.x)

                    if (particula.esFactible(particula.x)):
                        break
    
    def solve(self):
        self.inicializarPoblacion()
        self.evolucion()
        self.updateCandidatosEq()
        mejoresParticulas = self.eq_candidatos
        print("\n\nMejores particulas: ")
        for particula in mejoresParticulas:
            print(particula)

n = 30
maxIter = 5
a1 = 2
a2 = 1
GP = 0.5
epsilon = 3000
problema = Problema(epsilon)
optimizer = EquilibriumOptimizer2(problema, n, maxIter, a1, a2, GP)
optimizer.solve()