"""
Proyecto: Analizador de Grafos y Ajedrez
Archivo: warnsdorff_prototype.py
Descripción: Prototipo en terminal para resolver el problema del recorrido del 
             caballo (Knight's Tour) visto como la búsqueda de un Camino Hamiltoniano.
             Se utiliza la Regla de Warnsdorff (Heurística de grado mínimo) para
             evitar la complejidad exponencial del backtracking puro.
"""

import numpy as np

# Dimensión del tablero de ajedrez (Grafo de 64 vértices)
N = 8

# Definición de las aristas: Los 8 movimientos posibles del caballo en ejes (Fila, Columna)
# Cada combinación representa un salto legal en "L" en el plano cartesiano del tablero.
MOVIMIENTOS_X = [2, 1, -1, -2, -2, -1, 1, 2]
MOVIMIENTOS_Y = [1, 2, 2, 1, -1, -2, -2, -1]


def es_valido(x, y, tablero):
    """
    Función de Restricción / Validación de Vértices.
    Verifica si las coordenadas (x, y) pertenecen al conjunto de vértices del tablero
    y si el vértice no ha sido visitado previamente (su valor en la matriz es 0).
    """
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == 0


def obtener_grado(x, y, tablero):
    """
    Cálculo del Grado de un Vértice.
    En teoría de grafos, el grado es el número de aristas conectadas a un nodo.
    Esta función cuenta cuántos movimientos válidos futuros tiene el caballo 
    desde la posición actual (x, y). Los nodos periféricos tendrán un grado menor
    que los nodos centrales.
    """
    cuenta = 0
    for i in range(8):
        if es_valido(x + MOVIMIENTOS_X[i], y + MOVIMIENTOS_Y[i], tablero):
            cuenta += 1
    return cuenta


def siguiente_movimiento(x, y, tablero):
    """
    Implementación de la Regla de Warnsdorff (Heurística de Grado Mínimo).
    
    Principio: Evalúa todos los vértices adyacentes alcanzables en el siguiente paso
    y selecciona aquel que tenga el MENOR grado (menos salidas disponibles).
    
    ¿Por qué funciona?: Al priorizar los vértices más aislados (como esquinas y bordes) 
    temprano en el recorrido, evitamos que se conviertan en "nodos huérfanos" inaccesibles 
    más adelante, permitiendo encontrar el Camino Hamiltoniano de forma casi lineal.
    """
    min_grado = 9  # Cota superior: El grado máximo de un caballo en el ajedrez es 8
    sig_x, sig_y = -1, -1

    # Analizar el entorno local (los 8 posibles movimientos)
    for i in range(8):
        nx = x + MOVIMIENTOS_X[i]
        ny = y + MOVIMIENTOS_Y[i]

        # Si el nodo vecino es un objetivo válido, evaluamos su grado futuro
        if es_valido(nx, ny, tablero):
            grado = obtener_grado(nx, ny, tablero)
            
            # Buscamos estrictamente el mínimo grado para optimizar la ruta
            if grado < min_grado:
                min_grado = grado
                sig_x, sig_y = nx, ny

    return sig_x, sig_y


def resolver_camino_caballo(inicio_x, inicio_y):
    """
    Función Principal del Algoritmo.
    Inicializa la estructura de datos (Matriz de adyacencia/estado de 8x8) 
    y ejecuta el bucle que construye secuencialmente el Camino Hamiltoniano.
    """
    # Representación espacial del tablero donde 0 significa "No visitado"
    tablero = np.zeros((N, N), dtype=int)

    # Inicialización del camino en el vértice de origen (Paso 1)
    x, y = inicio_x, inicio_y
    tablero[x][y] = 1

    # El camino completo debe visitar los 64 vértices (63 pasos restantes)
    for paso in range(2, N * N + 1):
        x, y = siguiente_movimiento(x, y, tablero)

        # Control de errores: Si la heurística falla o no encuentra salida
        if x == -1 and y == -1:
            print(f"Error: Algoritmo atrapado en un callejón sin salida en el paso {paso}.")
            return False

        # Registrar el orden cronológico de la visita al vértice
        tablero[x][y] = paso

    # Impresión del resultado: La secuencia numérica del Camino Hamiltoniano
    print("\n========================================")
    print("   CAMINO HAMILTONIANO RESUELTO (8x8)   ")
    print("========================================")
    print(tablero)
    print("========================================")
    return True


# Ejecución del prototipo: Se inicia en la esquina superior izquierda (0, 0) -> Casilla A8
if __name__ == "__main__":
    resolver_camino_caballo(0, 0)
