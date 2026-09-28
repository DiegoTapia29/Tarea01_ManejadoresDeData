import re
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
        
        # Resolución de colisiones por encadenamie