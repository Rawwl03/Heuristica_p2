import csv, sys, constraint


def obtener_struct(filaxcol):
    fxc = filaxcol[0].split('x')
    return int(fxc[0]), int(fxc[1])

def lectura():
    datos = []
    try:
        with open('files_csv/datos_parking.txt', 'r') as archivo:
            # Lee todas las líneas del archivo y guárdalas en un array
            lineas = archivo.readlines()
        for linea in lineas:
            datos.append(linea.strip())
        return datos
    except FileNotFoundError:
        print("Archivo entrada no encontrado")

def crear_dominio(filas,columnas):
    dominio=[]
    for i in range (1,filas+1):
        for j in range (1,columnas+1):
            dominio.append((i,j))
    return dominio

def crear_variables(problem,variablesTNU,variablesTSU,plazas_electricas,variablesCongelador,filas,columnas):
    dominio=crear_dominio(filas,columnas)
    problem.addVariables(variablesCongelador,plazas_electricas)
    variablesTNU_sincongelador= list(set(variablesTNU)- set(variablesCongelador))
    variablesTSU_sincongelador = list(set(variablesTSU) - set(variablesCongelador))
    problem.addVariables(variablesTNU_sincongelador,dominio)
    problem.addVariables(variablesTSU_sincongelador, dominio)


def ejecucion():
    datos = lectura()
    filas, columnas = obtener_struct(datos)
    plazas_electricidad = obtenerPE(datos[1])
    variablesTNU, variablesTSU, variablesCongelador=obtenerVars(datos)
    #creación problema
    problem = constraint.Problem()
    crear_variables(problem,variablesTNU,variablesTSU,plazas_electricidad,variablesCongelador,filas,columnas)
    for variable, dominio in problem._variables.items():
        print(f"{variable}: {dominio}")

def notSamePlace(*args):
    for i in range(0, len(args)):
        for j in range(i+1, len(args)):
            if i!=j and args[i] == args[j]:
                return False
    return True

def notTNUinfront(*args):
    for i in range(1, len(args)):
        if args[i][0] == args[0][0] and args[i][1] > args[0][0]:
            return False
    return True

def obtenerVars(datos):
    variables = []
    variablesTNU = []
    variablesTSU = []
    varCongelador = []
    for i in range(2, len(datos)):
        data = datos[i].split("-")
        if data[1] == "TSU":
            variablesTSU.append(datos[i])
        elif data[1] == "TNU":
            variablesTNU.append(datos[i])
        if data[2] == "C":
            varCongelador.append(datos[i])
    return variablesTNU, variablesTSU, varCongelador

def obtenerPE(datospe):
    # Remove "PE:" and leading/trailing whitespaces
    pe_portion = datospe.split("PE:")[1].strip()

    # Process the pe_portion to extract tuples
    tuples_str = pe_portion.split('),(')
    tuples_str[0] = tuples_str[0][1:]

    if len(tuples_str) > 1:
        tuples_str[-1] = tuples_str[-1][:-1]

        # Convert the strings to tuples and return them
        return [tuple(map(int, tpl.split(','))) for tpl in tuples_str]
    else:
        print("Invalid data format: Second row does not contain tuples.")
        return []



if __name__ == "__main__":
    ejecucion()
