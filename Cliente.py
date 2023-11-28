# Función para calcular el máximo común divisor
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Función para calcular el inverso modular
def inverso_modular(e, phi):
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = y2 - temp1 * y1

        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi == 1:
        d = y2 + phi

    return d

# Función para generar claves pública y privada
def generar_claves(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Selecciona un entero e tal que 1 < e < phi y mcd(e, phi) = 1
    e = 2
    while mcd(e, phi) != 1:
        e += 1

    # Calcula d, el inverso multiplicativo de e módulo phi
    d = inverso_modular(e, phi)

    return ((e, n), (d, n))

# Función para cifrar un mensaje usando la clave pública
def cifrar(clave_publica, texto_plano):
    e, n = clave_publica
    mensaje_cifrado = [pow(ord(char), e, n) for char in texto_plano]
    return mensaje_cifrado

# Función para descifrar un mensaje usando la clave privada
def descifrar(clave_privada, texto_cifrado):
    d, n = clave_privada
    mensaje_descifrado = [chr(pow(char, d, n)) for char in texto_cifrado]
    return ''.join(mensaje_descifrado)

#####################################
########### CLIENTE #################
#####################################
import socket

# Configuración del cliente
host = 'localhost'
puerto = 12345

# Crear un socket del cliente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((host, puerto))

# Recibir la clave pública desde el servidor
clave_publica = eval(cliente_socket.recv(1024).decode())  # Convertir la cadena de texto a tupla

# Leer el archivo de entrada
with open("mensajeentrada.txt", "r") as archivo:
    mensaje = archivo.read()

# Cifrar el mensaje usando la clave pública
mensaje_cifrado = cifrar(clave_publica, mensaje)

# Imprimir o visualizar el mensaje cifrado
print("Mensaje cifrado recibido:", mensaje_cifrado)

# Enviar el mensaje cifrado al servidor
cliente_socket.send(str(mensaje_cifrado).encode())

cliente_socket.close()
