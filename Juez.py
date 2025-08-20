import re
import itertools

#Estudio de expreciones regulares
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
# 'r' indica que la cadena es una cadena cruda (raw string), lo que significa que los caracteres de escape se interpretan literalmente

# 're.fullmatch' verifica si toda la cadena coincide con la expresión regular
# 're.compile' compila la expresión regular para su uso posterior
# 're.search' busca el patrón en la cadena y devuelve un objeto de coincidencia si se encuentra
# 're.findall' encuentra todas las coincidencias del patrón en la cadena y las devuelve como una lista



EBNF = re.compile(r"^[0-9AEIOUaeiouÁÉÍÓÚáéíóúA-Za-zÑñ¿?¡!,.;'\-(): ]+$")
letras = re.compile(r"[A-Za-zÑñÁÉÍÓÚáéíóú]+")
vocales = re.compile(r"[AEIOUaeiouÁÉÍÓÚáéíóú]")


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
# Descripción: Extrae la última palabra de un verso, Decidí ignorar signos de puntuación y espacios para simplificar el calculo del bonus. Si no hay palabras válidas, retorna una cadena vacía.
def ultimas_palabras(verso):
    palabras = re.findall(r"[A-Za-zÑñÁÉÍÓÚáéíóú]+", verso)
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
# Descripción: Funciínq que compara las dos palabras y cuenta cuántas letras coinciden al final de ambas palabras. Si las palabras son iguales, retorna la longitud de la palabra.
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
# Descripción: Función con la que extraemos las vocales de una palabra y las devuelve como una cadena. Convierte la palabra a minúsculas antes de extraer las vocales. Si no encuentra vocales, retorna una cadena vacía.
def extraer_vocales(palabra):
    return "".join(vocales.findall(palabra.lower()))

#***
# Parametro 1: (String) Recibe como parametro una palabra a evaluar
# Parametro 2: (String) Recibe como parametro una palabra a evaluar
#***
# Tipo de return: Entero
#***
# Descripción: Función que compara las vocales de dos palabras y verifica si las vocales coinciden. Si coinciden, retorna el entero de cuantas coinciden; de lo contrario, deja de contar.
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

#***
# Parametro 1: (String) Recibe como parametro una palabra a evaluar
# Parametro 2: (String) Recibe como parametro una palabra a evaluar
#***
# Tipo de return: Tupla (String, Entero)
#***
# Descripción: Función que determina el tipo de rima entre dos palabras y asigna el puntaje correspondiente. (notar que Hola != hola por lo que no la considera gemela debido al cambio de Mayusculas.)
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


with open("estrofas.txt", "r", encoding="utf-8") as f: #Comenzamos el proceso del código
    lineas = [line.strip() for line in f]


palabras_bonus = [p.strip() for p in lineas[0].split(",")]  # Verificación de palabras bonus eliminando espacios
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


with open("decision.txt", "w", encoding="utf-8") as out: #Una vez procesado las estrofas, comenzamos con el archivo de decisión.
    for i, estrofa in enumerate(estrofas, 1): #Validación de 4 versos por estrofa
        if len(estrofa) != 4:
            #print("logre entrar")
            out.write(f"Estrofa {i}: Inválida\n")
            continue

        if not all(validacion_verso(v) for v in estrofa): #Validación de versos dentro del EBNF, se imprime el detalle en caso de invalidación
            for i, verso in enumerate(estrofa, 1):
                if not validacion_verso(verso):
                    print(f"Verso {i} inválido: {repr(verso)}")
                    for caracter in verso:
                        if not EBNF.fullmatch(caracter):
                            print(f"  Carácter no permitido: {repr(caracter)} (Unicode: {ord(caracter)})")
            out.write(f"Estrofa {i}: Inválida (símbolos no permitidos)\n")
            continue
        
        ultimas = [ultimas_palabras(v) for v in estrofa]
        #print("Ultimas palabras de la estrofa:", ultimas)

        total = 0
        tipos_rimas_detectados = set()
        versos_con_rima = [False] * 4
        contador_sin_rima = 0

        for a, b in itertools.combinations(range(4), 2):  #Combinaciones de versos para evaluar rimas
            tipo, puntaje = puntaje_rima(ultimas[a], ultimas[b])
            #print(tipo, puntaje)
            total += puntaje

            if tipo == 'consonante':
                tipos_rimas_detectados.add('consonante')
                tipos_rimas_detectados.add('asonante')
            else:
                tipos_rimas_detectados.add(tipo)

            if tipo != 'sin rima':
                versos_con_rima[a] = True
                versos_con_rima[b] = True
            else:
                contador_sin_rima += 1
            
        
        #Penalización (si ninguno es true, se penaliza ya que significa que no rima ninguno)
        if not all(versos_con_rima):
            total -= 2
        
        #Bonus (Se aplica solo una vez)
        bonus = False
        for palabra in ultimas:
            if palabra in palabras_bonus:
                bonus = True
                total += 2
                break
        
        #Se formatea el puntaje final con la estructura que nos piden
        puntaje_final = round(total / 5, 1)
        #print(total)
        bonus_palabra = " (BONUS)" if bonus else ""

        
        #Se formatea el tipo de rima detectado con la estructura que nos piden
        orden = ['consonante', 'asonante', 'misma terminación', 'gemela'] 
        #print(tipos_rimas_detectados)
        lista_tipos = [t for t in orden if t in tipos_rimas_detectados]
        #print(lista_tipos)
        out.write(f"Estrofa {i}: {puntaje_final}/10{bonus_palabra}\n")
        out.write("Rimas: " + ", ".join(lista_tipos) + "\n")
