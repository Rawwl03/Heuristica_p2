import csv
import sys
import time


class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

class Nodo:
    def __init__(self, nodo_arriba, nodo_abajo, nodo_izq, nodo_dcha, posicion):
        self.up = nodo_arriba
        self.down = nodo_abajo
        self.left = nodo_izq
        self.right = nodo_dcha
        self.posicion = posicion
        self.valor_heuristica = 0
        self.energia = 50
        self.recogidos_personas = [[],[]]
        self.mapa = []
        self.pos_personas = []
        self.coste_anadido = 0

class Problema:
    def __init__(self, pos_amb):
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.sol = []
        self.nodo_inicial = pos_amb
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
    lista_personas = []
    nodo_ambulancia = None
    for i in range(0, len(datos_csv)):
        for j in range(0, len(datos_csv[i])):
            nodo = Nodo(None, None, None, None, (i+1, j+1))
            if datos_csv[i][j]=='C' or datos_csv[i][j]=='N':
                lista_personas.append([(i+1,j+1),datos_csv[i][j]])
            if datos_csv[i][j] == 'P':
                nodo_ambulancia = nodo
            lista_nodos.append(nodo)
    for nodo in lista_nodos:
        node_up = False
        node_down = False
        node_right = False
        node_left = False
        if nodo.posicion[0] != 1:
            node_up = True
        if nodo.posicion[0] != len(datos_csv):
            node_down = True
        if nodo.posicion[1] != 1:
            node_left = True
        if nodo.posicion[1] != len(datos_csv[nodo.posicion[1]-1]):
            node_right = True
        if node_up:
            nodo.up = lista_nodos[(nodo.posicion[0]-2)*len(datos_csv)+(nodo.posicion[1]-1)]
        if node_left:
            nodo.left = lista_nodos[(nodo.posicion[0]-1)*len(datos_csv)+(nodo.posicion[1]-2)]
        if node_down:
            nodo.down = lista_nodos[(nodo.posicion[0])*len(datos_csv)+(nodo.posicion[1]-1)]
        if node_right:
            nodo.right = lista_nodos[(nodo.posicion[0]-1)*len(datos_csv)+(nodo.posicion[1])]
    #anadir_valor_heur(lista_nodos, heuristica)
    return lista_nodos, nodo_ambulancia, lista_personas

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
    lista_nodos, nodo_amb, pos_personas = crear_nodos(datos, heuristica)
    nodo_amb.mapa = datos
    nodo_amb.pos_personas = pos_personas
    problema = Problema(nodo_amb)
    tiempo_inicial = time.time()
    #imprimir_nodes(lista_nodos)
    solucion = algoritmo_heuristica1(problema, problema.nodo_inicial)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial

def algoritmo_heuristica1(problema, nodo_inicial):
    problema.lista_abierta = [(nodo_inicial, None)]
    solucion_encontrada = False
    iteracion = 0
    while len(problema.lista_abierta) > 0 and not solucion_encontrada:
        nodo_a_expandir = problema.lista_abierta.pop(0)
        if nodo_a_expandir[0].mapa[nodo_a_expandir[0].posicion[0]-1][nodo_a_expandir[0].posicion[1]-1] == "P" and len(nodo_a_expandir[0].pos_personas) == 0 and len(nodo_a_expandir[0].recogidos_personas[0])+len(nodo_a_expandir[0].recogidos_personas[1]) == 0:
          solucion_encontrada = True
          problema.lista_cerrada.append((nodo_a_expandir, None))
          estado_final = nodo_a_expandir
          break
        if iteracion > 0:
            nodo_valido = nodo_expandido(nodo_a_expandir[0])
            if nodo_valido:
                problema.lista_cerrada.append(nodo_a_expandir)
                for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down, nodo_a_expandir[0].left]:
                    if nodo:
                        nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                        nodo.energia = nodo_a_expandir[0].energia
                        nodo.recogidos_personas = nodo_a_expandir[0].recogidos_personas
                        nodo.mapa = nodo_a_expandir[0].mapa
                        nodo.pos_personas = nodo_a_expandir[0].pos_personas
                        tupla = (nodo, nodo_a_expandir[0])
                        resultado_nodo_in_lista = nodo_in_lista_abierta(nodo, problema.lista_abierta)
                        if not resultado_nodo_in_lista and not nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            problema.lista_abierta.append(tupla)
                        elif resultado_nodo_in_lista:
                            if resultado_nodo_in_lista[0].coste_anadido > tupla[0].coste_anadido:
                                problema.lista_abierta.remove(resultado_nodo_in_lista)
                                problema.lista_abierta.append(tupla)
                        elif nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            pass
        else:
            problema.lista_cerrada.append(nodo_a_expandir)
            for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down, nodo_a_expandir[0].left]:
                if nodo:
                    nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                    nodo.energia = nodo_a_expandir[0].energia
                    nodo.recogidos_personas = nodo_a_expandir[0].recogidos_personas
                    nodo.mapa = nodo_a_expandir[0].mapa
                    nodo.pos_personas = nodo_a_expandir[0].pos_personas
                    tupla = (nodo, nodo_a_expandir[0])
                    problema.lista_abierta.append(tupla)
        problema.lista_abierta = sorted(problema.lista_abierta, key=lambda x: x[0].coste_anadido)
        iteracion += 1
    if solucion_encontrada:
        solucion = camino_solucion(problema.lista_cerrada, estado_final)
        return solucion
    else:
        return "No hay solución :("


def camino_solucion(lista_cerrada, nodo):
    for tupla in lista_cerrada:
        nodo_actual, puntero = tupla
        if nodo_actual == nodo:
            ruta = [nodo_actual]
            while puntero is not None:
                for siguiente_tupla in lista_cerrada:
                    siguiente_nodo, siguiente_puntero = siguiente_tupla
                    if siguiente_nodo == puntero:
                        ruta.append(siguiente_nodo)
                        nodo_actual, puntero = siguiente_nodo, siguiente_puntero
                        break
                else:
                    break  # No se encontró un siguiente nodo, terminar la búsqueda
            return ruta[::-1]  # Invertir la ruta para que sea desde el nodo inicial hasta el final
    return None  # El nodo no está en la lista cerrada


def nodo_in_lista_abierta(nodo, lista_abierta):
    for nodo_abierta in lista_abierta:
        if nodo_abierta[0] == nodo:
            return nodo_abierta
    return None

def nodo_in_lista_cerrada(nodo, lista_cerrada):
    for nodo_abierta in lista_cerrada:
        if nodo_abierta[0] == nodo:
            return True
    return False


def nodo_expandido(nodo_a_expandir):
    valor_posicion = nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1]
    if valor_posicion == "X":
        return False
    else:
        if valor_posicion == "2":
            coste = 2
        else:
            coste = 1
        nodo_a_expandir.coste_anadido += coste
        nodo_a_expandir.energia -= coste
        if valor_posicion == "P" and (len(nodo_a_expandir.pos_personas) != 0 or len(nodo_a_expandir.recogidos_personas[0])+len(nodo_a_expandir.recogidos_personas[1]) != 0):
            nodo_a_expandir.energia = 50
        elif valor_posicion != "P" and nodo_a_expandir.energia <= 0:
            return False
        elif valor_posicion == "C":
            if len(nodo_a_expandir.recogidos_personas[1]) < 2:
                if nodo_a_expandir.recogidos_personas[1] and nodo_a_expandir.recogidos_personas[1][0] == "C":
                    nodo_a_expandir.recogidos_personas[1].append("C")
                    nodo_a_expandir.pos_personas.remove([nodo_a_expandir.posicion, valor_posicion])
                    nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1] = "1"
                elif not nodo_a_expandir.recogidos_personas[1]:
                    nodo_a_expandir.recogidos_personas[1].append("C")
                    nodo_a_expandir.pos_personas.remove([nodo_a_expandir.posicion, valor_posicion])
                    nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1] = "1"
        elif valor_posicion == "N":
            if len(nodo_a_expandir.recogidos_personas[0]) < 8:
                nodo_a_expandir.recogidos_personas[0].append("N")
                nodo_a_expandir.pos_personas.remove([nodo_a_expandir.posicion, valor_posicion])
                nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1] = "1"
            else:
                if len(nodo_a_expandir.recogidos_personas[1]) < 2:
                    if nodo_a_expandir.recogidos_personas[1] and nodo_a_expandir.recogidos_personas[1][0] == "N":
                        nodo_a_expandir.recogidos_personas[1].append("N")
                        nodo_a_expandir.pos_personas.remove([nodo_a_expandir.posicion, valor_posicion])
                        nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1] = "1"
                    elif not nodo_a_expandir.recogidos_personas[1]:
                        nodo_a_expandir.recogidos_personas[1].append("N")
                        nodo_a_expandir.pos_personas.remove([nodo_a_expandir.posicion, valor_posicion])
                        nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1] = "1"
        elif valor_posicion == "CN":
            for persona in nodo_a_expandir.recogidos_personas[0]:
                nodo_a_expandir.recogidos_personas[0].remove(persona)
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "N":
                    nodo_a_expandir.recogidos_personas[1].remove(persona)
        elif valor_posicion == "CC":
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "C":
                    nodo_a_expandir.recogidos_personas[1].remove(persona)
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise InputError("El comando en terminal debe seguir la siguiente estructura: python archivo.py <archivo.txt>")
    archivo_input=sys.argv[1]
    heuristica = sys.argv[2]
    ejecucion(archivo_input, heuristica)

