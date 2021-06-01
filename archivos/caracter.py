"""Detector de caracteres no validos en campos.
   Si nos ingresa una palabra, debemos saber que son todas letras y no numeros
   o caracteres especiales. Restringimos a que los campos no sean todos espacios.
   Evitamos tambien que un campo tenga lo siguiente: 'a   as'
   pero puede contener lo siguiente:'a a ', que no afecta"""

def caracter(caracteres, lista=False):
    #la funcion split une los caracteres, si hay espacios no importa, solo almacenamos la letras
    #la funcion split transforma en lista la cadena, por lo que accedemos a ella por el indice [0]
    #retornamos la cadena, entendemos que siempre es cadena, a mayuscula.
    #si la lista es True, se devuelven mas de dos palabras sino solo la primera
    
    if caracteres and not caracteres.isspace():
        caracteres = caracteres.split()
        if len(caracteres) > 1 and lista:
            for x in range(len(caracteres)):
                for e in caracteres[x]:
                    if not evaluar(e):
                        return False
            caracteres = ' '.join(caracteres)
            caracteres = caracteres.capitalize()
            return caracteres
        else:
            caracteres = caracteres[0]
            for x in range(len(caracteres)):
                if not evaluar(caracteres[x]):
                    return False
            caracteres = caracteres.strip()
            return caracteres.capitalize()
    else:return False

def evaluar(caracter):
    #si es espacio, no afecta, al igual que enie de nonio
    if ord(caracter) >= 65 and ord(caracter) <= 90:
        return True
    elif ord(caracter)>= 97 and ord(caracter) <= 122:
        return True
    elif ord(caracter) == 10:
        return True
    elif ord(caracter) == 241:
        return True
    else:
        return False

def es_num(caracter):
    try:
        caracter = str(caracter)
    except:
        return False
    if len(caracter) > 1:
        for x in range(len(caracter)):
            if not (ord(caracter[x]) >= 48 and ord(caracter[x]) <= 57):
                return False
        return True
    else:
        if caracter != "":
            if ord(caracter) >= 48 and ord(caracter) <= 57:
                return True
            else:return False
        else:return False

def alfa_num(caracter, opcion=False):
    #se pasa opcion para validar campo empresa
    #se aceptan comas, puntos, guiones y espacios
    #de lo contrario solo acepta letras+numeros sin espacios
    
    try:
        caracter = str(caracter)
    except:
        return False
    if len(caracter) >= 1:
        for x in range(len(caracter)):
            if not es_num(caracter[x]):
                if not evaluar(caracter[x]):
                    if opcion and ord(caracter[x]) != 32:
                        if not (ord(caracter[x]) >= 44 and ord(caracter[x]) <= 46):
                            return False
                    if not opcion:
                        return False
        caracter = caracter.strip()
        caracter = caracter.capitalize()
        return caracter
    else:
        return False
    
def comparar_cadenas(cadena1,cadena2):
    if (cadena1 and cadena2) != "":
        if len(cadena1) == len(cadena2):
            for x in range(len(cadena1)):
                if not ord(cadena1[x]) == ord(cadena2[x]):
                    return False
            return True
        else:
            return False
    else:
        return False

