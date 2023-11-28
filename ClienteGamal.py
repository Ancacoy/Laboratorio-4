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
    texto_cifrado = []
    for char in mensaje:
        k = random.randint(2, primo - 2)
        c1 = pow(g, k, primo)
        c2 = (pow(clave_publica_a, k, primo) * char) % primo
        texto_cifrado.append((c1, c2))
    return texto_cifrado

# Función para descifrar un mensaje cifrado con ElGamal
def descifrar(clave_privada, primo, c1, c2):
    s = pow(c1, clave_privada, primo)
    mensaje_descifrado = (c2 * pow(s, primo - 2, primo)) % primo
    return mensaje_descifrado

import socket

# Configuración del cliente
host = 'localhost'
puerto = 12345

# Crear un socket del cliente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((host, puerto))

# Recibir la clave pública desde el servidor
clave_publica = eval(cliente_socket.recv(1024).decode())

# Leer el archivo de entrada y convertirlo a una secuencia de enteros
with open("mensajeentrada.txt", "r") as archivo:
    mensaje = [ord(char) for char in archivo.read()]

# Cifrar el mensaje usando ElGamal
texto_cifrado = cifrar(clave_publica, mensaje)

# Unir todos los pares c1 y c2 en una cadena separada por un carácter especial
texto_cifrado_combinado = ','.join([f'{c1},{c2}' for c1, c2 in texto_cifrado])

# Enviar el mensaje cifrado al servidor como una única cadena
cliente_socket.send(texto_cifrado_combinado.encode())

cliente_socket.close()
