# ♟️ Knight's Tour Solver

¡Bienvenido! Este proyecto es una aplicación interactiva que explora la intersección entre el **Ajedrez**, la **Ciencia de Datos** y la **Teoría de Grafos**. El objetivo principal es analizar historiales de partidas en formato PGN y resolver retos algorítmicos clásicos modelando el tablero como un grafo funcional.

---

##  Características Principales

* **Teoría Interactiva:** Un espacio didáctico para comprender cómo se conectan los movimientos del ajedrez con las estructuras de datos avanzadas.
* **Visualizador de Caminos Hamiltonianos:** Animación interactiva del "Problema del Caballo" (*Knight's Tour*) resolviéndose en milisegundos.
* **Dashboard de Datos (Próximamente):** Análisis estadístico de partidas cargadas mediante archivos `.pgn` (aperturas más comunes, mapas de calor de casillas visitadas y tasas de victoria).

---

##  Respaldos Matemáticos y Algorítmicos

El núcleo de la sección de optimización se basa en el **Problema del Caballo**, el cual consiste en recorrer las 64 casillas del tablero visitando cada una **exactamente una vez**.

* **Enfoque de Grafos:** El tablero se modela como un grafo $G = (V, E)$, donde los vértices $V$ son las 64 casillas y las aristas $E$ son los movimientos legales de la pieza. Encontrar el recorrido perfecto equivale a hallar un **Camino Hamiltoniano**.
* **La Regla de Warnsdorff:** Para evitar la complejidad exponencial ($NP$-completa) del *backtracking* por fuerza bruta, implementamos una heurística lineal. El algoritmo evalúa el entorno local y desplaza la pieza hacia la casilla adyacente que posea el **menor grado de salida futuro**, garantizando una solución óptima instantánea.

>  El prototipo algorítmico base para terminal con documentación y comentarios académicos se encuentra disponible en `research/warnsdorff_prototype.py`.

---

##  Tecnologías Utilizadas

* **Python 3** - Lenguaje principal.
* **NumPy** - Gestión y manipulación de matrices para el estado del tablero.
* **Streamlit** *(Próximamente)* - Framework para el despliegue de la interfaz web interactiva.
* **Plotly / Pandas** *(Próximamente)* - Procesamiento de datos y gráficas estadísticas.

Sandy
