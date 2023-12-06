import csv, sys, constraint

ruta_csv = "datos_parking.csv"


def obtener_struct(filaxcol):
    fxc = filaxcol[0].split('x')
    return fxc[0], fxc[1]

def lectura():
    datos = []
    try:
        with open("files_csv/"+ruta_csv, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                datos.append(fila)
            return datos
    except FileNotFoundError:
        print("Archivo csv no encontrado")
    except csv.Error as e:
        sys.exit('Error en el formato del archivo csv: {}'.format(str(e)))

def ejecucion():
    datos = lectura()
    filas, columnas = obtener_struct(datos[0])
    plazas_electricidad = datos[1]
    indexTNU, indexTSU, variables =obtenerVars(datos)
    #creación problema
    problem = constraint.Problem()

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
    indexTNU = []
    indexTSU = []
    for i in range(2, datos):
        data = datos[i].split("-")
        if data[1] == "TSU":
            indexTSU.append(i-2)
        elif data[1] == "TNU":
            indexTNU.append(i-2)
        variables.append(datos[i])
    return indexTNU, indexTSU, variables

def obtenerPE(datos):



if __name__ == "__main__":
    ejecucion()
