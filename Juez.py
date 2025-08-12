import re
import itertools

EBNF = re.compile(r"^[0-9AEIOUaeiouÁÉÍÓÚáéíóúA-Za-zÑñ¿?¡!,.;'\-(): ]+$")

letras = re.compile(r"[A-Za-zÑñÁÉÍÓÚáéíóú]")

def validacion_verso(verso):
    return bool(EBNF.fullmatch(verso.strip()))

def ultimas_palabras(verso):
    palabras = re.findall(r"[A-Za-zÑñÁÉÍÓÚáéíóú]+", verso.lower())
    if palabras:
        return palabras[-1]
    else:
        return ""

def rima_consonante(palabra1, palabra2):
    palabra1 = palabra1.lower()
    palabra2 = palabra2.lower()
    
    minimo_largoPalabra = min(len(palabra1), len(palabra2))
    contador = 0
    for i in range(1, minimo_largoPalabra + 1):
        if palabra1[-i] == palabra2[-i]:
            contador += 1
        else:
            break
    return contador 

def puntaje_rima_consonante(palabra1, palabra2):
    suma = rima_consonante(palabra1, palabra2)
    if suma >= 5:
        return 8
    elif suma >= 3:
        return 5
    else:
        return 0

#Abrimos el archivo estrofas.txt
with open("estrofas.txt", "r", encoding="utf-8") as f:
    lineas = [line.strip() for line in f]

#Verificación del bonus (Saltar línea de palabras bonus y línea en blanco siguiente)
palabras_bonus = lineas[0].split(",")  
lineas = lineas[2:]

#Separar estrofas por líneas en blanco para separar los puntajes
estrofas = []
temp = []
for linea in lineas:
    if linea == "":
        if temp:
            estrofas.append(temp)
            temp = []
    else:
        temp.append(linea)
if temp:
    estrofas.append(temp)

#Abrimos el archivo decision.txt para escribir los resultados
with open("decision.txt", "w", encoding="utf-8") as out:
    for i, estrofa in enumerate(estrofas, 1):
        if len(estrofa) != 4:
            out.write(f"Estrofa {i}: Inválida (no tiene 4 versos)\n")
            continue

        if not all(validacion_verso(v) for v in estrofa):
            out.write(f"Estrofa {i}: Inválida (símbolos no permitidos)\n")
            continue

        ultimas = [ultimas_palabras(v) for v in estrofa]

        total = 0
        for a, b in itertools.combinations(range(4), 2):
            total += puntaje_rima_consonante(ultimas[a], ultimas[b])

        puntaje_final = round(total / 5, 1)
        out.write(f"Estrofa {i}: {puntaje_final}/10\n")
        out.write("Rimas: consonante\n")