import csv, sys, time


class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

class Nodo:
    def __init__(self, nodo_arriba, nodo_abajo, nodo_izq, nodo_dcha, posicion, valor):
        self.up = nodo_arriba
        self.down = nodo_abajo
        self.left = nodo_izq
        self.right = nodo_dcha
        self.position = posicion
        self.value = valor
        self.valor_heuristica = 0

class Problema:
    def __init__(self, pos_amb):
        self.plazas = []
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.sol = []
        self.energia = 50
        self.posicion_ambulancia = pos_amb
        self.tiempo_total = 0

def lectura_mapa(archivo_input):
    try:
        with open(archivo_input, newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            datos_csv = list(lector_csv)
            data = [fila[0].split(';') for fila in datos_csv]
            return data
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_input}' no se encuentra.")
    except csv.Error as e:
        print(f"Error CSV: {e}")

def anadir_valor_heur(lista_nodos, heuristica):

    ...

def crear_nodos(datos_csv, heuristica):
    lista_nodos = []
    nodo_ambulancia = None
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
        if nodo.position[0] != len(datos_csv):
            node_down = True
        if nodo.position[1] != 1:
            node_left = True
        if nodo.position[1] != len(datos_csv[nodo.position[1]-1]):
            node_right = True
        if node_up:
            nodo.up = lista_nodos[(nodo.position[0]-2)*len(datos_csv)+(nodo.position[1]-1)]
        if node_left:
            nodo.left = lista_nodos[(nodo.position[0]-1)*len(datos_csv)+(nodo.position[1]-2)]
        if node_down:
            nodo.down = lista_nodos[(nodo.position[0])*len(datos_csv)+(nodo.position[1]-1)]
        if node_right:
            nodo.right = lista_nodos[(nodo.position[0]-1)*len(datos_csv)+(nodo.position[1])]
        if nodo.value == "P":
            nodo_ambulancia = nodo
    anadir_valor_heur(lista_nodos, heuristica)
    return lista_nodos, nodo_ambulancia

def imprimir_nodes(lista_nodos):
    i = 1
    for nodo in lista_nodos:
        print("-------DATOS NODO "+str(i)+"--------")
        if nodo.up:
            print("Nodo arriba: "+str(nodo.up.position))
        if nodo.left:
            print("Nodo izq: "+str(nodo.left.position))
        if nodo.right:
            print("Nodo dcha: "+str(nodo.right.position))
        if nodo.down:
            print("Nodo abajo: "+str(nodo.down.position))
        print("Valor: "+nodo.value+", Posicion: "+str(nodo.position))
        i += 1
def ejecucion(archivo_input, heuristica):

    datos = lectura_mapa(archivo_input)
    lista_nodos, nodo_amb = crear_nodos(datos, heuristica)
    problema = Problema(nodo_amb)
    tiempo_inicial = time.time()
    #imprimir_nodes(lista_nodos)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial

def algoritmo_heuristica1(lista_nodos, problema):



if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise InputError("El comando en terminal debe seguir la siguiente estructura: python archivo.py <archivo.txt>")
    archivo_input=sys.argv[1]
    heuristica = sys.argv[2]
    ejecucion(archivo_input, heuristica)

