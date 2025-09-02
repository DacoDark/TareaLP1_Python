import re
import itertools

#Estudio expreciones regulares
# '^' significa que busca desde el inicio de la cadena
# '$' significa que busca hasta el final de la cadena
# '[]' define un conjunto de caracteres permitidos
# '+' significa que debe haber al menos un carácter del conjunto
# ' ' (espacio) es un carácter permitido
# '*' significa que puede haber cero o más repeticiones del carácter anterior
# '|' significa "o", permitiendo múltiples opciones
# '()' agrupa expresiones para aplicar cuantificadores a todo el grupo
# '.' es un carácter comodín que representa cualquier carácter excepto una nueva línea
# '\' es utilizado para escapar caracteres especiales
# '-' permite el uso de guiones en palabras
# 're.fullmatch' verifica si toda la cadena coincide con la expresión regular
# 're.compile' compila la expresión regular para su uso posterior

# 'r' indica que la cadena es una cadena cruda (raw string), lo que significa que los caracteres de escape se interpretan literalmente

EBNF = re.compile(r"^[0-9AEIOUaeiouÁÉÍÓÚáéíóúA-Za-zÑñ¿?¡!,.;'-():\" ]+$")
letras = re.compile(r"[A-Za-zÑñÁÉÍÓÚáéíóú]+")
vocales = re.compile(r"[AEIOUaeiouÁÉÍÓÚáéíóú]")


#***
# Parametro 1: Recibe como parametro el patrón a buscar
# Parametro 2: Recibe como parametro el texto donde se buscará el patrón
#***
# Tipo de return: None
#***
# Descripción: Busca un patrón en un texto y muestra el resultado de la búsqueda. Si
# el patrón se encuentra, muestra el texto encontrado y su posición; si no se encuentra, indica que no se encontró.
def buscar_patron(patron, texto):
    print(texto)

    res = re.search(patron, texto)
    if res:
        print(f"Patrón encontrado: {res.group()} en la posición {res.start()} hasta : {res.end()}") 
        print("----------------------------------------")
    else:
        print("Patrón no encontrado")
        print("----------------------------------------")

#*** 
# Parametro 1: (String) Recibe como parametro el verso de una estrofa
#***
# Tipo de Return: Booleano
#***
# Descripción: Verifica si un verso es válido según la expresión regular definida en EBNF si es válido retorna true, si no es válido retorna false.
def validacion_verso(verso):
    return bool(EBNF.fullmatch(verso.strip()))

#***
# Parametro 1: (String) Recibe como parametro el verso de una estrofa
#***
# Tipo de return: String
#***
# Descripción: Extrae la última palabra de un verso, ignorando signos de puntuación y espacios. Si no hay palabras válidas, retorna una cadena vacía.
def ultimas_palabras(verso):
    palabras = re.findall(r"[A-Za-zÑñÁÉÍÓÚáéíóú]+", verso.lower())
    if palabras:
        return palabras[-1]
    else:
        return ""

#***
# Parametro 1: (String) Recibe como parametro una palabra a evaluar
# Parametro 2: (String) Recibe como parametro una palabra a evaluar
#***
# Tipo de return: Entero
#***
# Descripción: Compara las dos palabras y cuenta cuántas letras coinciden al final de ambas palabras. Si las palabras son iguales, retorna la longitud de la palabra.
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

#***
# Parametro 1: (String) Recibe como parametro una palabra a evaluar
#***
# Tipo de return: String
#***
# Descripción: Extrae las vocales de una palabra y las devuelve como una cadena. Convierte la palabra a minúsculas antes de extraer las vocales. Si no encuentra vocales, retorna una cadena vacía.
def extraer_vocales(palabra):
    return "".join(vocales.findall(palabra.lower()))

#***
# Parametro 1: (String) Recibe como parametro una palabra a evaluar
# Parametro 2: (String) Recibe como parametro una palabra a evaluar
#***
# Tipo de return: Entero
#***
# Descripción: Compara las vocales de dos palabras y verifica si las vocales coinciden. Si coinciden, retorna el entero de cuantas coinciden; de lo contrario, deja de contar.
def rima_asonante(palabra1, palabra2):
    palabra1_vocales = extraer_vocales(palabra1)
    palabra2_vocales = extraer_vocales(palabra2)
    minimo_vocales = min(len(palabra1_vocales), len(palabra2_vocales))
    contador = 0
    for i in range(1, minimo_vocales + 1):
        if palabra1_vocales[-i] == palabra2_vocales[-i]:
            contador += 1
        else:
            break
    return contador


def puntaje_rima(palabra1, palabra2):
    if (palabra1 == palabra2):
        return 'gemela', 1  # Si son iguales, puntaje es la longitud de la palabra
    
    puntaje_con = rima_consonante(palabra1, palabra2)
    if puntaje_con >= 5:
        return 'consonante', 8
    elif puntaje_con >= 3:
        return 'consonante', 5
    
    puntaje_ason = rima_asonante(palabra1, palabra2)
    if puntaje_ason >= 3:
        return 'asonante', 8
    elif puntaje_ason == 2:
        return 'asonante', 4
    elif puntaje_ason == 1:
        return 'asonante', 3
    
    if puntaje_con >= 2:
        return 'misma terminación', 2

    return 'sin rima', 0

#Comenzamos el proceso del código
with open("estrofas.txt", "r", encoding="utf-8") as f:
    lineas = [line.strip() for line in f]


palabras_bonus = lineas[0].split(",")  #Verificacion del bonus
lineas = lineas[2:]

estrofas = [] #Separar estrofas por líneas en blanco para separar los puntajes
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
        tipos_rimas_detectados = set()
        rima_verso = [False] * 4
        contador_sin_rima = 0

        for a, b in itertools.combinations(range(4), 2):
            tipo, puntaje = puntaje_rima(ultimas[a], ultimas[b])
            total += puntaje

            if tipo != 'sin rima':
                rima_verso[a] = True
                rima_verso[b] = True
                tipos_rimas_detectados.add(tipo)
            else:
                contador_sin_rima += 1
                
            #tipos_rimas_detectados.add(tipo)
        
        #Penalización
        if not all(rima_verso):
            total -= 2
        
        #Bonus
        bonus = False
        for palabra in ultimas:
            if palabra in palabras_bonus:
                bonus = True
                total += 2
                break

        puntaje_final = round(total / 5, 1)
        bonus_palabra = "(BONUS)" if bonus else ""


        # antes de escribir:
        orden = ['consonante', 'asonante', 'misma terminación', 'gemela']
        lista_tipos = [t for t in orden if t in tipos_rimas_detectados]
        print(lista_tipos)
        out.write(f"Estrofa {i}: {puntaje_final}/10{bonus_palabra}\n")
        out.write("Rimas: " + ", ".join(lista_tipos) + "\n")
