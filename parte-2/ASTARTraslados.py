import csv
import sys
import time
import copy

num_personas = 0

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

    def __eq__(self, other):
        if isinstance(other, Nodo):
            return self.posicion == other.posicion and \
                   self.energia == other.energia and \
                   self.recogidos_personas == other.recogidos_personas and \
                   self.mapa == other.mapa and \
                   self.pos_personas == other.pos_personas
        return False

    def crear_nuevo_nodo(self):
        nuevo_nodo = Nodo(
            self.up, self.down,
            self.left, self.right,
            self.posicion
        )
        nuevo_nodo.valor_heuristica = self.valor_heuristica
        nuevo_nodo.energia = self.energia
        nuevo_nodo.recogidos_personas = [copy.deepcopy(personas) for personas in self.recogidos_personas]
        nuevo_nodo.mapa = [copy.deepcopy(fila) for fila in self.mapa]
        nuevo_nodo.pos_personas = copy.deepcopy(self.pos_personas)
        nuevo_nodo.coste_anadido = self.coste_anadido
        return nuevo_nodo

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

def anadir_valor_heur(nodo, heuristica):
    if heuristica == 1:
        valor_heuristico = len(nodo.recogidos_personas) + (num_personas-len(nodo.pos_personas))*2
        nodo.valor_heuristica = valor_heuristico
    else:
        ...

def crear_nodos(datos_csv):
    global num_personas
    lista_nodos = []
    lista_personas = []
    nodo_ambulancia = None
    for i in range(0, len(datos_csv)):
        for j in range(0, len(datos_csv[i])):
            nodo = Nodo(None, None, None, None, (i+1, j+1))
            if datos_csv[i][j]=='C' or datos_csv[i][j]=='N':
                lista_personas.append([(i+1,j+1),datos_csv[i][j]])
                num_personas += 1
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
        if nodo.posicion[1] != len(datos_csv[nodo.posicion[0]-1]):
            node_right = True
        if node_up:
            nodo.up = lista_nodos[(nodo.posicion[0]-2)*len(datos_csv[nodo.posicion[0]-1])+(nodo.posicion[1]-1)]
        if node_left:
            nodo.left = lista_nodos[(nodo.posicion[0]-1)*len(datos_csv[nodo.posicion[0]-1])+(nodo.posicion[1]-2)]
        if node_down:
            nodo.down = lista_nodos[(nodo.posicion[0])*len(datos_csv[nodo.posicion[0]-1])+(nodo.posicion[1])-1]
        if node_right:
            nodo.right = lista_nodos[(nodo.posicion[0]-1)*len(datos_csv[nodo.posicion[0]-1])+(nodo.posicion[1])]
    #anadir_valor_heur(lista_nodos, heuristica)
    return lista_nodos, nodo_ambulancia, lista_personas

def escritura_salida(solucion, nodos_exp, problema, salidas, mapa):
    with open("ASTAR-salidas/"+salidas[0], 'w') as archivo:
        for nodo in solucion:
            linea = "("+str(nodo[0].posicion[0])+","+str(nodo[0].posicion[1])+") :"+mapa[nodo[0].posicion[0]-1][nodo[0].posicion[1]-1]+":"+str(nodo[0].energia)+"\n"
            if mapa[nodo[0].posicion[0]-1][nodo[0].posicion[1]-1] == "C" or mapa[nodo[0].posicion[0]-1][nodo[0].posicion[1]-1] == "N":
                mapa[nodo[0].posicion[0] - 1][nodo[0].posicion[1] - 1] = "1"
            archivo.write(linea)
    with open("ASTAR-salidas/"+salidas[1], 'w') as archivo:
        text = "Tiempo total: "+str(problema.tiempo_total)+"\nCoste total: "+str(problema.coste_problema)+"\nLongitud del plan: "+str(len(solucion)-1)+"\nNodos expandidos: "+str(nodos_exp)
        archivo.write(text)

def imprimir_nodes(lista_nodos):
    i = 1
    for nodo in lista_nodos:
        print("-------DATOS NODO "+str(i)+"--------")
        if nodo.up:
            print("Nodo arriba: "+str(nodo.up.posicion))
        if nodo.left:
            print("Nodo izq: "+str(nodo.left.posicion))
        if nodo.right:
            print("Nodo dcha: "+str(nodo.right.posicion))
        if nodo.down:
            print("Nodo abajo: "+str(nodo.down.posicion))
        print("Posicion: "+str(nodo.posicion))
        i += 1

def ejecucion(archivo_input, heuristica, salidas):
    datos = lectura_mapa(archivo_input)
    lista_nodos, nodo_amb, pos_personas = crear_nodos(datos)
    nodo_amb.mapa = datos
    nodo_amb.pos_personas = pos_personas
    problema = Problema(nodo_amb)
    tiempo_inicial = time.time()
    #imprimir_nodes(lista_nodos)
    solucion, nodos_exp = algoritmo_heuristica1_prueba(problema, problema.nodo_inicial, heuristica)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial
    escritura_salida(solucion, nodos_exp, problema, salidas, datos)
    print("\nEjecución terminada.\nLa solución se ha guardado en parte-2/ASTAR-salidas/"+salidas[0]+" y las estadísticas en parte-2/ASTAR-salidas/"+salidas[1])

def algoritmo_heuristica1(problema, nodo_inicial, heuristica):
    problema.lista_abierta = [(nodo_inicial, None)]
    solucion_encontrada = False
    iteracion = 0
    nodos_expandidos = 0
    while len(problema.lista_abierta) > 0 and not solucion_encontrada:
        nodo_a_expandir = problema.lista_abierta.pop(0)
        if nodo_a_expandir[0].mapa[nodo_a_expandir[0].posicion[0]-1][nodo_a_expandir[0].posicion[1]-1] == "P" and len(nodo_a_expandir[0].pos_personas) == 0 and len(nodo_a_expandir[0].recogidos_personas[0])+len(nodo_a_expandir[0].recogidos_personas[1]) == 0:
          solucion_encontrada = True
          problema.lista_cerrada.append((nodo_a_expandir, None))
          estado_final = nodo_a_expandir
          break
        problema.lista_cerrada.append(nodo_a_expandir)
        for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down, nodo_a_expandir[0].left]:
            if nodo:
                nodo = nodo.crear_nuevo_nodo()
                nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                nodo.energia = nodo_a_expandir[0].energia
                nodo.recogidos_personas = copy.deepcopy(nodo_a_expandir[0].recogidos_personas)
                nodo.mapa = copy.deepcopy(nodo_a_expandir[0].mapa)
                nodo.pos_personas = copy.deepcopy(nodo_a_expandir[0].pos_personas)
                nodo_valido = nodo_expandido(nodo)
                nodos_expandidos+=1
                if nodo_valido:
                    anadir_valor_heur(nodo, heuristica)
                    tupla = (nodo, nodo_a_expandir[0])
                    if iteracion > 0:
                        resultado_nodo_in_lista = nodo_in_lista_abierta(nodo, problema.lista_abierta)
                        if not resultado_nodo_in_lista and not nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            problema.lista_abierta.append(tupla)
                        elif resultado_nodo_in_lista:
                            if resultado_nodo_in_lista[0].coste_anadido - resultado_nodo_in_lista[0].valor_heuristica > tupla[0].coste_anadido - tupla[0].valor_heuristica:
                                problema.lista_abierta.remove(resultado_nodo_in_lista)
                                problema.lista_abierta.append(tupla)
                        elif nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            pass
                    else:
                        problema.lista_abierta.append(tupla)
        problema.lista_abierta = sorted(problema.lista_abierta, key=lambda x: x[0].coste_anadido - x[0].valor_heuristica)
        iteracion += 1
    if solucion_encontrada:
        problema.coste_problema = estado_final[0].coste_anadido
        solucion = camino_solucion(problema.lista_cerrada, estado_final)
        return solucion, nodos_expandidos
    else:
        return "No hay solución :("


def algoritmo_heuristica1_prueba(problema, nodo_inicial, heuristica):
    problema.lista_abierta = [(nodo_inicial, None)]
    solucion_encontrada = False
    iteracion = 0
    nodos_expandidos = 0
    while len(problema.lista_abierta) > 0 and not solucion_encontrada:
        nodo_a_expandir = problema.lista_abierta.pop(0)
        if nodo_a_expandir[0].mapa[nodo_a_expandir[0].posicion[0]-1][nodo_a_expandir[0].posicion[1]-1] == "P" and len(nodo_a_expandir[0].pos_personas) == 0 and len(nodo_a_expandir[0].recogidos_personas[0])+len(nodo_a_expandir[0].recogidos_personas[1]) == 0:
          solucion_encontrada = True
          nodo_a_expandir[0].coste_anadido += 1
          nodo_a_expandir[0].energia -= 1
          problema.lista_cerrada.append((nodo_a_expandir, None))
          estado_final = nodo_a_expandir
          break
        problema.lista_cerrada.append(nodo_a_expandir)
        if iteracion > 0:
            nodo_valido = nodo_expandido(nodo_a_expandir[0])
            nodos_expandidos += 1
            if nodo_valido:
                for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down, nodo_a_expandir[0].left]:
                    if nodo:
                        nodo = nodo.crear_nuevo_nodo()
                        nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                        nodo.energia = nodo_a_expandir[0].energia
                        nodo.recogidos_personas = copy.deepcopy(nodo_a_expandir[0].recogidos_personas)
                        nodo.mapa = copy.deepcopy(nodo_a_expandir[0].mapa)
                        nodo.pos_personas = copy.deepcopy(nodo_a_expandir[0].pos_personas)
                        anadir_valor_heur(nodo, heuristica)
                        tupla = (nodo, nodo_a_expandir[0])
                        resultado_nodo_in_lista = nodo_in_lista_abierta(nodo, problema.lista_abierta)
                        if not resultado_nodo_in_lista and not nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            problema.lista_abierta.append(tupla)
                        elif resultado_nodo_in_lista:
                            if resultado_nodo_in_lista[0].coste_anadido - resultado_nodo_in_lista[0].valor_heuristica > tupla[0].coste_anadido - tupla[0].valor_heuristica:
                                problema.lista_abierta.remove(resultado_nodo_in_lista)
                                problema.lista_abierta.append(tupla)
                        elif nodo_in_lista_cerrada(tupla, problema.lista_cerrada):
                            pass
        else:
            for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down,
                         nodo_a_expandir[0].left]:
                if nodo:
                    nodo = nodo.crear_nuevo_nodo()
                    nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                    nodo.energia = nodo_a_expandir[0].energia
                    nodo.recogidos_personas = copy.deepcopy(nodo_a_expandir[0].recogidos_personas)
                    nodo.mapa = copy.deepcopy(nodo_a_expandir[0].mapa)
                    nodo.pos_personas = copy.deepcopy(nodo_a_expandir[0].pos_personas)
                    anadir_valor_heur(nodo, heuristica)
                    tupla = (nodo, nodo_a_expandir[0])
                    problema.lista_abierta.append(tupla)
        problema.lista_abierta = sorted(problema.lista_abierta, key=lambda x: x[0].coste_anadido - x[0].valor_heuristica)
        iteracion += 1
    if solucion_encontrada:
        problema.coste_problema = estado_final[0].coste_anadido
        solucion = camino_solucion(problema.lista_cerrada, estado_final)
        return solucion, nodos_expandidos
    else:
        return "No hay solución :("


def camino_solucion(lista_cerrada, nodo_final):
    camino = []
    actual = nodo_final
    while actual[1] is not None:
        # Buscar la tupla que contiene el nodo actual
        for tupla in lista_cerrada:
            if tupla[0] == actual[1]:
                camino.append(actual)
                actual = tupla
                break  # Salir del bucle una vez que se ha encontrado la tupla
    camino.append(actual)
    return camino[::-1]


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
        try:
            coste = int(valor_posicion)
        except ValueError:
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
            contag_recogido = False
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "C":
                    contag_recogido = True
            if not contag_recogido:
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
            contag_recogido = False
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "C":
                    contag_recogido = True
            if not contag_recogido:
                nodo_a_expandir.recogidos_personas[0]=[]
                if len(nodo_a_expandir.recogidos_personas[1])>0:
                    for persona in nodo_a_expandir.recogidos_personas[1]:
                        nueva_lista=[]
                        if persona == "C":
                            nueva_lista.append(persona)
                    nodo_a_expandir.recogidos_personas[1]=copy.deepcopy(nueva_lista)
        elif valor_posicion == "CC":
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "C":
                    nodo_a_expandir.recogidos_personas[1] = []
                    break
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise InputError("El comando en terminal debe seguir la siguiente estructura: python archivo.py <archivo.csv> <num-h>")
    archivo_input = sys.argv[1]
    heuristica = int(sys.argv[2])
    arch = archivo_input.split("/")
    mapa = arch[len(arch)-1]
    nameMap = mapa.split(".")
    salida_fichero_solution, salida_fichero_stat = nameMap[0]+"-"+str(heuristica)+".output",  nameMap[0]+"-"+str(heuristica)+".stat"
    salidas_nombres = (salida_fichero_solution, salida_fichero_stat)
    ejecucion(archivo_input, heuristica, salidas_nombres)

