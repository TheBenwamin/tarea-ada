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

ESQUEMA SRTBOT:
    S: f(i, j, turno) = máxima satisfacción garantizada del Profesor
                        considerando porciones [i, j] y turno actual
    R: Recurrencia minimax: Profesor maximiza, Hermana minimiza
    T: Tabla de memoización (diccionario o arreglo)
    B: Casos base cuando quedan < n o = n porciones
    O: Cálculo bajo demanda (top-down)
    T: Máxima satisfacción garantizada (valor numérico)

================================================================================
"""

# ============================================================================
# VERSIÓN 1: MEMOIZACIÓN CON DICCIONARIOS (Recomendada para claridad)
# ============================================================================

def satisfaccion_hash(st, n):
    """
    Resuelve el problema de la torta usando memoización con diccionarios.

    Parámetros:
        st (list): Lista de satisfacciones de las 2n porciones
                   st[i] puede ser negativo, cero o positivo
        n (int): Número de porciones que se comen en cada turno
                 Total de porciones = 2n

    Retorna:
        int/float: Máxima satisfacción garantizada para el Profesor

    Complejidad:
        Tiempo: O(n³) promedio
        Espacio: O(n²) promedio para la tabla de memoización
    """

    total_porciones = 2 * n
    memo = {}  # Diccionario de memoización: clave (i, j, turno) -> valor f(i, j, turno)

    # =========================================================================
    # FUNCIONES AUXILIARES
    # =========================================================================

    def suma_rango(inicio, fin):
        """
        Calcula la suma de satisfacciones en el rango [inicio, fin] (inclusive).

        Parámetros:
            inicio (int): Índice inicial
            fin (int): Índice final

        Retorna:
            int/float: Suma de satisfacciones en el rango
        """
        if inicio <= fin:
            return sum(st[inicio:fin+1])
        else:
            # Manejo de caso donde inicio > fin (no debe ocurrir en este problema)
            return 0

    # =========================================================================
    # FUNCIÓN RECURSIVA CON MEMOIZACIÓN
    # =========================================================================

    def resolver(i, j, turno):
        """
        Función recursiva principal que implementa la recurrencia SRTBOT.

        Parámetros:
            i (int): Índice inicial del rango de porciones disponibles
            j (int): Índice final del rango de porciones disponibles
            turno (int):
                - 0 para Profesor (maximiza)
                - 1 para Hermana (minimiza)

        Retorna:
            int/float: Máxima satisfacción garantizada del Profesor

        Lógica:
            - Verifica si el resultado ya está memoizado
            - Aplica los casos base (< n o == n porciones)
            - Aplica la recurrencia según el turno
        """

        # =====================================================================
        # PASO 1: Verificar si ya fue calculado (memoización)
        # =====================================================================

        clave = (i, j, turno)
        if clave in memo:
            return memo[clave]

        # =====================================================================
        # PASO 2: Calcular tamaño del subproblema
        # =====================================================================

        tamaño = j - i + 1

        # =====================================================================
        # CASO BASE 1: Menos de n porciones disponibles
        # =====================================================================
        # No es posible hacer una jugada válida, no hay satisfacción adicional

        if tamaño < n:
            resultado = 0

        # =====================================================================
        # CASO BASE 2: Exactamente n porciones disponibles
        # =====================================================================
        # Es la última jugada posible, el jugador actual se las lleva todas
        # No hay turno posterior

        elif tamaño == n:
            resultado = suma_rango(i, j)

        # =====================================================================
        # CASO RECURSIVO: Más de n porciones disponibles
        # =====================================================================

        else:
            # El jugador actual puede elegir varias posiciones de inicio
            # para su jugada (elegir n porciones consecutivas)

            if turno == 0:  # ===== TURNO DEL PROFESOR (MAXIMIZA) =====

                mejor = -float("inf")

                # Iterar sobre todas las posiciones válidas donde el Profesor
                # puede comenzar su jugada
                for k in range(i, j - n + 2):  # k va desde i hasta j-n+1 (inclusive)

                    # Porciones que se lleva el Profesor en esta jugada
                    ganancia_profesor = suma_rango(k, k + n - 1)

                    # Rango de porciones restantes después de esta jugada
                    siguiente_i = k + n
                    siguiente_j = j

                    # Verificar si quedan porciones para la siguiente jugada
                    if siguiente_i <= siguiente_j:
                        # Hay porciones restantes, es turno de la Hermana
                        futuro = resolver(siguiente_i, siguiente_j, 1)
                    else:
                        # No hay porciones restantes
                        futuro = 0

                    # Calcular valor total para esta opción
                    valor_total = ganancia_profesor + futuro

                    # El Profesor elige la opción que maximiza su satisfacción
                    mejor = max(mejor, valor_total)

                resultado = mejor

            else:  # ===== TURNO DE LA HERMANA (MINIMIZA) =====

                mejor = float("inf")

                # Iterar sobre todas las posiciones válidas donde la Hermana
                # puede comenzar su jugada
                for k in range(i, j - n + 2):  # k va desde i hasta j-n+1 (inclusive)

                    # Las porciones que toma la Hermana se pierden para el Profesor
                    # (no contribuyen a su satisfacción)
                    # Usamos suma_rango solo para claridad, pero no la añadimos

                    # Rango de porciones restantes después de esta jugada
                    siguiente_i = k + n
                    siguiente_j = j

                    # Verificar si quedan porciones para la siguiente jugada
                    if siguiente_i <= siguiente_j:
                        # Hay porciones restantes, es turno del Profesor
                        futuro = resolver(siguiente_i, siguiente_j, 0)
                    else:
                        # No hay porciones restantes
                        futuro = 0

                    # La Hermana elige la opción que minimiza la satisfacción del Profesor
                    mejor = min(mejor, futuro)

                resultado = mejor

        # =====================================================================
        # PASO 3: Memoizar el resultado
        # =====================================================================

        memo[clave] = resultado
        return resultado

    # =========================================================================
    # INICIALIZACIÓN Y RETORNO
    # =========================================================================

    # El juego comienza con todas las porciones disponibles (0 a 2n-1)
    # y es el turno del Profesor (turno = 0)
    respuesta = resolver(0, total_porciones - 1, 0)

    return respuesta


# ============================================================================
# VERSIÓN 2: MEMOIZACIÓN CON ARREGLOS (Listas de Listas)
# ============================================================================

def satisfaccion_arreglo(st, n):
    """
    Resuelve el problema de la torta usando memoización con arreglos.

    Parámetros:
        st (list): Lista de satisfacciones de las 2n porciones
        n (int): Número de porciones que se comen en cada turno

    Retorna:
        int/float: Máxima satisfacción garantizada para el Profesor

    Nota:
        Esta versión usa una estructura tridimensional de listas:
        memo[i][j][t] = f(i, j, t)

        Se inicializa con -inf para detectar estados no calculados.
    """

    total_porciones = 2 * n

    # Inicializar tabla de memoización tridimensional
    # memo[i][j][turno] donde turno ∈ {0, 1}
    memo = [
        [
            [float('-inf') for _ in range(2)]  # 2 valores: turno 0 y turno 1
            for _ in range(total_porciones + 1)
        ]
        for _ in range(total_porciones + 1)
    ]

    # =========================================================================
    # FUNCIONES AUXILIARES
    # =========================================================================

    def suma_rango(inicio, fin):
        """Calcula suma de satisfacciones en [inicio, fin] (inclusive)."""
        if inicio <= fin:
            return sum(st[inicio:fin+1])
        else:
            return 0

    # =========================================================================
    # FUNCIÓN RECURSIVA CON MEMOIZACIÓN EN ARREGLO
    # =========================================================================

    def resolver(i, j, turno):
        """
        Función recursiva que usa arreglo para memoización.

        Parámetros y lógica: Idéntica a satisfaccion_hash pero usando
        arreglo tridimensional en lugar de diccionario.
        """

        # Verificar si ya fue calculado
        if memo[i][j][turno] != float('-inf'):
            return memo[i][j][turno]

        tamaño = j - i + 1

        # CASO BASE 1: Menos de n porciones
        if tamaño < n:
            resultado = 0

        # CASO BASE 2: Exactamente n porciones
        elif tamaño == n:
            resultado = suma_rango(i, j)

        # CASO RECURSIVO
        else:
            if turno == 0:  # PROFESOR maximiza
                mejor = -float("inf")
                for k in range(i, j - n + 2):
                    ganancia = suma_rango(k, k + n - 1)
                    siguiente_i = k + n
                    siguiente_j = j

                    if siguiente_i <= siguiente_j:
                        futuro = resolver(siguiente_i, siguiente_j, 1)
                    else:
                        futuro = 0

                    valor_total = ganancia + futuro
                    mejor = max(mejor, valor_total)

                resultado = mejor

            else:  # HERMANA minimiza
                mejor = float("inf")
                for k in range(i, j - n + 2):
                    siguiente_i = k + n
                    siguiente_j = j

                    if siguiente_i <= siguiente_j:
                        futuro = resolver(siguiente_i, siguiente_j, 0)
                    else:
                        futuro = 0

                    mejor = min(mejor, futuro)

                resultado = mejor

        # Memoizar
        memo[i][j][turno] = resultado
        return resultado

    # =========================================================================
    # INICIALIZACIÓN Y RETORNO
    # =========================================================================

    respuesta = resolver(0, total_porciones - 1, 0)
    return respuesta


# ============================================================================
# FUNCIÓN PRINCIPAL: PRUEBAS Y EJEMPLOS
# ============================================================================

def main():
    """
    Función principal que ejecuta ejemplos de prueba para ambas versiones.
    """

    print("=" * 80)
    print("PROBLEMA DE LA TORTA DE CUMPLEAÑOS - ENTREGA 1")
    print("Esquema SRTBOT - Programación Dinámica")
    print("=" * 80)
    print()

    # =========================================================================
    # EJEMPLO 1: Caso simple con n=2
    # =========================================================================

    print("EJEMPLO 1: n = 2, st = [3, 1, 2, -1]")
    print("-" * 80)

    n1 = 2
    st1 = [3, 1, 2, -1]

    print(f"Porciones: {len(st1)} (2n = {2*n1})")
    print(f"Satisfacciones: {st1}")
    print(f"Cada jugada consume: {n1} porciones consecutivas")
    print()

    resultado_hash_1 = satisfaccion_hash(st1, n1)
    resultado_arreglo_1 = satisfaccion_arreglo(st1, n1)

    print(f"Versión con diccionarios: {resultado_hash_1}")
    print(f"Versión con arreglos:     {resultado_arreglo_1}")
    print()

    # =========================================================================
    # EJEMPLO 2: Caso con valores positivos
    # =========================================================================

    print("EJEMPLO 2: n = 2, st = [1, 2, 3, 4]")
    print("-" * 80)

    n2 = 2
    st2 = [1, 2, 3, 4]

    print(f"Porciones: {len(st2)} (2n = {2*n2})")
    print(f"Satisfacciones: {st2}")
    print()

    resultado_hash_2 = satisfaccion_hash(st2, n2)
    resultado_arreglo_2 = satisfaccion_arreglo(st2, n2)

    print(f"Versión con diccionarios: {resultado_hash_2}")
    print(f"Versión con arreglos:     {resultado_arreglo_2}")
    print()

    # =========================================================================
    # EJEMPLO 3: Caso con valores mixtos
    # =========================================================================

    print("EJEMPLO 3: n = 2, st = [5, -5, 3, -3]")
    print("-" * 80)

    n3 = 2
    st3 = [5, -5, 3, -3]

    print(f"Porciones: {len(st3)} (2n = {2*n3})")
    print(f"Satisfacciones: {st3}")
    print()

    resultado_hash_3 = satisfaccion_hash(st3, n3)
    resultado_arreglo_3 = satisfaccion_arreglo(st3, n3)

    print(f"Versión con diccionarios: {resultado_hash_3}")
    print(f"Versión con arreglos:     {resultado_arreglo_3}")
    print()

    # =========================================================================
    # EJEMPLO 4: Caso con n=1
    # =========================================================================

    print("EJEMPLO 4: n = 1, st = [10, -5, 8, -2]")
    print("-" * 80)

    n4 = 1
    st4 = [10, -5, 8, -2]

    print(f"Porciones: {len(st4)} (2n = {2*n4})")
    print(f"Satisfacciones: {st4}")
    print(f"Cada jugada consume: {n4} porción (juego de nim)")
    print()

    resultado_hash_4 = satisfaccion_hash(st4, n4)
    resultado_arreglo_4 = satisfaccion_arreglo(st4, n4)

    print(f"Versión con diccionarios: {resultado_hash_4}")
    print(f"Versión con arreglos:     {resultado_arreglo_4}")
    print()

    # =========================================================================
    # VERIFICACIÓN DE CONSISTENCIA
    # =========================================================================

    print("=" * 80)
    print("VERIFICACIÓN DE CONSISTENCIA")
    print("=" * 80)

    ejemplos = [
        (n1, st1, resultado_hash_1, resultado_arreglo_1, "Ejemplo 1"),
        (n2, st2, resultado_hash_2, resultado_arreglo_2, "Ejemplo 2"),
        (n3, st3, resultado_hash_3, resultado_arreglo_3, "Ejemplo 3"),
        (n4, st4, resultado_hash_4, resultado_arreglo_4, "Ejemplo 4"),
    ]

    for n, st, res_hash, res_arreglo, nombre in ejemplos:
        coinciden = res_hash == res_arreglo
        estado = "✓ OK" if coinciden else "✗ ERROR"
        print(f"{nombre}: {estado} (diccionario={res_hash}, arreglo={res_arreglo})")

    print()
    print("=" * 80)
    print("Fin de pruebas")
    print("=" * 80)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
