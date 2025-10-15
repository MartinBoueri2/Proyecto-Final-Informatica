import socket
import json

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 3141       # Puerto igual al que usa el cliente

# Crear socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Servidor escuchando en {HOST}:{PORT}...")

conn, addr = s.accept()
print(f"Conectado desde: {addr}")

# Buffer para mensajes completos
buffer = b''

try:
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            buffer += data

            # Procesar mensajes completos terminados en '\n'
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                try:
                    lectura = json.loads(line.decode())
                    temp_c = lectura.get('temp_c', 0)
                    promedio = lectura.get('promedio', 0)
                    timestamp = lectura.get('timestamp', 0)

                    print(f"[{timestamp:.2f}] Temperatura: {temp_c:.2f} °C, Promedio: {promedio:.2f} °C")
                except json.JSONDecodeError:
                    print("JSON inválido recibido:", line.decode())

except KeyboardInterrupt:
    print("Servidor detenido.")
finally:
    conn.close()
    s.close()