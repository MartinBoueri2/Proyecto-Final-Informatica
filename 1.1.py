import time
import pyfirmata
from datetime import datetime

import inspect
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec  # parche compatibilidad 3.11
board = pyfirmata.Arduino('COM4')

#Promedio
temperaturas = []

#Capturas
capturasTemperatura=[]
capturasPromedio=[]
capturasFecha=[]
capNum=0


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

print("Programa iniciado. Ctrl+C para salir.")

try:
    while True:
        lectura = sensor_temp.read()           # 0..1 (proporcional a 0..5V)
        boton   = pulsador.read()              # True/False o None (flotante)

        # Normalizamos None a False para evitar falsos positivos
        boton = bool(boton)

        #Calculo y Display de la temperatura
        temp_c = lectura * 5.0 * 100.0
        print(f"Temperatura: {temp_c:.2f} °C")


        if lectura is not None and len(temperaturas) == 5:

            # Rangos mutuamente excluyentes (evita pisarse)
            if temp_c < 25:
                led_verde.write(1);  led_amarillo.write(0); led_rojo.write(0)
            elif temp_c < 200:
                led_verde.write(0);  led_amarillo.write(1); led_rojo.write(0)
            else:  # temp_c >= 200
                led_verde.write(0);  led_amarillo.write(0); led_rojo.write(1)
        else:
            # Sin lectura o sin promedio
            led_verde.write(1); led_amarillo.write(1); led_rojo.write(1)


            # --- Promedio móvil de las últimas 5 lecturas ---
        temperaturas.append(temp_c)
        if len(temperaturas) > 5:
            temperaturas.pop(0)  # elimina la más vieja

        promedio = sum(temperaturas) / len(temperaturas)
        print(f"Promedio (últimas {len(temperaturas)}): {promedio:.2f} °C")

        time.sleep(1)

                #Pulsador enviende los leds por 50ms
        if boton:
            led_verde.write(1); led_amarillo.write(1); led_rojo.write(1)
            time.sleep(0.05)
            capturasTemperatura.append(temp_c)
            capturasPromedio.append(promedio)
            capturasFecha.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            capNum=capNum+1

except KeyboardInterrupt:
    print("Programa terminado.")
    print("\n=== Resumen de capturas ===")
    for i in range(len(capturasTemperatura)):
        print(f"Captura {i+1}: {capturasTemperatura[i]:.2f}°C, Promedio: {capturasPromedio[i]:.2f}°C, Fecha: {capturasFecha[i]}")

    # Crear archivo y guardar datos
    with open("capturas.txt", "w", encoding="utf-8") as archivo:
        for i in range(len(capturasTemperatura)):
            archivo.write(f"Captura {i+1}: {capturasTemperatura[i]:.2f}°C, Promedio: {capturasPromedio[i]:.2f}°C, Fecha: {capturasFecha[i]}\n")
    print("\nDatos guardados en 'capturas.txt'.")
finally:
    # Apaga LEDs y cierra conexión siempre
    led_verde.write(0); led_amarillo.write(0); led_rojo.write(0)
    board.exit()

