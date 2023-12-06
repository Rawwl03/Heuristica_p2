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
    #creación problema
    problem = constraint.Problem()

def notSamePlace(a, b):


if __name__ == "__main__":
    ejecucion()
