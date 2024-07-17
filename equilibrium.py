import random
import numpy as np

class Problema:
  def __init__(self):
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

    return True

  def eval(self, x):
    # Se evalua el fitness uti
        return 70 * x[0] + 91 * x[1] + 50 * x[2] + 61 * x[3] + 21 * x[4]
  
  def sigmoideDim(self, x):
    a = 1 / (1 + np.exp(-8*x + 4))
    if a > 0.5:
        a = 1
    else:
        a = 0
    return a

  def sigmoideP(self, arr):
      result = np.zeros(self.dimensiones)
      for n in arr:
        aux = n - int(n)
        s = self.sigmoideDim(aux)
        n = int(n) + s
        result = np.append(result, n)
      return result


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
    # Codigo
    return self.problema.check(self.x)

  def esMejorQue(self, comp):
    # Codigo
    return self.fit() > comp.fit()

  def fit(self):
    # Codigo
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
        self.eq_candidatos = [Particula(problema) for _ in range(n)]

        self.lower_band = [ self.problema.limites[f"x{i+1}"][0] for i in range( len( self.problema.limites.keys() ) ) ]
        self.upper_band = [ self.problema.limites[f"x{i+1}"][-1] for i in range( len( self.problema.limites.keys() ) ) ]


    def inicializarPoblacion(self):
        for _ in range(self.nParticulas):
            while True:
                particula = Particula(self.problema)
                if particula.esFactible(particula.x):
                    self.enjambre.append(particula)
                    break
    
    def updateCandidatosEq(self):
        for particula in self.enjambre:

            if particula.esMejorQue(self.eq_candidatos[0]):
                self.eq_candidatos = [particula] + self.eq_candidatos[:-1]

            elif particula.esMejorQue(self.eq_candidatos[1]):
                self.eq_candidatos = [self.eq_candidatos[0], particula] + self.eq_candidatos[1:-1]

            elif particula.esMejorQue(self.eq_candidatos[2]):
                self.eq_candidatos = self.eq_candidatos[:2] + [particula] + self.eq_candidatos[2: -1]
            
            elif particula.esMejorQue(self.eq_candidatos[3]):
                self.eq_candidatos[3] = particula
                
    def construirEqPool(self):
        eqPromedio = Particula(self.problema)
        eqPromedio.x = np.mean([ candidato.x for candidato in self.eq_candidatos ], axis = 0).tolist()
        return self.eq_candidatos + [ eqPromedio ]
    
    def evolucion(self):

        for iter in range(1, self.maxIter + 1):

            print(f"Iteracion no: {iter}")
            
            self.updateCandidatosEq()
            eq_pool = self.construirEqPool()
            for particula in eq_pool:
                print(particula)

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

                    particula.x = self.problema.sigmoideP(particula.x)
                    print(particula.x)

                    # np.clip
                    #particula.x = np.clip(particula.x, self.lower_band, self.upper_band)


                    if (particula.esFactible(particula.x)):
                        print("particula era factible")
                        break
                

    def solve(self):
        self.inicializarPoblacion()
        self.evolucion()
        self.updateCandidatosEq()
        mejoresParticulas = self.eq_candidatos
        print("Mejores particulas: ")
        for particula in mejoresParticulas:
            print(particula)


# Cantidad de particulas = 5
n = 5
# Numero maximo de iteraciones
MAX_ITER = 15
# Constantes de explotacion y explotacion
a1 = 2
a2 = 1
#
GP = 0.5

# Ejecutar el optimizador
problema = Problema()
optimizer = EquilibriumOptimizer2(problema, n, MAX_ITER, a1, a2, GP)
optimizer.solve()
