import csv
import sys
import time
import copy
import math

num_personas = 0

class InputError(Exception):
    def __init__(self, message="Input Inválido"):
        self.message = message
        super().__init__(self.message)

'''Clase nodo que representa un estado'''
class Nodo:
    def __init__(self, nodo_arriba, nodo_abajo, nodo_izq, nodo_dcha, posicion):
        """Los atributos up,down,left y rigth son apuntan a los nodos con una posicion adyacente"""
        self.up = nodo_arriba
        self.down = nodo_abajo
        self.left = nodo_izq
        self.right = nodo_dcha
        self.posicion = posicion
        self.valor_heuristica = 0
        self.energia = 50
        """Recogidas_personas[0] simboliza el espacio reservado para los pacientes no contagiados, y
        recogidos_personas[1] el espacio reservado para las personas contagiadas"""
        self.recogidos_personas = [[],[]]
        """En mapa se almacena el mapa actualizado con el valor de las casillas"""
        self.mapa = []
        """En pos_personas se almacenan las posiciones de los pacientes por recoger"""
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

    """Función para crear un nuevo_nodo a partir de uno dado. Esta función es útil para evitar actualizar
    que se sobreescriban los atributos de los nodos, ya que estan conectados por punteros"""
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

"""La clase problema almacena informacion general del problema, como el coste total la lista abierta
 y cerrada del problema, el nodo inical y el tiempo total de la ejecución del algoritmo"""
class Problema:
    def __init__(self, pos_amb):
        self.coste_problema = 0
        self.lista_abierta = []
        self.lista_cerrada = []
        self.sol = []
        self.nodo_inicial = pos_amb
        self.tiempo_total = 0

"""Función para leer el mapa del archivo inicial"""
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

"""Función para calcular la distancia manhattan entre dos posiciones, esta función se usa
a la hora de calcular la heuristica de la menor distancia al paciente mas cercano"""
def calcular_distancia(posicion1, posicion2):
    #Se calcula la distancia manhattan entre las dos posiciones
    return math.sqrt((posicion1[0] - posicion2[0]) ** 2 + (posicion1[1] - posicion2[1]) ** 2)

"""Función para calcular la heuristica de la distancia mas corta al paciente mas cercano"""
def distancia_paciente_mas_cercano(nodo):
    pacientes = [persona[0] for persona in nodo.pos_personas]

    # Calcular la distancia al paciente más cercano
    if not pacientes:
        return 0  # No hay pacientes, distancia cero

    distancia_mas_cercana = min(calcular_distancia(nodo.posicion, paciente) for paciente in pacientes)

    valor_heuristico =1 / distancia_mas_cercana if distancia_mas_cercana != 0 else float('inf')
    return valor_heuristico

"""Función para calcular el valor heurístico en función del valor de la heurística pasado por comandos"""
def anadir_valor_heur(nodo, heuristica):
    if heuristica == 1:
        valor_heuristico = len(nodo.recogidos_personas) + (num_personas-len(nodo.pos_personas))*2
        nodo.valor_heuristica = valor_heuristico
    elif heuristica ==2:
        valor_heuristico= distancia_paciente_mas_cercano(nodo)
        nodo.valor_heuristica = valor_heuristico
    else:
        nodo.valor_heuristica=0

"""Función para crear los nodos del problema"""
def crear_nodos(datos_csv):
    global num_personas
    lista_nodos = []
    lista_personas = []
    nodo_ambulancia = None
    for i in range(0, len(datos_csv)):
        for j in range(0, len(datos_csv[i])):
            nodo = Nodo(None, None, None, None, (i+1, j+1))
            if datos_csv[i][j] == 'C' or datos_csv[i][j] == 'N':
                lista_personas.append([(i+1, j+1), datos_csv[i][j]])
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

"""Función para escribir la salida"""
def escritura_salida(solucion, nodos_exp, problema, salidas, mapa):
    with open("ASTAR-tests/" + salidas[0], 'w', encoding='utf-8') as archivo:
        if len(solucion) > 0:
            for nodo in solucion:
                linea = "(" + str(nodo[0].posicion[0]) + "," + str(nodo[0].posicion[1]) + ") :" + \
                        mapa[nodo[0].posicion[0] - 1][nodo[0].posicion[1] - 1] + ":" + str(nodo[0].energia) + "\n"
                if mapa[nodo[0].posicion[0] - 1][nodo[0].posicion[1] - 1] == "C" or mapa[nodo[0].posicion[0] - 1][
                    nodo[0].posicion[1] - 1] == "N":
                    mapa[nodo[0].posicion[0] - 1][nodo[0].posicion[1] - 1] = "1"
                archivo.write(linea)
        else:
            linea = "No se ha encontrado una solución que satisfaga el modelo\n"
            archivo.write(linea)
    with open("ASTAR-tests/"+salidas[1], 'w') as archivo:
        if len(solucion) == 0:
            text = "Tiempo total: "+str(problema.tiempo_total)+"\nCoste total: "+str(problema.coste_problema)+"\nLongitud del plan: "+str(len(solucion))+"\nNodos expandidos: "+str(nodos_exp)
            archivo.write(text)
        else:
            text = "Tiempo total: " + str(problema.tiempo_total) + "\nCoste total: " + str(problema.coste_problema) + "\nLongitud del plan: " + str(len(solucion)-1) + "\nNodos expandidos: " + str(nodos_exp)
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

"""Función que crea los nodos del modelo y realiza la ejecución del algoritmo a estrella"""
def ejecucion(archivo_input, heuristica, salidas):
    datos = lectura_mapa(archivo_input)
    lista_nodos, nodo_amb, pos_personas = crear_nodos(datos)
    nodo_amb.mapa = datos
    nodo_amb.pos_personas = pos_personas
    problema = Problema(nodo_amb)
    tiempo_inicial = time.time()
    solucion, nodos_exp = algoritmo_A(problema, problema.nodo_inicial, heuristica)
    marca_tiempo = time.time()
    problema.tiempo_total = marca_tiempo - tiempo_inicial
    escritura_salida(solucion, nodos_exp, problema, salidas, datos)
    print("\nEjecución terminada.\nLa solución se ha guardado en parte-2/ASTAR-salidas/"+salidas[0]+" y las estadísticas en parte-2/ASTAR-salidas/"+salidas[1])

"""Función que ejecuta el algoritmo  estrella"""
def algoritmo_A(problema, nodo_inicial, heuristica):
    """Se inicializa la lista abierta con el nodo inicial"""
    problema.lista_abierta = [(nodo_inicial, None)]
    solucion_encontrada = False
    iteracion = 0
    nodos_expandidos = 0
    """Mientras que no se haya encontrada la solución y la lista abierta no esté vacía se sigue buscando la solución"""
    while len(problema.lista_abierta) > 0 and not solucion_encontrada:
        """Se elimina el primer nodo de la lista_cerrada (el nodo con mejor f(n), y se comprueba si es el estado final, en cuyo caso se deja de iterar)"""
        nodo_a_expandir = problema.lista_abierta.pop(0)
        if nodo_a_expandir[0].mapa[nodo_a_expandir[0].posicion[0]-1][nodo_a_expandir[0].posicion[1]-1] == "P" and len(nodo_a_expandir[0].pos_personas) == 0 and len(nodo_a_expandir[0].recogidos_personas[0])+len(nodo_a_expandir[0].recogidos_personas[1]) == 0:
          solucion_encontrada = True
          problema.lista_cerrada.append((nodo_a_expandir, None))
          estado_final = nodo_a_expandir
          break
        """Si no es el nodo final se añade el nodo actual a la lista,cerrada"""
        problema.lista_cerrada.append(nodo_a_expandir)
        for nodo in [nodo_a_expandir[0].up, nodo_a_expandir[0].right, nodo_a_expandir[0].down, nodo_a_expandir[0].left]:
            if nodo:
                """Para cada nodo con una posición adyacente se crea un nuevo nodo, con la energia,coste_anadido,recogidos_personas,mapa y pos_personas del padre"""
                nodo = nodo.crear_nuevo_nodo()
                nodo.coste_anadido = nodo_a_expandir[0].coste_anadido
                nodo.energia = nodo_a_expandir[0].energia
                nodo.recogidos_personas = copy.deepcopy(nodo_a_expandir[0].recogidos_personas)
                nodo.mapa = copy.deepcopy(nodo_a_expandir[0].mapa)
                nodo.pos_personas = copy.deepcopy(nodo_a_expandir[0].pos_personas)
                """Y se comprueba que al expandirse genere un nodo válido, llamando a nodo_expandido()"""
                nodo_valido = nodo_expandido(nodo)
                nodos_expandidos += 1
                if nodo_valido:
                    """Si el nodo es válido se procede a añadirle el valor heuristico y se busca si ya está en la lista 
                    abierta o en la lista cerrada del problema"""
                    anadir_valor_heur(nodo, heuristica)
                    tupla = (nodo, nodo_a_expandir[0])
                    if iteracion > 0:
                        resultado_nodo_in_lista_abierta = nodo_in_lista(nodo, problema.lista_abierta)
                        """Si no está ni en la lista abierta, ni en la cerrada se añade directamente a la lista abierta"""
                        if not resultado_nodo_in_lista_abierta and not nodo_in_lista(nodo, problema.lista_cerrada):
                            problema.lista_abierta.append(tupla)
                        #Si está en la lista abierta, se comprueba cual de los dos tiene una mejor f(n)
                        elif resultado_nodo_in_lista_abierta:
                            if resultado_nodo_in_lista_abierta[0].coste_anadido - resultado_nodo_in_lista_abierta[0].valor_heuristica > nodo.coste_anadido - nodo.valor_heuristica:
                                problema.lista_abierta.remove(resultado_nodo_in_lista_abierta)
                                problema.lista_abierta.append(tupla)
                        #Si ya está en la lista cerrada, no se hace nada
                        elif nodo_in_lista(nodo, problema.lista_cerrada):
                            pass
                    else:
                        problema.lista_abierta.append(tupla)
        """Al acabar cada iteración se reordena la lista abierta, para que en la siguiente iteración el primer elemento sea aquel con mejor f(n)"""
        problema.lista_abierta = sorted(problema.lista_abierta, key=lambda x: x[0].coste_anadido - x[0].valor_heuristica)
        iteracion += 1
    if solucion_encontrada:
        problema.coste_problema = estado_final[0].coste_anadido
        """Si hay solución se invoca a camino_solución para encontrar el camino de la solución"""
        solucion = camino_solucion(problema.lista_cerrada, estado_final)
        return solucion, nodos_expandidos
    else:
        return [], nodos_expandidos

"""Función para buscar el camino de la solución"""
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

"""Función para comprobr si un nodo está en la lista (cerrada o abierta) pasado por argumentos"""
def nodo_in_lista(nodo, lista):
    for nodo_lista in lista:
        if nodo_lista[0] == nodo:
            return nodo_lista
    return None

"""Función que expande un nodo teniendo en cuenta los diferentes operadores"""
def nodo_expandido(nodo_a_expandir):
    valor_posicion = nodo_a_expandir.mapa[nodo_a_expandir.posicion[0]-1][nodo_a_expandir.posicion[1]-1]
    """Si el valor en el mapa es una X no es un estado válido"""
    if valor_posicion == "X":
        return False
    else:
        try:
            coste = int(valor_posicion)
        except ValueError:
            coste = 1
        """Se actualiza el coste añadido y la energía del nodo actual"""
        nodo_a_expandir.coste_anadido += coste
        nodo_a_expandir.energia -= coste
        """Si llega al parking y todavía faltan pacientes por recoger o la ambulancia no está vacía se recarga la energía"""
        if valor_posicion == "P" and (len(nodo_a_expandir.pos_personas) != 0 or len(nodo_a_expandir.recogidos_personas[0])+len(nodo_a_expandir.recogidos_personas[1]) != 0):
            nodo_a_expandir.energia = 50
        #Si se acaba la energía se genera un estado no válido, es decir, se devuelve false
        elif valor_posicion != "P" and nodo_a_expandir.energia <= 0:
            return False
        #Si la casilla tiene el valor C se añade el paciente a recogidos_personas[1] si hay hueco y se elimina a su
        #vez dicho paciente de pos_personas. Además se actualiza el valor en el mapa de esa casilla a 1 para que
        #no se vuelva a recoger al paciente
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
        #Si la casilla tiene el valor N se añade el paciente a recogidos_personas[0] si hay hueco y no se
        # ha recogido ya a un paciente del tipo "N". Si recogidos_personas[0] está lleno
        # Se comprueba que en recogidos_personas[1] haya hueco y no hya ningún paciente "C", para guardar al paciente en
        # dicha posicion.En caso de recogerse se elimina a su vez dicho paciente de pos_personas
        #. Además se actualiza el valor en el mapa de esa casilla a 1 para que
        #no se vuelva a recoger al paciente
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
        #Si la casilla tiene valor CN se vacía recogidos_personas[0] si no hay ningún
        #paciente C en recogidas_personas[1].Además en el caso anterior, se vacía
        #recogidos_personas[1]
        elif valor_posicion == "CN":
            contag_recogido = False
            for persona in nodo_a_expandir.recogidos_personas[1]:
                if persona == "C":
                    contag_recogido = True
            if not contag_recogido:
                nodo_a_expandir.recogidos_personas[0] = []
                nodo_a_expandir.recogidos_personas[1] = []
        #Si la casilla tiene valor CC se vacía recogidos_personas[1]
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

