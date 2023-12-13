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

class Ambulancia:
    def __init__(self, posicion):
        self.energia = 50
        self.posicion = posicion
        self.recogidos_personas = [[],[]]

class Problema:
    def __init__(self, pos_amb):
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.sol = []
        self.posicion_ambulancia = Ambulancia(pos_amb)
        self.tiempo_total = 0
        self.pos_personas = []


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
    #anadir_valor_heur(lista_nodos, heuristica)
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
    imprimir_nodes(lista_nodos)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial

def algoritmo_heuristica1(lista_nodos, problema):
    ...


def nodo_expandido(nodo_a_expandir, problema):
    if nodo_a_expandir.value == "X":
        return False
    else:
        if nodo_a_expandir.value == "2":
            coste = 2
        else:
            coste = 1
        problema.ambulancia.energia -= coste
        if nodo_a_expandir.value == "P" and len(problema.pos_personas) == 0 and len(problema.ambulancia.recogidos_personas[0])+len(problema.ambulancia.recogidas_personas[1]) == 0:
            return True
        elif nodo_a_expandir.value == "P" and (len(problema.pos_personas) != 0 or len(problema.ambulancia.recogidos_nc)+len(problema.ambulancia.recogidos_c) != 0):
            problema.ambulancia.energia = 50
        elif nodo_a_expandir.value != "P" and problema.ambulancia.energia == 0:
            return False
        elif nodo_a_expandir.value == "C":
            if len(problema.ambulancia.recogidos_personas[1]) < 2:
                if problema.ambulancia.recogidos_personas[1][0] and problema.ambulancia.recogidos_personas[1][0].value == "C":
                    problema.ambulancia.recogidos_personas[1].append("C")
                    problema.pos_personas.remove(nodo_a_expandir)
                    nodo_a_expandir.value = "1"
                elif not problema.ambulancia.recogidos_personas[1][0]:
                    problema.ambulancia.recogidos_personas[1].append("C")
                    problema.pos_personas.remove(nodo_a_expandir)
                    nodo_a_expandir.value = "1"
                else:
                    return False
        elif nodo_a_expandir.value == "N":
            if len(problema.ambulancia.recogidos_personas[0]) < 8:
                problema.ambulancia.recogidos_personas[0].append("N")
                problema.pos_personas.remove(nodo_a_expandir)
                nodo_a_expandir.value = "1"
            else:
                if len(problema.ambulancia.recogidos_personas[1]) < 2:
                    if problema.ambulancia.recogidos_personas[1][0] and problema.ambulancia.recogidos_personas[1][0].value == "N":
                        problema.ambulancia.recogidos_personas[1].append("N")
                        problema.pos_personas.remove(nodo_a_expandir)
                        nodo_a_expandir.value = "1"
                    elif not problema.ambulancia.recogidos_personas[1][0]:
                        problema.ambulancia.recogidos_personas[1].append("N")
                        problema.pos_personas.remove(nodo_a_expandir)
                        nodo_a_expandir.value = "1"
                    else:
                        return False
        elif nodo_a_expandir.value == "CN":
            for persona in problema.ambulancia.recogidos_personas[0]:
                problema.ambulancia.recogidos_personas[0].remove(persona)
            for persona in problema.ambulancia.recogidos_personas[1]:
                if persona == "N":
                    problema.ambulancia.recogidos_personas[1].remove(persona)
        elif nodo_a_expandir.value == "CC":
            for persona in problema.ambulancia.recogidos_personas[1]:
                if persona == "C":
                    problema.ambulancia.recogidos_personas[1].remove(persona)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise InputError("El comando en terminal debe seguir la siguiente estructura: python archivo.py <archivo.txt>")
    archivo_input=sys.argv[1]
    heuristica = sys.argv[2]
    ejecucion(archivo_input, heuristica)

