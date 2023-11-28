import socket

# Implementación del RSA

# Función para calcular el máximo común divisor
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def inverso_modular(e, phi):
    d = 0  # Inicializa la variable para almacenar el inverso modular
    x1, x2 = 0, 1  
    y1, y2 = 1, 0  
    temp_phi = phi  # Almacena temporalmente el valor de phi

    while e > 0: 
        
        temp1 = temp_phi // e  # Calcula el cociente de la división entera         
        temp2 = temp_phi - temp1 * e  # Calcula el residuo de la división 
        # Actualiza las variables
        temp_phi = e
        e = temp2  
        # Calcula x e y basado en los valores anteriores
        x = x2 - temp1 * x1 
        y = y2 - temp1 * y1  

        x2 = x1  # Actualiza los valores  para la siguiente iteración
        x1 = x  
        y2 = y1  
        y1 = y  

    if temp_phi == 1:  # Verifica si el máximo común divisor es 1
        d = y2 + phi  # Calcula el inverso modular si el MCD es 1

    return d  # Devuelve el inverso modular calculado

# Función para generar claves pública y privada
def generar_par_claves(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Selecciona un entero e tal que 1 < e < phi y mcd(e, phi) = 1
    e = 2
    while mcd(e, phi) != 1:
        e += 1

    # Calcula d
    d = inverso_modular(e, phi)

    return ((e, n), (d, n))

# Función para cifrar un mensaje usando la clave pública
def cifrar(clave_publica, texto_plano):
    e, n = clave_publica
    # Esta es una comprensión de lista que itera a través de cada carácter en el texto plano.
    mensaje_cifrado = [pow(ord(caracter), e, n) for caracter in texto_plano]
    return mensaje_cifrado

# Función para descifrar un mensaje usando la clave privada
def descifrar(clave_privada, texto_cifrado):
    d, n = clave_privada
    mensaje_descifrado = [chr(pow(caracter, d, n)) for caracter in texto_cifrado]
    return ''.join(mensaje_descifrado)

##############################################################
################SERVIDOR########################################
##############################################################
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
print("Conexión establecida desde: ", direccion)

# Llaves RSA (p y q son números primos)
p = 61
q = 53
clave_publica, clave_privada = generar_par_claves(p, q)

# Enviar la clave pública al cliente
socket_cliente.send(str(clave_publica).encode())

# Recibir mensaje cifrado desde el cliente
mensaje_cifrado = socket_cliente.recv(1024).decode()
mensaje_cifrado = eval(mensaje_cifrado)  # Convertir la cadena de texto de nuevo a tupla

# Descifrar el mensaje
mensaje_descifrado = descifrar(clave_privada, mensaje_cifrado)

# Escribir el mensaje descifrado en un archivo
with open("mensajerecibido.txt", "w") as archivo:
    archivo.write(mensaje_descifrado)

print("Mensaje recibido y descifrado con éxito.")
socket_cliente.close()
socket_servidor.close()
