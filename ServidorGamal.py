import random

# Función para calcular el máximo común divisor
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Función para encontrar un generador de un grupo primo
def encontrar_generador(primo):
    generadores = []
    for i in range(2, primo):
        if mcd(i, primo) == 1:
            generadores.append(i)
    return generadores

# Función para generar claves pública y privada
def generar_par_claves(primo):
    generadores = encontrar_generador(primo)
    g = random.choice(generadores)

    # Seleccionar un número aleatorio secreto
    clave_privada = random.randint(2, primo - 1)

    # Calcular la clave pública
    clave_publica = pow(g, clave_privada, primo)

    return (primo, g, clave_publica), clave_privada

# Función para cifrar un mensaje usando ElGamal
def cifrar(clave_publica, mensaje):
    primo, g, clave_publica_a = clave_publica
    k = random.randint(2, primo - 2)
    c1 = pow(g, k, primo)
    c2 = (pow(clave_publica_a, k, primo) * mensaje) % primo
    return c1, c2

# Función para descifrar un mensaje cifrado con ElGamal
def descifrar(clave_privada, primo, c1, c2):
    s = pow(c1, clave_privada, primo)
    mensaje_descifrado = (c2 * pow(s, primo - 2, primo)) % primo
    return mensaje_descifrado



import socket

# Configuración del servidor
host = 'localhost'
puerto = 12345

# Crear un socket del servidor
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((host, puerto))
socket_servidor.listen(1)

print("Esperando conexiones...")

# Aceptar conexiones entrantes
socket_cliente, direccion = socket_servidor.accept()
print("Conexión establecida desde:", direccion)

# Parámetros del algoritmo ElGamal (número primo)
primo = 503
clave_publica, clave_privada = generar_par_claves(primo)

# Enviar la clave pública al cliente
socket_cliente.send(str(clave_publica).encode())

# Recibir mensaje cifrado desde el cliente
datos_recibidos = socket_cliente.recv(1024).decode()

# Procesar los datos cifrados completos
pares_texto_cifrado = datos_recibidos.split(",")  # Separar por comas

datos_cifrados = []
mensaje_descifrado = ''
# Procesar los datos cifrados completos
for indice in range(0, len(pares_texto_cifrado), 2):
    if indice + 1 < len(pares_texto_cifrado):
        c1, c2 = int(pares_texto_cifrado[indice]), int(pares_texto_cifrado[indice + 1])
        datos_cifrados.append((c1, c2))  # Agregar el par cifrado a la lista
        caracter_descifrado = descifrar(clave_privada, primo, c1, c2)
        mensaje_descifrado += chr(caracter_descifrado)  # Concatenar el carácter decodificado

print("Valores cifrados en lista de tuplas:", datos_cifrados)
print("Mensaje descifrado completo:", mensaje_descifrado)

# Escribir el mensaje descifrado en un archivo
with open("mensajerecibido.txt", "w") as archivo:
    archivo.write(mensaje_descifrado)

socket_cliente.close()
socket_servidor.close()
