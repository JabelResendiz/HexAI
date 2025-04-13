# Estrategia de HexAI

La estrategia de HexAI combina heurísticas estructurales y búsqueda de caminos para tomar decisiones óptimas en el juego de Hex. El objetivo es conectar los lados asignados al jugador de manera eficiente mientras se contrarrestan las amenazas del oponente.

---


## Heurística Mejorada y Búsqueda A* Personalizada

Una parte fundamental de la inteligencia de HexAI radica en su capacidad para encontrar rutas óptimas entre regiones propias del tablero, evitando la influencia del oponente. Para lograr esto, se utiliza una variante del algoritmo A* que incorpora una heurística especialmente diseñada para el entorno hexagonal del juego.

### Distancia Hexagonal

La métrica base para calcular la distancia entre dos posiciones en el tablero hexagonal es:

```python

def hex_distance(a, b):
    return max(
        abs(a[0] - b[0]),
        abs(a[1] - b[1]),
        abs((a[0] + a[1]) - (b[0] + b[1]))
)
```

Esta función captura de forma efectiva la distancia real en un tablero de celdas hexagonales, y es utilizada tanto en la evaluación heurística como en penalizaciones de proximidad.

### Heurística Mejorada

La función heurística combina la distancia mínima a las metas con un penalizador por cercanía a fichas del oponente, promoviendo caminos más seguros y defensivos:

```python

def improved_heuristic(pos, goal_nodes, opponent_positions):
    h1 = min(hex_distance(pos, goal) for goal in goal_nodes)
    proximity_penalty = sum(1 for op in opponent_positions if hex_distance(pos, op) <= 1)
    return h1 + 3 * proximity_penalty

```

Esto permite que el agente no solo busque conectar regiones propias, sino que también evite aquellas posiciones con alto riesgo estratégico.

### Costo y Prioridad en A*

Durante la ejecución del algoritmo A*, se da preferencia a rutas que pasen por fichas propias (costo 0) sobre las celdas vacías (costo 1), guiadas por la heurística definida:

```python-repl
heapq.heappush(heap, (g + cost + h, g + cost, neighbor))
```

Donde `g` es el costo acumulado real y `h` es el valor de la heurística. Esto permite priorizar rutas eficientes y seguras hacia las regiones objetivo.

### Integración General

Esta búsqueda A* personalizada es utilizada en:

- La evaluación del mejor movimiento posible (`best_move_astar`).
- El análisis de conectividad entre regiones (`min_cost_between_sets`).
- La simulación de amenazas y defensas contra el oponente.

Con esta estrategia, HexAI logra un equilibrio entre ofensiva y defensa, adaptándose dinámicamente al estado del juego.


## Estrategia:



La estrategia general de HexAI sigue un enfoque por etapas que combina patrones clásicos de juego con un análisis heurístico sofisticado. El objetivo es avanzar de forma segura y progresiva hacia una victoria garantizada, minimizando el riesgo y reaccionando inteligentemente ante las acciones del oponente. A continuación, se detallan los pasos clave:


1. **Construcción inicial mediante puentes**  
   - En cada turno, se evalúan las estructuras de puente, que representan una de las formas más sólidas y difíciles de bloquear para conectar regiones.
   - Se priorizan movimientos que extiendan o creen nuevos puentes, consolidando una base sólida de conexión entre los bordes.

2. **Reconexión ante interrupciones del oponente**  
   - Si el oponente juega una ficha que bloquea un puente importante (una posición intermedia crítica), HexAI busca **reconectar las estructuras**, reconstruyendo la conexión y evitando que se debilite la red.

3. **Conexión completa entre bordes**  
   - Una vez se logra unir ambos bordes asignados al jugador (vertical u horizontal según el turno) mediante una cadena de puentes, se alcanza una posición estratégica muy favorable.
   - En esta fase, la prioridad pasa a garantizar el camino mínimo de fichas faltantes para asegurar la victoria.

4. **Juego en posiciones ganadoras**  
   - Se evalúan jugadas que conducen directamente a la victoria, priorizando caminos que requieren la menor cantidad de fichas para cerrar el recorrido ganador.
   - Este análisis se basa en simulaciones y caminos óptimos entre regiones propias del tablero.

5. **Construcción dinámica con heurística mejorada**  
   - Si aún no se ha alcanzado una victoria clara, se juega utilizando la **heurística mejorada basada en A\***:
     - Esta busca rutas eficientes, evitando la influencia directa del oponente.
     - Penaliza zonas cercanas a fichas rivales y promueve trayectorias seguras con preferencia por celdas propias.
     - Integra criterios tanto ofensivos como defensivos, permitiendo a HexAI adaptarse de forma táctica a cada situación del juego.

Con este enfoque escalonado, HexAI combina conocimiento estructural, respuesta táctica y planeación a largo plazo, logrando así un estilo de juego altamente competitivo y difícil de contrarrestar.
