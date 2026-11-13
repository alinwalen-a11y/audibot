import time

def medir_rendimiento(funcion_a_probar):
    inicio = time.time()
    funcion_a_probar()
    fin = time.time()
    return round((fin - inicio) * 1000, 2) # en milisegundos

def ejemplo_lento():
    # Simula un código lento O(n²)
    resultado = []
    for i in range(1000):
        for j in range(1000):
            resultado.append(i*j)
    return resultado

def ejemplo_rapido():
    return [i*j for i in range(1000) for j in range(1000)]

if __name__ == "__main__":
    t_lento = medir_rendimiento(ejemplo_lento)
    t_rapido = medir_rendimiento(ejemplo_rapido)
    print(f"Lento: {t_lento}ms | Rápido: {t_rapido}ms")
    if t_lento > t_rapido * 1.5:
        print("⚠️ REGRESIÓN: El nuevo código es más lento!")