"""
================================================================================
                    SOLUCIÓN: PROBLEMA DE LA TORTA DE CUMPLEAÑOS
                    Entrega 1 - Análisis de Algoritmos
================================================================================

DESCRIPCIÓN:
    Implementación del esquema SRTBOT (Subproblema, Relación, Tabla, Borde,
    Orden, Transición) para resolver el problema de la torta de cumpleaños
    usando programación dinámica.

PROBLEMA:
    - Una torta redonda se divide en 2n porciones iguales
    - Cada porción i tiene satisfacción st[i] (puede ser negativa o positiva)
    - Profesor y Hermana se alternan eligiendo ángulos válidos
    - Quien elige α se come porciones desde α hasta α + π (n porciones consecutivas)
    - Profesor comienza y ambos juegan óptimamente
    - Objetivo: Maximizar satisfacción GARANTIZADA del Profesor

================================================================================
"""

# ============================================================================
# VERSIÓN 1: MEMOIZACIÓN CON DICCIONARIOS (Recomendado para claridad)
# ============================================================================

def satisfaccion_hash(st, n):
    """
    Resuelve el problema de la torta usando memoización con diccionarios.

    ESQUEMA SRTBOT:
    - S (Subproblema): f(inicio, fin, turno) = máxima satisfacción garantizada
                       del Profesor cuando quedan porciones [inicio, fin] y es
                       el turno del jugador indicado
    - R (Recurrencia):
        * Base: tamaño==n => suma de porciones
        * Recursiva: turno==0 => max { suma + f(...,turno=1) }
                     turno==1 => min { f(...,turno=0) }
    - T (Tabla): Diccionario (hash table)
    - B (Borde): tamaño < n => 0, tamaño == n => suma de n porciones
    - O (Orden): Memoización (cálculo bajo demanda)
    - T (Resultado): Valor entero/flotante

    Parámetros:
        st (list): Lista de satisfacciones de las 2n porciones
        n (int): Número de porciones que se comen en cada turno

    Retorna:
        int/float: Máxima satisfacción garantizada para el Profesor

    Complejidad:
        Tiempo: O((2n)^3) en promedio
        Espacio: O((2n)^3) promedio (solo estados visitados)
    """

    total_porciones = 2 * n
    memo = {}  # Tabla de memoización con diccionario

    # Tabla auxiliar para suma prefija
    prefix_sum = [0] * (total_porciones + 1)
    for i in range(total_porciones):
        prefix_sum[i + 1] = prefix_sum[i] + st[i]

    def suma_rango(inicio, fin):
        """
        Calcula suma de satisfacciones en rango [inicio, fin)

        Parámetros:
            inicio: índice inicial (inclusivo)
            fin: índice final (exclusivo)
        """
        if inicio < fin:
            return prefix_sum[fin] - prefix_sum[inicio]
        else:
            # Manejo de casos circulares
            return prefix_sum[total_porciones] - prefix_sum[inicio] + prefix_sum[fin]

    def resolver(inicio, fin, turno):
        """
        Función recursiva con memoización.

        Parámetros:
            inicio (int): Índice inicial del rango [inclusivo]
            fin (int): Índice final del rango [inclusivo]
            turno (int): 0 para Profesor (maximiza), 1 para Hermana (minimiza)

        Retorna:
            int/float: Máxima satisfacción garantizada del Profesor en este subproblema
        """

        # Verificar si ya fue calculado
        clave = (inicio, fin, turno)
        if clave in memo:
            return memo[clave]

        tamaño = fin - inicio + 1

        # ===== CASO BASE 1: Menos de n porciones =====
        # No es posible hacer una jugada válida, retorna 0
        if tamaño < n:
            resultado = 0
            memo[clave] = resultado
            return resultado

        # ===== CASO BASE 2: Exactamente n porciones =====
        # El jugador actual toma todas las porciones restantes
        # Si es turno del Profesor (turno=0), obtiene esa suma
        # Si es turno de la Hermana (turno=1), el Profesor obtiene 0 (ella no suma para el Profesor)
        if tamaño == n:
            if turno == 0:
                resultado = suma_rango(inicio, fin + 1)
            else:  # turno == 1, la Hermana elige
                resultado = 0  # La hermana no aporta a la satisfacción del Profesor
            memo[clave] = resultado
            return resultado

        # ===== CASO RECURSIVO: Más de n porciones =====

        if turno == 0:  # Turno del PROFESOR (MAXIMIZA su satisfacción)
            mejor = -float("inf")

            # El Profesor prueba todas las posibles jugadas válidas
            # Cada jugada consiste en elegir n porciones consecutivas
            for pos in range(inicio, fin - n + 2):
                # Profesor elige porciones desde pos hasta pos+n-1
                ganancia_profesor = suma_rango(pos, pos + n)

                # Después de esta jugada, quedan porciones en el rango
                # [pos + n, fin], y es el turno de la Hermana
                nuevo_inicio = pos + n
                nuevo_fin = fin

                if nuevo_inicio > nuevo_fin:
                    # No hay más porciones después de esta jugada
                    futuro = 0
                else:
                    # Recursivamente resolver el subproblema con turno de Hermana
                    futuro = resolver(nuevo_inicio, nuevo_fin, 1)

                # El Profesor quiere maximizar: su ganancia actual + lo que obtendrá después
                mejor = max(mejor, ganancia_profesor + futuro)

        else:  # turno == 1, Turno de la HERMANA (MINIMIZA la satisfacción del Profesor)
            mejor = float("inf")

            # La Hermana prueba todas las posibles jugadas válidas
            # Ella elige para minimizar la ganancia futura del Profesor
            for pos in range(inicio, fin - n + 2):
                # Hermana elige porciones desde pos hasta pos+n-1
                # (Sus porciones no afectan directamente la satisfacción del Profesor)

                # Después de esta jugada, quedan porciones en el rango
                # [pos + n, fin], y es el turno del Profesor nuevamente
                nuevo_inicio = pos + n
                nuevo_fin = fin

                if nuevo_inicio > nuevo_fin:
                    # No hay más porciones después de esta jugada
                    futuro = 0
                else:
                    # Recursivamente resolver el subproblema con turno del Profesor
                    futuro = resolver(nuevo_inicio, nuevo_fin, 0)

                # La Hermana quiere minimizar: lo que el Profesor obtendrá
                mejor = min(mejor, futuro)

        memo[clave] = mejor
        return mejor

    # RESULTADO: Resolver desde rango completo, turno del Profesor
    resultado = resolver(0, total_porciones - 1, 0)
    return resultado


# ============================================================================
# VERSIÓN 2: MEMOIZACIÓN CON ARREGLOS (Listas de Listas)
# ============================================================================

def satisfaccion_arreglo(st, n):
    """
    Resuelve el problema de la torta usando memoización con arreglos.

    ESQUEMA SRTBOT:
    - S (Subproblema): memo[i][j][turno] = máxima satisfacción garantizada
                       del Profesor cuando quedan porciones [i, j] y es
                       el turno del jugador indicado
    - R (Recurrencia): Mismo que versión hash
    - T (Tabla): Arreglo 3D (listas de listas)
    - B (Borde): tamaño < n => 0, tamaño == n => suma de n porciones
    - O (Orden): Llenar por tamaño creciente de rango
    - T (Resultado): Valor entero/flotante

    Parámetros:
        st (list): Lista de satisfacciones de las 2n porciones
        n (int): Número de porciones que se comen en cada turno (mitad del total)

    Retorna:
        int/float: Máxima satisfacción garantizada para el Profesor

    Complejidad:
        Tiempo: O((2n)^3) - O(n^3) estados × O(n) transiciones por estado
        Espacio: O((2n)^3) - Tabla de memoización
    """

    total_porciones = 2 * n

    # INICIALIZACIÓN DE LA TABLA DE MEMOIZACIÓN
    # memo[i][j][turno] = máxima satisfacción garantizada para el Profesor
    #                      cuando hay porciones en rango [i, j]
    #                      turno: 0 = Profesor (maximiza), 1 = Hermana (minimiza)
    memo = [[[-float("inf") for _ in range(2)] for _ in range(total_porciones)]
            for _ in range(total_porciones)]

    # Tabla auxiliar para suma prefija (optimización)
    prefix_sum = [0] * (total_porciones + 1)
    for i in range(total_porciones):
        prefix_sum[i + 1] = prefix_sum[i] + st[i]

    def suma_rango(inicio, fin):
        """Calcula suma de satisfacciones en rango [inicio, fin) (fin exclusivo)"""
        if inicio < fin:
            return prefix_sum[fin] - prefix_sum[inicio]
        else:
            return prefix_sum[total_porciones] - prefix_sum[inicio] + prefix_sum[fin]

    # ===== RELLENADO DE LA TABLA (ORDEN: Por tamaño creciente del rango) =====
    # Procesamos desde rangos de tamaño n hasta tamaño 2n
    # Esto garantiza que cuando calculamos f[i][j], todos los subproblemas
    # más pequeños ya han sido resueltos

    for tamaño in range(n, total_porciones + 1):
        for inicio in range(total_porciones):
            fin = inicio + tamaño - 1

            # Validar que los índices estén dentro del rango válido
            if fin >= total_porciones:
                continue

            # ===== CASOS BASE: Cuando exactamente quedan n porciones =====
            if tamaño == n:
                suma = suma_rango(inicio, fin + 1)
                # Si es turno del Profesor, obtiene la suma
                memo[inicio][fin][0] = suma
                # Si es turno de la Hermana, el Profesor obtiene 0
                memo[inicio][fin][1] = 0

            # ===== CASO RECURSIVO: Cuando hay más de n porciones =====
            else:
                # ===== Turno del PROFESOR (turno = 0, MAXIMIZA) =====
                mejor_profesor = -float("inf")

                # El Profesor intenta cada posible primera jugada
                for primera_jugada in range(inicio, fin - n + 2):
                    ganancia_actual = suma_rango(primera_jugada, primera_jugada + n)

                    # Calcular nuevo rango después que el Profesor elige
                    nuevo_inicio = primera_jugada + n
                    nuevo_fin = fin
                    nuevo_tamaño = nuevo_fin - nuevo_inicio + 1

                    if nuevo_tamaño == 0:
                        # No hay más porciones, solo la ganancia actual
                        mejor_profesor = max(mejor_profesor, ganancia_actual)
                    else:
                        # Hay más juego, le toca a la Hermana
                        futuro = memo[nuevo_inicio][nuevo_fin][1]
                        mejor_profesor = max(mejor_profesor, ganancia_actual + futuro)

                memo[inicio][fin][0] = mejor_profesor

                # ===== Turno de la HERMANA (turno = 1, MINIMIZA) =====
                mejor_hermana = float("inf")

                # La Hermana elige para minimizar la satisfacción del Profesor
                for primera_jugada in range(inicio, fin - n + 2):
                    nuevo_inicio = primera_jugada + n
                    nuevo_fin = fin
                    nuevo_tamaño = nuevo_fin - nuevo_inicio + 1

                    if nuevo_tamaño == 0:
                        # No hay más juego
                        mejor_hermana = min(mejor_hermana, 0)
                    else:
                        # Le toca al Profesor en el siguiente turno
                        futuro = memo[nuevo_inicio][nuevo_fin][0]
                        mejor_hermana = min(mejor_hermana, futuro)

                memo[inicio][fin][1] = mejor_hermana

    # RESULTADO: Máxima satisfacción garantizada del Profesor
    # Comienza en rango completo [0, 2n-1] y es turno del Profesor (turno=0)
    resultado = memo[0][total_porciones - 1][0]

    return resultado if resultado != -float("inf") else 0


# ============================================================================
# FUNCIÓN PRINCIPAL: PRUEBAS Y EJEMPLOS
# ============================================================================

def main():
    """
    Función principal que prueba ambas versiones de la solución
    con ejemplos básicos para validar la lógica del SRTBOT.
    """

    print("=" * 80)
    print("SOLUCIÓN: PROBLEMA DE LA TORTA DE CUMPLEAÑOS")
    print("=" * 80)
    print()

    # ====== EJEMPLO 1: Torta simple con 4 porciones (n=2) ======
    print("EJEMPLO 1: Torta con 4 porciones (n=2)")
    print("-" * 80)

    n1 = 2
    st1 = [1, -2, 3, -1]

    print(f"n = {n1} (2n = {2*n1} porciones)")
    print(f"Satisfacciones: st = {st1}")
    print()

    print("Análisis manual:")
    print("- Porción 0: satisfacción = 1")
    print("- Porción 1: satisfacción = -2")
    print("- Porción 2: satisfacción = 3")
    print("- Porción 3: satisfacción = -1")
    print()
    print("Posibles primeras jugadas del Profesor:")
    print("  1. Elegir porciones [0,1]: ganancia = 1 + (-2) = -1")
    print("     → Hermana elige [2,3]: = 3 + (-1) = 2")
    print("     → Garantizado Profesor: -1")
    print()
    print("  2. Elegir porciones [1,2]: ganancia = -2 + 3 = 1")
    print("     → Hermana elige [3,0]: = -1 + 1 = 0")
    print("     → Garantizado Profesor: 1")
    print()
    print("  3. Elegir porciones [2,3]: ganancia = 3 + (-1) = 2")
    print("     → Hermana elige [0,1]: = 1 + (-2) = -1")
    print("     → Garantizado Profesor: 2")
    print()
    print("  Profesor elige opción 3 (máximo garantizado): 2")
    print()

    resultado1_hash = satisfaccion_hash(st1, n1)
    resultado1_arr = satisfaccion_arreglo(st1, n1)

    print(f"Resultado (versión hash):     {resultado1_hash}")
    print(f"Resultado (versión arreglos): {resultado1_arr}")
    print()

    # ====== EJEMPLO 2: Torta con 6 porciones (n=3) ======
    print("EJEMPLO 2: Torta con 6 porciones (n=3)")
    print("-" * 80)

    n2 = 3
    st2 = [5, -3, 2, 4, -1, 3]

    print(f"n = {n2} (2n = {2*n2} porciones)")
    print(f"Satisfacciones: st = {st2}")
    print()

    resultado2_hash = satisfaccion_hash(st2, n2)
    resultado2_arr = satisfaccion_arreglo(st2, n2)

    print(f"Resultado (versión hash):     {resultado2_hash}")
    print(f"Resultado (versión arreglos): {resultado2_arr}")
    print()

    # ====== EJEMPLO 3: Caso trivial (n=1) ======
    print("EJEMPLO 3: Caso trivial con 2 porciones (n=1)")
    print("-" * 80)

    n3 = 1
    st3 = [10, 5]

    print(f"n = {n3} (2n = {2*n3} porciones)")
    print(f"Satisfacciones: st = {st3}")
    print()
    print("Análisis:")
    print("- Profesor elige porción 0: ganancia = 10")
    print("  → Hermana elige porción 1")
    print("  → Total garantizado al Profesor: 10")
    print()
    print("- Profesor elige porción 1: ganancia = 5")
    print("  → Hermana elige porción 0")
    print("  → Total garantizado al Profesor: 5")
    print()
    print("Profesor elige para maximizar: max(10, 5) = 10")
    print()

    resultado3_hash = satisfaccion_hash(st3, n3)
    resultado3_arr = satisfaccion_arreglo(st3, n3)

    print(f"Resultado (versión hash):     {resultado3_hash}")
    print(f"Resultado (versión arreglos): {resultado3_arr}")
    print()

    # ====== EJEMPLO 4: Todas satisfacciones positivas ======
    print("EJEMPLO 4: Todas satisfacciones positivas (n=2)")
    print("-" * 80)

    n4 = 2
    st4 = [10, 8, 6, 4]

    print(f"n = {n4} (2n = {2*n4} porciones)")
    print(f"Satisfacciones: st = {st4}")
    print()

    resultado4_hash = satisfaccion_hash(st4, n4)
    resultado4_arr = satisfaccion_arreglo(st4, n4)

    print(f"Resultado (versión hash):     {resultado4_hash}")
    print(f"Resultado (versión arreglos): {resultado4_arr}")
    print()

    # ====== VERIFICACIÓN DE CONSISTENCIA ======
    print("=" * 80)
    print("VERIFICACIÓN DE CONSISTENCIA")
    print("=" * 80)

    todas_coinciden = (
        resultado1_arr == resultado1_hash and
        resultado2_arr == resultado2_hash and
        resultado3_arr == resultado3_hash and
        resultado4_arr == resultado4_hash
    )

    if todas_coinciden:
        print("✓ Ambas versiones producen resultados idénticos")
    else:
        print("✗ Discrepancia entre versiones (verificar lógica)")

    print()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()

