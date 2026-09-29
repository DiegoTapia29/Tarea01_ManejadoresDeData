import re
import unicodedata
import time
import random
import string

# 1. Normalización de texto y manejo de excepciones
class TextoVacioError(Exception):
    """Excepción arrojada cuando el texto de entrada está vacío o no tiene palabras válidas."""
    pass

def normalizar_texto(texto):
    """Limpia puntuación, números, espacios extra y acentos, pasando a minúsculas."""
    if not texto or not texto.strip():
        raise TextoVacioError("Error: El texto de entrada está vacío.")
    
    # Eliminamos acentos
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])
    texto = texto.lower()
    
    # Mantenemos solo caracteres alfabéticos y espacios (eliminamos números y puntuación)
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    # Eliminamos espacios extra
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    if not texto:
        raise TextoVacioError("Error: El texto limpiado no contiene palabras válidas.")
        
    return texto.split()

# 2. Eliminamos repetidos y 4. Conteo de frecuencia con tabla hash propia
class TablaHashPropia:
    def __init__(self, capacidad=1009):
        self.capacidad = capacidad
        self.buckets = [[] for _ in range(capacidad)]

    def _hash(self, cadena):
        h = 0
        for char in cadena:
            h = (31 * h + ord(char)) % self.capacidad
        return h

    def insertar(self, palabra):
        """Inserta la palabra o incrementa su frecuencia si ya existe."""
        indice = self._hash(palabra)
        bucket = self.buckets[indice]
        
        # Resolución de colisiones por encadenamiento
        for i in range(len(bucket)):
            if bucket[i][0] == palabra:
                bucket[i][1] += 1
                return
        bucket.append([palabra, 1])

    def obtener_elementos(self):
        """Guarda las palabras y sus frecuencias."""
        elementos = []
        for bucket in self.buckets:
            for item in bucket:
                elementos.append(item)
        return elementos

# 3. Algoritmos de ordenamiento
def merge_sort(arr):
    """Ordena las palabras alfabéticamente."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    izq = merge_sort(arr[:mid])
    der = merge_sort(arr[mid:])

    return merge(izq, der)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i][0] <= der[j][0]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def quick_sort(arr):
    """Ordena las palabras usando un pivote."""
    if len(arr) <= 1:
        return arr

    pivote = arr[len(arr) // 2][0]
    menores = [x for x in arr if x[0] < pivote]
    iguales = [x for x in arr if x[0] == pivote]
    mayores = [x for x in arr if x[0] > pivote]

    return quick_sort(menores) + iguales + quick_sort(mayores)

# 5. Comparamos los tiempos
def generar_texto_aleatorio(num_palabras):
    palabras_base = ["adventures", "disneyland", "blondes", "fork", "road", "sign", "left", "home"]
    return " ".join(random.choice(palabras_base) for _ in range(num_palabras))

def medir_tiempos():
    tamanos = [100, 1000, 10000]
    print(f"{'Palabras':<10} | {'Merge Sort (s)':<15} | {'Quick Sort (s)':<15}")
    print("-" * 46)

    for n in tamanos:
        texto = generar_texto_aleatorio(n)
        palabras = normalizar_texto(texto)

        tabla = TablaHashPropia(capacidad=max(100, n//10))
        for p in palabras:
            tabla.insertar(p)

        datos = tabla.obtener_elementos()

        inicio = time.perf_counter()
        merge_sort(datos.copy())
        t_merge = time.perf_counter() - inicio

        inicio = time.perf_counter()
        quick_sort(datos.copy())
        t_quick = time.perf_counter() - inicio

        print(f"{n:<10} | {t_merge:<15.6f} | {t_quick:<15.6f}")import re
import unicodedata
import time
import random
import string

# 1. Normalización de texto y manejo de excepciones
class TextoVacioError(Exception):
    """Excepción lanzada cuando el texto de entrada está vacío o no tiene palabras válidas."""
    pass

def normalizar_texto(texto):
    """Limpia puntuación, números, espacios extra y acentos, pasando a minúsculas."""
    if not texto or not texto.strip():
        raise TextoVacioError("Error: El texto de entrada está vacío.")

    # Eliminar acentos
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])
    texto = texto.lower()

    # Mantener solo caracteres alfabéticos y espacios (elimina números y puntuación)
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    # Eliminar espacios extra
    texto = re.sub(r'\s+', ' ', texto).strip()

    if not texto:
        raise TextoVacioError("Error: El texto limpiado no contiene palabras válidas.")

    return texto.split()

# 2. Eliminación de repetidos y 4. Conteo de frecuencia con tabla hash propia
class TablaHashPropia:
    def __init__(self, capacidad=1009):
        self.capacidad = capacidad
        self.buckets = [[] for _ in range(capacidad)]

    def _hash(self, cadena):
        h = 0
        for char in cadena:
            h = (31 * h + ord(char)) % self.capacidad
        return h

    def insertar(self, palabra):
        """Inserta la palabra o incrementa su frecuencia si ya existe."""
        indice = self._hash(palabra)
        bucket = self.buckets[indice]

        # Resolución de colisiones por encadenamiento
        for i in range(len(bucket)):
            if bucket[i][0] == palabra:
                bucket[i][1] += 1
                return
        bucket.append([palabra, 1])

    def obtener_elementos(self):
        """Retorna una lista de listas con formato [palabra, frecuencia]."""
        elementos = []
        for bucket in self.buckets:
            for item in bucket:
                elementos.append(item)
        return elementos

# 3. Dos algoritmos de ordenamiento O(n log n)
def merge_sort(arr):
    """Ordena alfabéticamente comparando el primer elemento (la palabra)."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    izq = merge_sort(arr[:mid])
    der = merge_sort(arr[mid:])

    return merge(izq, der)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i][0] <= der[j][0]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def quick_sort(arr):
    """Ordena alfabéticamente usando partición basada en pivote."""
    if len(arr) <= 1:
        return arr

    pivote = arr[len(arr) // 2][0]
    menores = [x for x in arr if x[0] < pivote]
    iguales = [x for x in arr if x[0] == pivote]
    mayores = [x for x in arr if x[0] > pivote]

    return quick_sort(menores) + iguales + quick_sort(mayores)

# 5. Comparación empírica
def generar_texto_aleatorio(num_palabras):
    palabras_base = ["adventures", "disneyland", "blondes", "fork", "road", "sign", "left", "home"]
    return " ".join(random.choice(palabras_base) for _ in range(num_palabras))

def medir_tiempos():
    tamanos = [100, 1000, 10000]
    print(f"{'Palabras':<10} | {'Merge Sort (s)':<15} | {'Quick Sort (s)':<15}")
    print("-" * 46)

    for n in tamanos:
        texto = generar_texto_aleatorio(n)
        palabras = normalizar_texto(texto)

        tabla = TablaHashPropia(capacidad=max(100, n//10))
        for p in palabras:
            tabla.insertar(p)

        datos = tabla.obtener_elementos()

        inicio = time.perf_counter()
        merge_sort(datos.copy())
        t_merge = time.perf_counter() - inicio

        inicio = time.perf_counter()
        quick_sort(datos.copy())
        t_quick = time.perf_counter() - inicio

        print(f"{n:<10} | {t_merge:<15.6f} | {t_quick:<15.6f}")

# Ejecución del ejemplo del PDF
if __name__ == "__main__":
    texto_ejemplo = 'Juan fue al parque con Ana. Después compraron comida y regresaron a su casa. Ana quería regresar al parque, pero Juan prefirió quedarse en casa.'

    try:
        palabras_limpias = normalizar_texto(texto_ejemplo)
        tabla = TablaHashPropia()
        for p in palabras_limpias:
            tabla.insertar(p)

        palabras_unicas = tabla.obtener_elementos()
        resultado_ordenado = quick_sort(palabras_unicas)

        # Se hace un reporte de lista alfabética y frecuencias
        print("--- Resultado del Ejemplo ---")
        palabras_solo = [item[0] for item in resultado_ordenado]
        print("Lista alfabética:", ", ".join(palabras_solo))
        print("\nFrecuencias:")
        for item in resultado_ordenado:
            print(f"{item[0]}: {item[1]}")

        print("\n--- Comparación Empírica ---")
        medir_tiempos()

    except TextoVacioError as e:
        print(e)
