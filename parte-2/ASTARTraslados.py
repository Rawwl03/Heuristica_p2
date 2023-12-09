import csv

class Nodo:

    def __init__(self, nodo_arriba, nodo_abajo, nodo_izq, nodo_dcha, posicion, valor):
        self.up: nodo_arriba
        self.down: nodo_abajo
        self.left: nodo_izq
        self.right: nodo_dcha
        self.position: posicion
        self.value: valor

class Problema:

    def __init__(self, pos_amb):
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.posicion_ambulancia = pos_amb


def lectura_mapa():
    nombre_archivo = "ASTAR-tests/mapa.csv"
    datos_csv = []
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                datos_csv.append(fila)
            return datos_csv
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
    except csv.Error as e:
        print(f"Error CSV: {e}")

def crear_nodos(datos_csv):
    lista_nodos = []
    for i in range(0, len(datos_csv)):
        for j in range(0, len(datos_csv[i])):
            nodo = Nodo(None, None, None, None, (i+1, j+1), datos_csv[i][j])
            lista_nodos.append(nodo)
    for nodo in lista_nodos:
        node_up = False
        node_down = False
        node_right = False
        node_left = False
        if nodo.position[0] != 1:
            node_up = True
        if nodo.position[0] != len(datos_csv)+1:
            node_down = True
        if nodo.position[1] != 1:
            node_left = True
        if nodo.position[1] != len(datos_csv[nodo.position[1]-1])+1:
            node_right = True
        if node_up:
            nodo.up = lista_nodos[(nodo.position[0]-2)*len(datos_csv)+(nodo.position[1]-1)]
        if node_left:
            nodo.left = lista_nodos[(nodo.position[0]-1)*len(datos_csv)+(nodo.position[1]-2)]
        if node_down:
            nodo.up = lista_nodos[(nodo.position[0])*len(datos_csv)+(nodo.position[1]-1)]
        if node_right:
            nodo.left = lista_nodos[(nodo.position[0]-1)*len(datos_csv)+(nodo.position[1])]
    return lista_nodos

def imprimir_nodes(lista_nodos):
    i = 1
    for nodo in lista_nodos:
        print("-------DATOS NODO "+str(i)+"--------")
        print("Nodo arriba: "+nodo.up, )
def ejecucion(problema):
    datos = lectura_mapa()
    lista_nodos = crear_nodos(datos)
    imprimir_nodes(lista_nodos)


