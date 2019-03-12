import numpy as np
from numpy import matrix

# caracteres = "\"'AÁBCDEÉFGHIÍJKLMNÑOÓPQRTSUÚVWXYZaábcdeéghiíjklmnñoópqrtsuúvwxyz0123456789-_,{}[]()*+. \n"
caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
modulo = len(caracteres)

nums_llave = []

bloques = []
bloques_llave = []

def inverso_modular_matriz(matriz, mod):
  n = len(matriz)
  matriz = np.matrix(matriz)
  adjunta = np.zeros(shape=(n,n))
  for i in range(n):
    for j in range(n):
      adjunta[i][j] = ((-1) ** (i+j) * round(np.linalg.det(minor(matriz, j , i)))) % mod
  return ((inverso_modular(int(round(np.linalg.det(matriz))), modulo) * adjunta) % mod).astype(int)

def inverso_modular(n, p):
  for i in range(1, p):
    if i * n % p == 1:
      return i
  raise ValueError("{} no tiene inverso módulo {}".format(n, p))

def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
  A=np.array(A)
  minor=np.zeros(shape=(len(A)-1,len(A)-1))
  p=0
  for s in range(0,len(minor)):
    if p==i:
      p=p+1
    q=0
    for t in range(0,len(minor)):
      if q==j:
        q=q+1
      minor[s][t]=A[p][q]
      q=q+1
    p=p+1
  return minor

def texto_a_numeros(texto):
    return [caracteres.find(char) for char in texto]

def lista_a_matriz(lista, dimension):
    bloques = []

    for i in range(0, len(lista), dimension):
        bloques.append(lista[i:i + dimension])

    return np.array(bloques).transpose()

def encriptar(texto, llave, transponer=True):
    matriz_texto = lista_a_matriz(texto_a_numeros(texto), 3)
    matriz_llave = lista_a_matriz(texto_a_numeros(llave), 3)
    if transponer:
        matriz_llave = matriz_llave.transpose()
    matriz_mult = np.asarray(np.dot(matriz_llave, matriz_texto))
    matriz_mod = np.mod(matriz_mult, modulo)
    array_codificado = matriz_mod.transpose().flatten()
    texto_codificado = ""
    for elemento in array_codificado:
        texto_codificado = texto_codificado + caracteres[elemento]

    return texto_codificado

def decriptar(texto, llave):
    matriz_llave = lista_a_matriz(texto_a_numeros(llave), 3).transpose()

    matriz_inversa = inverso_modular_matriz(matriz_llave, modulo)
    inversa_plana = matriz_inversa.transpose().flatten()
    llave_inversa = ""
    for elemento in inversa_plana:
        llave_inversa += caracteres[elemento]

    return encriptar(texto, llave_inversa, transponer=False)

def main():
    opcion = ""

    # reconocer acción a realizar
    while opcion not in ["d", "e"]:
        opcion = input("¿Desea (e)ncriptar o (d)ecriptar? ")

    opcion = {"d": "decriptar", "e": "encriptar"}.get(opcion)

    nombre_archivo = input("Introduzca el nombre de archivo a {}: ".format(opcion))

    # obtener texto del archivo
    with open(nombre_archivo, "r") as f:
        texto = f.read()

    # obtener una llave válida
    while True:
        llave = input("Introduzca la llave: ")
        # convertir la llave en una lista de números
        nums_llave = texto_a_numeros(llave)
        # convertir a bloques de longitud 3
        bloques_llave = []
        for i in range(0, len(nums_llave), 3):
            bloques_llave.append(nums_llave[i:i + 3])

        # si la determinante de la llave es 0
        if not len(llave) == 9 or np.linalg.det(np.array(bloques_llave)) == 0:
            print("Llave inválida. Debe de contener 9 caracteres.")
        else:
            break

    # ya se tiene una llave válida

    if opcion == "encriptar":
        texto_codificado = encriptar(texto, llave)
    else:
        texto_codificado = decriptar(texto, llave)

    print("Texto codificado: {}".format(texto_codificado))

    with open("res.txt", "w") as archivo_encriptado:
        archivo_encriptado.write(texto_codificado)
        print("Texto {} escrito en res.txt".format(opcion[:-1] + "do"))

# def encriptar(texto, llave):

if __name__ == "__main__":
    main()
