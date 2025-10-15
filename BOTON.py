# --- CORREGIDO (con comentarios útiles) ---
import time
import pyfirmata
from datetime import datetime

import inspect
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec  # parche compatibilidad 3.11
board = pyfirmata.Arduino('COM3')

#Promedio
temperaturas = []

# Pines
sensor_temp = board.get_pin('a:0:i')
led_verde    = board.get_pin('d:10:o')
led_amarillo = board.get_pin('d:9:o')
led_rojo     = board.get_pin('d:8:o')
pulsador     = board.get_pin('d:4:i')   # Usá una resistencia de pull-down o cableá pull-up y ajustá la lógica

# Iterador para entradas y habilitar reporting
it = pyfirmata.util.Iterator(board)
it.start()

# Habilitar “reporting” para que no devuelva None (especialmente analógicos)
sensor_temp.enable_reporting()
pulsador.enable_reporting()             # En muchas placas también mejora la lectura digital

# Pequeño “warm-up” hasta tener lecturas válidas
time.sleep(0.5)
for _ in range(10):
    if sensor_temp.read() is not None:
        break
    time.sleep(0.1)

while True:
    boton = pulsador.read()   # se actualiza constantemente
    print(boton)