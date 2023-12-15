import csv, constraint, sys

"""VARIABLES GLOBALES"""
filas_problema = 0
columnas_problema = 0

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

'''Función para obtener las filas y columnas del problema'''
def obtener_struct(filaxcol):
    try:
        fxc = filaxcol[0].split('x')
        return int(fxc[0]), int(fxc[1])
    except Exception:
        raise InputError("La primera línea del archivo de entrada debe de seguir la siguiente estructura: 5x5")

'''Función que lee el archivo de entrada'''
def lectura(archivo_input:str):
    datos = []
    try:
        with open(archivo_input, 'r') as archivo:
            # Lee todas las líneas del archivo y guárdalas en un array
            lineas = archivo.readlines()
        if len(lineas)<3:
            raise InputError("El archivo de entrada debe de tener al menos 3 líneas")
        for linea in lineas:
            datos.append(linea.strip())
        return datos
    except (PermissionError, FileNotFoundError, IsADirectoryError, OSError) as e:
        raise type(e)(f"Error al escribir el archivo de salida: {e}")

def crear_dominio(filas,columnas):
    dominio=[]
    for i in range (1,filas+1):
        for j in range (1,columnas+1):
            dominio.append((i,j))
    return dominio

def crear_variables(problem,variablesTNU,variablesTSU,plazas_electricas,variablesCongelador):
    global filas_problema, columnas_problema
    dominio=crear_dominio(filas_problema,columnas_problema)
    problem.addVariables(variablesCongelador,plazas_electricas)
    variablesTNU_sincongelador= list(set(variablesTNU)- set(variablesCongelador))
    variablesTSU_sincongelador = list(set(variablesTSU) - set(variablesCongelador))
    problem.addVariables(variablesTNU_sincongelador,dominio)
    problem.addVariables(variablesTSU_sincongelador, dominio)

def crear_restricciones(problem, variablesTNU, variablesTSU):
    variables = variablesTSU + variablesTNU
    problem.addConstraint(notSamePlace, variables)
    problem.addConstraint(noGatoEncerrado, variables)
    for var_TSU in variablesTSU:
        problem.addConstraint(notTNUinfront, [var_TSU] + variablesTNU)

'''Función que genera el formato de la cuadrícula del archivo de salida'''
def obtener_formato_cuadricula(num_soluciones,solucion:dict):
    global filas_problema, columnas_problema
    formato_cuadricula = []
    for i in range(filas_problema):
        fila = ["'-'"] * columnas_problema
        formato_cuadricula.append(fila)
    if num_soluciones > 0 :
        variables = list(solucion.keys())
        for var in variables:
            var_valor= solucion[var]
            formato_cuadricula[var_valor[0]-1][var_valor[1]-1]="'"+var+"'"
    return formato_cuadricula

'''Función que genera el archivo de salida'''
def generar_salida(archivo_input:str,num_soluciones,solucion:dict):
    global filas_problema,columnas_problema
    salida=archivo_input.split('.txt')[0]+'.csv'
    try:
        with open(salida, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            header = ["'N. Sol:'", num_soluciones]
            writer.writerow(header)
            cuadricula = obtener_formato_cuadricula(num_soluciones,solucion)
            writer.writerows(cuadricula)
    except (PermissionError, FileNotFoundError, IsADirectoryError, OSError) as e:
        raise type(e)(f"Error al escribir el archivo de salida: {e}")

'''Función principal que ejecuta el programa'''
def ejecucion(archivo_input:str):
    global filas_problema, columnas_problema
    datos = lectura(archivo_input)
    filas, columnas = obtener_struct(datos)
    filas_problema = filas
    columnas_problema = columnas
    plazas_electricidad = obtenerPE(datos[1])
    variablesTNU, variablesTSU, variablesCongelador=obtenerVars(datos)
    if (len(plazas_electricidad) > 0 and len(variablesCongelador) > 0) or (len(plazas_electricidad) == 0 and len(variablesCongelador) == 0):
        #creación problema
        problem = constraint.Problem()
        crear_variables(problem,variablesTNU,variablesTSU,plazas_electricidad,variablesCongelador)
        crear_restricciones(problem, variablesTNU, variablesTSU)
        num_soluciones = sum(1 for _ in problem.getSolutionIter())
        solucion=problem.getSolution()
        generar_salida(archivo_input,num_soluciones, solucion)
    else:
        generar_salida(archivo_input,0, [])
    return 0

def notSamePlace(*args):
    for i in range(0, len(args)):
        for j in range(i+1, len(args)):
            if i!=j and args[i] == args[j]:
                return False
    return True

def notTNUinfront(*args):
    for i in range(1, len(args)):
        if args[i][0] == args[0][0] and args[i][1] > args[0][1]:
            return False
    return True

def noGatoEncerrado(*args):
    global filas_problema
    for i in range(0, len(args)):
        izda = False
        dcha = False
        for j in range(0, len(args)):
            if args[i][0] != 1 and args[i][0] != filas_problema:
                if i!=j and args[i][0] == args[j][0]+1 and args[i][1] == args[j][1]:
                    izda = True
                elif i!=j and args[i][0] == args[j][0]-1 and args[i][1] == args[j][1]:
                    dcha = True
                if dcha and izda:
                    return False
            elif args[i][0] == 1:
                if i!=j and args[j][0] == 2 and args[j][1] == args[i][1]:
                    return False
            elif args[i][0] == filas_problema:
                if i!=j and args[j][0] == filas_problema-1 and args[j][1] == args[i][1]:
                    return False
    return True

'''Función para obtener las variables del archivo de entrada'''
def obtenerVars(datos):
    variablesTNU = []
    variablesTSU = []
    varCongelador = []
    for i in range(2, len(datos)):
        data = datos[i].split("-")
        if data[1] == "TSU":
            variablesTSU.append(datos[i])
        elif data[1] == "TNU":
            variablesTNU.append(datos[i])
        else:
            raise InputError("Las variables deben de seguir el siguiente formato: 1-TSU-C 2-TNU-X ...")
        if data[2] == "C":
            varCongelador.append(datos[i])
        elif data[2] != "X":
            raise InputError("Las variables deben de acabar por 'C' o por 'X'")
    return variablesTNU, variablesTSU, varCongelador

'''Función para obtener las coordenadas de las plazas eléctricas del archivo de entrada'''
def obtenerPE(datospe):
    try:
        pe_portion = datospe.split("PE:")[1].strip()
        if pe_portion == "":
            return []
        else:
            tuples_str = pe_portion.split(')(')
            tuples_str[0] = tuples_str[0][1:]
            if len(tuples_str) > 0:
                tuples_str[-1] = tuples_str[-1][:-1]
                # Convertimos los strings en tuplas de enteros y devolvemos un array con todas las tuplas
                return [tuple(map(int, tpl.split(','))) for tpl in tuples_str]
            else:
                raise InputError("La segunda línea no contiene tuplas en formato: PE: (1,1)(1,2)(2,1) ")
    except (IndexError, ValueError, TypeError, AttributeError) as e:
        raise type(e)(f"La segunda línea del archivo de entrada debe de seguir el siguiente formato: PE: (1,1)(1,2)(2,1) {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise InputError("El comando en terminal debe seguir la siguiente estructura: python archivo.py <archivo.txt>")
    archivo_input=sys.argv[1]
    ejecucion(archivo_input)
