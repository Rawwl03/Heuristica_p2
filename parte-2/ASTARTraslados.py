import csv
import sys
import time


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
        self.posicion = posicion
        self.value = valor
        self.valor_heuristica = 0
        self.energia = 50
        self.recogidos_personas= [[],[]]

class Problema:
    def __init__(self, pos_amb):
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.sol = []
        self.nodo_inicial = pos_amb
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
    lista_personas = []
    nodo_ambulancia = None
    for i in range(0, len(datos_csv)):
        for j in range(0, len(datos_csv[i])):
            nodo = Nodo(None, None, None, None, (i+1, j+1), datos_csv[i][j])
            if datos_csv[i][j]=='C' or datos_csv[i][j]=='N':
                lista_personas.append([(i+1,j+1),datos_csv[i][j]])
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
        if nodo.value == "P":
            nodo_ambulancia = nodo
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
    problema = Problema(nodo_amb)
    problema.pos_personas=pos_personas
    tiempo_inicial = time.time()
    #imprimir_nodes(lista_nodos)
    algoritmo_heuristica1(problema,problema.nodo_inicial)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial

def algoritmo_heuristica1(problema,nodo_inicial):
    problema.lista_abierta=[(nodo_inicial,0)]
    solucion_encontrada=False
    iteracion=0
    while len(problema.lista_abierta)>0 or not solucion_encontrada:
        nodo_a_expandir=problema.lista_abierta.pop(0)
        print(len(problema.pos_personas))
        if nodo_a_expandir[0].value == "P" and len(problema.pos_personas) == 0 and len(nodo_a_expandir[0].recogidos_personas[0])+len(nodo_a_expandir[0].recogidos_personas[1]) == 0:
          solucion_encontrada=True
          problema.lista_cerrada.append((nodo_a_expandir,nodo_anterior))
          break
        if iteracion==0:
            problema.lista_cerrada.append(nodo_a_expandir)
        else:
            problema.lista_cerrada.append((nodo_a_expandir,nodo_anterior))
        for nodo in [nodo_a_expandir[0].up,nodo_a_expandir[0].right,nodo_a_expandir[0].down,nodo_a_expandir[0].left] :
            if nodo:
                problema.coste_problema=nodo_a_expandir[1]
                nodo_valido=nodo_expandido(nodo,problema)
                if nodo_valido:
                    tupla=(nodo,problema.coste_problema)
                    resultado_nodo_in_lista=nodo_in_lista_abierta(tupla,problema.lista_abierta)
                    if not resultado_nodo_in_lista and not nodo_in_lista_cerrada(tupla,problema.lista_cerrada):
                        problema.lista_abierta.append((nodo,problema.coste_problema))
                    elif resultado_nodo_in_lista:
                        if resultado_nodo_in_lista[1]>tupla[1]:
                            problema.lista_abierta.remove(resultado_nodo_in_lista)
                            problema.lista_abierta.append(tupla)
                    elif nodo_in_lista_cerrada(tupla,problema.lista_cerrada):
                        pass
        problema.lista_abierta=sorted(problema.lista_abierta, key=lambda x: x[1])
        nodo_anterior=nodo_a_expandir
        iteracion+=1
    if solucion_encontrada:
        print(iteracion)
        for i in problema.lista_cerrada:
            print (i)
        solucion=camino_solucion(problema.lista_cerrada,nodo_a_expandir)
        for i in solucion:
            print(i)
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
                    if siguiente_puntero == nodo_actual:
                        ruta.append(siguiente_nodo)
                        nodo_actual, puntero = siguiente_nodo, siguiente_puntero
                        break
                else:
                    break  # No se encontró un siguiente nodo, terminar la búsqueda
            return ruta[::-1]  # Invertir la ruta para que sea desde el nodo inicial hasta el final
    return None  # El nodo no está en la lista cerrada


def nodo_in_lista_abierta(tupla,lista_abierta):
    for nodo_abierta in lista_abierta:
        if nodo_abierta[0] == tupla[0]:
            return nodo_abierta
    return None

def nodo_in_lista_cerrada(tupla,lista_cerrada):
    for nodo_abierta in lista_cerrada:
        if nodo_abierta[0] == tupla[0] and nodo_abierta[1] == tupla[1]:
            return True
    return False



def nodo_expandido(nodo_a_expandir, problema):
    if nodo_a_expandir.value == "X":
        return False
    else:
        if nodo_a_expandir.value == "2":
            coste = 2
        else:
            coste = 1
        nodo_a_expandir.energia -= coste
        problema.coste_problema+=coste
        if nodo_a_expandir.value == "P" and (len(problema.pos_personas) != 0 or len(nodo_a_expandir.recogidos_nc)+len(nodo_a_expandir.recogidos_c) != 0):
            nodo_a_expandir.energia = 50
        elif nodo_a_expandir.value != "P" and nodo_a_expandir.energia == 0:
            return False
        elif nodo_a_expandir.value == "C":
            if len(nodo_a_expandir.recogidos_personas[1]) < 2:
                if nodo_a_expandir.recogidos_personas[1] and nodo_a_expandir.recogidos_personas[1][0].value == "C":
                    nodo_a_expandir.recogidos_personas[1].append("C")
                    problema.pos_personas.remove([nodo_a_expandir.posicion,nodo_a_expandir.value])
                    nodo_a_expandir.value = "1"
                elif not nodo_a_expandir.recogidos_personas[1]:
                    nodo_a_expandir.recogidos_personas[1].append("C")
                    problema.pos_personas.remove([nodo_a_expandir.posicion,nodo_a_expandir.value])
                    nodo_a_expandir.value = "1"
        elif nodo_a_expandir.value == "N":
            if len(nodo_a_expandir.recogidos_personas[0]) < 8:
                nodo_a_expandir.recogidos_personas[0].append("N")
                problema.pos_personas.remove([nodo_a_expandir.posicion,nodo_a_expandir.value])
                nodo_a_expandir.value = "1"
            else:
                if len(nodo_a_expandir.recogidos_personas[1]) < 2:
                    if nodo_a_expandir.recogidos_personas[1] and nodo_a_expandir.recogidos_personas[1][0].value == "N":
                        nodo_a_expandir.recogidos_personas[1].append("N")
                        problema.pos_personas.remove([nodo_a_expandir.posicion,nodo_a_expandir.value])
                        nodo_a_expandir.value = "1"
                    elif not nodo_a_expandir.recogidos_personas[1]:
                        nodo_a_expandir.recogidos_personas[1].append("N")
                        problema.pos_personas.remove([nodo_a_expandir.posicion,nodo_a_expandir.value])
                        nodo_a_expandir.value = "1"
        elif nodo_a_expandir.value == "CN":
            for persona in nodo_a_expandir.recogidos_personas[0]:
                nodo_a_expandir.recogidos_personas[0].remove(persona)
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "N":
                    nodo_a_expandir.recogidos_personas[1].remove(persona)
        elif nodo_a_expandir.value == "CC":
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

