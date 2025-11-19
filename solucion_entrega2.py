"""
================================================================================
                    SOLUCIÓN: PROBLEMA DE LA TORTA DE CUMPLEAÑOS
                    Entrega 2 - Análisis y Diseño de Algoritmos
================================================================================

DESCRIPCIÓN:
    Implementación completa del esquema SRTBOT para resolver el problema
    de la torta de cumpleaños usando programación dinámica.

OBJETIVO:
    Comparar experimentalmente dos estrategias de memoización:
    1. Memoización con diccionarios (tablas hash)
    2. Memoización con arreglos (listas tridimensionales)

    Se realizan mediciones de tiempo para diferentes valores de n y se
    analiza la complejidad teórica versus la experimental.

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

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict


# ============================================================================
# VERSIÓN 1: MEMOIZACIÓN CON DICCIONARIOS (Tablas Hash)
# ============================================================================

def satisfaccion_hash(st: List[int]) -> int:
    """
    Resuelve el problema de la torta usando memoización con diccionarios.

    Parámetros:
        st (List[int]): Lista de satisfacciones de las 2n porciones.
                        st[i] puede ser negativo, cero o positivo.
                        len(st) debe ser par.

    Retorna:
        int: Máxima satisfacción garantizada para el Profesor.

    Complejidad Teórica:
        Tiempo: O(n³)
            - En el peor caso, hay O(n²) subproblemas distintos (i, j, turno)
            - Cada subproblema realiza O(n) iteraciones (loop for k)
            - Total: O(n²) × O(n) = O(n³)

        Espacio: O(n²)
            - Tabla de memoización almacena O(n²) entradas
            - Profundidad de la pila de recursión: O(n)
            - Total: O(n²) + O(n) = O(n²)

    Ventajas de Diccionarios:
        - Solo almacena estados realmente visitados
        - Mejor para problemas con espacios dispersos
        - Menor consumo de memoria en promedio
    """
    n = len(st) // 2
    total_porciones = len(st)
    memo: Dict[Tuple[int, int, int], int] = {}

    def suma_rango(inicio: int, fin: int) -> int:
        """Suma de satisfacciones en el rango [inicio, fin] (inclusive)."""
        if inicio <= fin:
            return sum(st[inicio:fin+1])
        return 0

    def resolver(i: int, j: int, turno: int) -> int:
        """
        Función recursiva principal con memoización en diccionario.

        Parámetros:
            i (int): Índice inicial del rango de porciones disponibles
            j (int): Índice final del rango de porciones disponibles
            turno (int): 0 para Profesor (maximiza), 1 para Hermana (minimiza)

        Retorna:
            int: Máxima satisfacción garantizada del Profesor
        """
        # Verificar memoización
        clave = (i, j, turno)
        if clave in memo:
            return memo[clave]

        tamaño = j - i + 1

        # CASO BASE 1: Menos de n porciones disponibles
        if tamaño < n:
            resultado = 0

        # CASO BASE 2: Exactamente n porciones disponibles
        elif tamaño == n:
            resultado = suma_rango(i, j)

        # CASO RECURSIVO: Más de n porciones disponibles
        else:
            if turno == 0:  # PROFESOR (maximiza)
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

            else:  # HERMANA (minimiza)
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

        memo[clave] = resultado
        return resultado

    # Inicializar con todas las porciones disponibles
    respuesta = resolver(0, total_porciones - 1, 0)
    return respuesta


# ============================================================================
# VERSIÓN 2: MEMOIZACIÓN CON ARREGLOS (Listas Tridimensionales)
# ============================================================================

def satisfaccion_arreglo(st: List[int]) -> int:
    """
    Resuelve el problema de la torta usando memoización con arreglos.

    Parámetros:
        st (List[int]): Lista de satisfacciones de las 2n porciones.
                        len(st) debe ser par.

    Retorna:
        int: Máxima satisfacción garantizada para el Profesor.

    Complejidad Teórica:
        Tiempo: O(n³)
            - Idéntica a la versión con diccionarios
            - O(n²) subproblemas × O(n) iteraciones por subproblema

        Espacio: O(n²)
            - Arreglo tridimensional de tamaño (2n+1) × (2n+1) × 2
            - Total: (2n+1)² × 2 ≈ 8n² en peor caso
            - Pila de recursión: O(n)
            - Total: O(n²) + O(n) = O(n²)

    Desventajas de Arreglos:
        - Requiere asignación de memoria total al inicio
        - Desperdicia espacio para estados no visitados
        - Mayor uso de memoria en problemas dispersos

    Ventajas de Arreglos:
        - Acceso O(1) garantizado a cualquier estado
        - Mejor localidad de caché (mejor para CPU)
        - Más rápido en algunos contextos
    """
    n = len(st) // 2
    total_porciones = len(st)

    # Inicializar tabla tridimensional: memo[i][j][turno]
    # Usar -inf como marcador de "no calculado"
    UNINIT = float('-inf')
    memo = [
        [
            [UNINIT for _ in range(2)]  # turno ∈ {0, 1}
            for _ in range(total_porciones + 1)
        ]
        for _ in range(total_porciones + 1)
    ]

    def suma_rango(inicio: int, fin: int) -> int:
        """Suma de satisfacciones en el rango [inicio, fin] (inclusive)."""
        if inicio <= fin:
            return sum(st[inicio:fin+1])
        return 0

    def resolver(i: int, j: int, turno: int) -> int:
        """
        Función recursiva con memoización en arreglo tridimensional.

        Parámetros y lógica: Idénticos a satisfaccion_hash pero usando
        arreglo tridimensional en lugar de diccionario.
        """
        # Verificar si ya fue calculado
        if memo[i][j][turno] != UNINIT:
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
            if turno == 0:  # PROFESOR (maximiza)
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

            else:  # HERMANA (minimiza)
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

        memo[i][j][turno] = resultado
        return resultado

    respuesta = resolver(0, total_porciones - 1, 0)
    return respuesta


# ============================================================================
# MEDICIÓN DE TIEMPOS Y ANÁLISIS EXPERIMENTAL
# ============================================================================

def medir_tiempos() -> Tuple[List[int], List[float], List[float]]:
    """
    Mide el tiempo de ejecución de ambas versiones para diferentes valores de n.

    Retorna:
        Tuple[List[int], List[float], List[float]]:
            - ns: Lista de valores de n probados
            - tiempos_hash: Lista de tiempos para versión con diccionarios
            - tiempos_arreglo: Lista de tiempos para versión con arreglos
    """
    # Valores de n a probar
    ns = [4, 6, 8, 10, 12, 14, 16]
    
    tiempos_hash = []
    tiempos_arreglo = []

    print("\n" + "="*80)
    print("MEDICIÓN DE TIEMPOS DE EJECUCIÓN")
    print("="*80)
    print(f"{'n':<5} {'2n':<5} {'Diccionario (s)':<20} {'Arreglo (s)':<20} {'Ratio':<10}")
    print("-"*80)

    for n in ns:
        # Generar instancia aleatoria
        st = [random.randint(-10, 10) for _ in range(2*n)]

        # Medir tiempo para versión con diccionarios
        start = time.perf_counter()
        resultado_hash = satisfaccion_hash(st)
        tiempo_hash = time.perf_counter() - start
        tiempos_hash.append(tiempo_hash)

        # Medir tiempo para versión con arreglos
        start = time.perf_counter()
        resultado_arreglo = satisfaccion_arreglo(st)
        tiempo_arreglo = time.perf_counter() - start
        tiempos_arreglo.append(tiempo_arreglo)

        # Verificar que ambas versiones den el mismo resultado
        assert resultado_hash == resultado_arreglo, \
            f"Resultados diferentes para n={n}: {resultado_hash} vs {resultado_arreglo}"

        # Calcular ratio
        ratio = tiempo_arreglo / tiempo_hash if tiempo_hash > 0 else 0

        print(f"{n:<5} {2*n:<5} {tiempo_hash:<20.6f} {tiempo_arreglo:<20.6f} {ratio:<10.2f}x")

    print("-"*80)
    print()
    return ns, tiempos_hash, tiempos_arreglo


def generar_graficos(ns: List[int], tiempos_hash: List[float], tiempos_arreglo: List[float]) -> None:
    """
    Genera gráficos comparativos de tiempo de ejecución.

    Parámetros:
        ns: Lista de valores de n
        tiempos_hash: Tiempos para versión con diccionarios
        tiempos_arreglo: Tiempos para versión con arreglos
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Análisis Experimental: Comparación de Estrategias de Memoización', 
                 fontsize=16, fontweight='bold')

    # Gráfico 1: Tiempo de ejecución lineal
    ax1 = axes[0, 0]
    ax1.plot(ns, tiempos_hash, 'o-', label='Diccionarios (Hash)', linewidth=2, markersize=8)
    ax1.plot(ns, tiempos_arreglo, 's-', label='Arreglos', linewidth=2, markersize=8)
    ax1.set_xlabel('Valor de n', fontsize=11)
    ax1.set_ylabel('Tiempo (segundos)', fontsize=11)
    ax1.set_title('Comparación de Tiempos (Escala Lineal)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(ns)

    # Gráfico 2: Tiempo de ejecución logarítmico
    ax2 = axes[0, 1]
    ax2.semilogy(ns, tiempos_hash, 'o-', label='Diccionarios (Hash)', linewidth=2, markersize=8)
    ax2.semilogy(ns, tiempos_arreglo, 's-', label='Arreglos', linewidth=2, markersize=8)
    ax2.set_xlabel('Valor de n', fontsize=11)
    ax2.set_ylabel('Tiempo (segundos, escala logarítmica)', fontsize=11)
    ax2.set_title('Comparación de Tiempos (Escala Logarítmica)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_xticks(ns)

    # Gráfico 3: Ratio de tiempos
    ax3 = axes[1, 0]
    ratios = [t_arr / t_hash if t_hash > 0 else 0 for t_hash, t_arr in zip(tiempos_hash, tiempos_arreglo)]
    colors = ['green' if r < 1 else 'red' for r in ratios]
    ax3.bar(ns, ratios, color=colors, alpha=0.7, edgecolor='black')
    ax3.axhline(y=1, color='black', linestyle='--', linewidth=1)
    ax3.set_xlabel('Valor de n', fontsize=11)
    ax3.set_ylabel('Ratio (Arreglo / Diccionario)', fontsize=11)
    ax3.set_title('Ratio de Tiempo Arreglo vs Diccionario', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_xticks(ns)
    ax3.set_ylim(0, max(ratios) * 1.1)

    # Gráfico 4: Complejidad teórica O(n³)
    ax4 = axes[1, 1]
    # Generar curva teórica O(n³) normalizada
    t0 = tiempos_hash[0] if tiempos_hash[0] > 0 else 1
    n0 = ns[0]
    teorica = [t0 * ((n / n0) ** 3) for n in ns]
    
    ax4.plot(ns, tiempos_hash, 'o-', label='Experimental (Diccionario)', linewidth=2, markersize=8)
    ax4.plot(ns, teorica, 'x--', label='Teórica O(n³)', linewidth=2, markersize=8)
    ax4.set_xlabel('Valor de n', fontsize=11)
    ax4.set_ylabel('Tiempo (segundos)', fontsize=11)
    ax4.set_title('Experimental vs Teórica (Diccionario)', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(ns)

    plt.tight_layout()
    plt.savefig('/workspaces/tarea-ada/graficos_comparacion.png', dpi=300, bbox_inches='tight')
    print("✓ Gráficos guardados en: /workspaces/tarea-ada/graficos_comparacion.png")
    plt.close()


def analizar_complejidad(ns: List[int], tiempos: List[float]) -> None:
    """
    Realiza análisis experimental de complejidad.

    Parámetros:
        ns: Lista de valores de n
        tiempos: Lista de tiempos de ejecución
    """
    print("\n" + "="*80)
    print("ANÁLISIS DE COMPLEJIDAD EXPERIMENTAL")
    print("="*80)

    print("\nValidación de O(n³):")
    print(f"{'n':<5} {'Tiempo (s)':<15} {'T(n)/T(n-1)':<15} {'Expected (n/n-1)³':<20}")
    print("-"*80)

    for i in range(1, len(ns)):
        n_prev = ns[i-1]
        n_curr = ns[i]
        t_prev = tiempos[i-1]
        t_curr = tiempos[i]

        if t_prev > 1e-6:  # Evitar división por cero
            ratio_actual = t_curr / t_prev
            ratio_teorica = (n_curr / n_prev) ** 3
            print(f"{n_curr:<5} {t_curr:<15.6f} {ratio_actual:<15.2f} {ratio_teorica:<20.2f}")

    print("-"*80)
    print("\nInterpretación:")
    print("- Si T(n)/T(n-1) ≈ (n/n-1)³, entonces T(n) ∈ O(n³)")
    print("- Desviaciones pueden deberse a constantes, overhead y variabilidad del sistema")


def tests_funcionales() -> None:
    """
    Realiza pruebas funcionales para verificar correctitud.
    """
    print("\n" + "="*80)
    print("PRUEBAS FUNCIONALES DE CORRECTITUD")
    print("="*80)

    test_cases = [
        ([3, 1, 2, -1], "Caso simple 1"),
        ([1, 2, 3, 4], "Todos positivos"),
        ([5, -5, 3, -3], "Mixtos"),
        ([10, -5, 8, -2], "Valores grandes"),
        ([1, 1, 1, 1, 1, 1], "Todos iguales"),
        ([10, 9, 8, 7, 6, 5, 4, 3], "Decrecientes"),
    ]

    print(f"\n{'Descripción':<25} {'st':<40} {'Hash':<10} {'Arreglo':<10} {'Estado':<10}")
    print("-"*100)

    all_passed = True
    for st, descripcion in test_cases:
        try:
            resultado_hash = satisfaccion_hash(st)
            resultado_arreglo = satisfaccion_arreglo(st)
            
            if resultado_hash == resultado_arreglo:
                estado = "✓ PASS"
            else:
                estado = "✗ FAIL"
                all_passed = False

            st_str = str(st)[:38]
            print(f"{descripcion:<25} {st_str:<40} {resultado_hash:<10} {resultado_arreglo:<10} {estado:<10}")

        except Exception as e:
            print(f"{descripcion:<25} {'ERROR':<40} {str(e):<10}")
            all_passed = False

    print("-"*100)
    if all_passed:
        print("✓ Todas las pruebas pasaron correctamente")
    else:
        print("✗ Algunas pruebas fallaron")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todo el análisis de la Entrega 2.
    """
    print("\n" + "="*80)
    print("ENTREGA 2: ANÁLISIS EXPERIMENTAL Y COMPARACIÓN DE ESTRATEGIAS")
    print("Problema de la Torta de Cumpleaños - Programación Dinámica")
    print("="*80)

    # 1. Ejecutar pruebas funcionales
    tests_funcionales()

    # 2. Medir tiempos
    ns, tiempos_hash, tiempos_arreglo = medir_tiempos()

    # 3. Generar gráficos
    generar_graficos(ns, tiempos_hash, tiempos_arreglo)

    # 4. Analizar complejidad
    analizar_complejidad(ns, tiempos_hash)

    print("\n" + "="*80)
    print("RESUMEN DE RESULTADOS")
    print("="*80)
    print("\nVERSIÓN CON DICCIONARIOS (Hash):")
    print("  - Complejidad Temporal: O(n³)")
    print("  - Complejidad Espacial: O(n²)")
    print("  - Ventaja: Usa solo memoria necesaria para estados visitados")
    print("  - Desventaja: Overhead de hash table")

    print("\nVERSIÓN CON ARREGLOS (Listas 3D):")
    print("  - Complejidad Temporal: O(n³)")
    print("  - Complejidad Espacial: O(n²)")
    print("  - Ventaja: Acceso O(1) directo, mejor localidad de caché")
    print("  - Desventaja: Requiere asignar memoria total al inicio")

    print("\n" + "="*80)
    print("Fin de análisis. Gráficos guardados.")
    print("="*80 + "\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
