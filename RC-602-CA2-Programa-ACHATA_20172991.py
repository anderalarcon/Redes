from collections import deque
INFINITY = float("inf")


class Graph:
    def __init__(self, filename):
        """1.Leemos el archivo txt y lo guardamos en una lista[desde, hacia,distancia]. Esto es un paso previo antes de entrar a la funcion prinpipal

        self.nodos-> representa un conjunto de todos los nodos únicos en el gráfico
        self.lista_adjacencia-> representa un diccionario que asigna cada nodo a un conjunto desordenado de tuplas (vecino, distancia).
        """
        # STRIP -> elimina espacios; SPLIT-> para los saltos de linea en el txt, UPDATE -> pushea en un diccionario

        print("Grafo inicial insertado del archivo .txt sin formato:")
        grafo_nodos = []
        with open(filename) as fhandle:
            for line in fhandle:
                edge_from, edge_to, cost, *_ = line.strip().split(" ")
                grafo_nodos.append((edge_from, edge_to, float(cost)))
        print(grafo_nodos)
        print("-----------------------------------------------------------------------------------------------------------------")

        print("Separamos los nodos: ")
        self.nodos = set()
        for edge in grafo_nodos:
            self.nodos.update([edge[0], edge[1]])
        print(self.nodos)
        print("-----------------------------------------------------------------------------------------------------------------")

        print("Usamos los nodos separados y les asignamos un espacio que va ser llenado luego:")
        self.lista_adjacencia = {node: set() for node in self.nodos}
        print(self.lista_adjacencia)
        print("-----------------------------------------------------------------------------------------------------------------")
        print("LLenamos los espacios asignados con sus veciones y distancias en tuplas:")
        for edge in grafo_nodos:
            self.lista_adjacencia[edge[0]].add((edge[1], edge[2]))
        print(self.lista_adjacencia)

    # Funcion Dijkstra, el cual recibe como parametros un nodo inicial, nodo final y retorna una tuplac (ruta,distancia)
    def ruta_mas_corta(self, nodo_inicial, nodo_final):
        # Seteamos todos los nodos como no visitados
        nodos_no_visitados = self.nodos.copy()

        # Creamos un diccionario de cada nodo desde nodo_inicial. Actualizaremos la distancia de cada nodo siempre que encontremos una ruta más corta.
        distancia_desde_inicio = {
            node: (0 if node == nodo_inicial else INFINITY) for node in self.nodos
        }

        # Inicializamos nodo_previo, el diccionario que mapea,recorre nodo en nodo que fue visitado de la ruta mas corta
        nodo_previo = {node: None for node in self.nodos}
        entradas_a_bucle = 0
        revision_nodos = 0
        while nodos_no_visitados:
            revision_nodos = revision_nodos+1
            # Seteamos el nodo_actual al nodo no visitado con la ruta más corta
            nodo_actual = min(
                nodos_no_visitados, key=lambda node: distancia_desde_inicio[node]
            )
            nodos_no_visitados.remove(nodo_actual)

            # Si la distancia del nodo actual es infinita, los nodos sin visitar faltante no son conectados al nodo incial y termina
            if distancia_desde_inicio[nodo_actual] == INFINITY:
                break

            # Por cada vecino de nodo_actual, comprobamos si la distancia al vecion via nodo_actual es menor que la distancia actual para ese nodo. Si lo es actualizamos los valores

            for vecino, distancia in self.lista_adjacencia[nodo_actual]:
                nuevo_camino = distancia_desde_inicio[nodo_actual] + distancia
                entradas_a_bucle = entradas_a_bucle+1
                if nuevo_camino < distancia_desde_inicio[vecino]:
                    distancia_desde_inicio[vecino] = nuevo_camino
                    nodo_previo[vecino] = nodo_actual

            if nodo_actual == nodo_final:
                break  # Aca acabaría puesto que visitamos todos los nodos

        # Para construir la ruta , se iteraron los nodos desde el nodo final al nodo icnial
       
        ruta = deque()
        nodo_actual = nodo_final
        while nodo_previo[nodo_actual] is not None:
            ruta.appendleft(nodo_actual)
            nodo_actual = nodo_previo[nodo_actual]
        ruta.appendleft(nodo_inicial)
        return ruta, distancia_desde_inicio[nodo_final]


def main():


    print("=========================ESCENARIO COMPLEJIDAD BASICA==========================")
    verify_algorithm(
        filename="basica.txt",
        start="A",
        end="G",
    )

    print("========================ESCENARIO COMPLEJIDAD MEDIA=========================")
    verify_algorithm(
        filename="media.txt",
        start="A",
        end="J",
    )




def verify_algorithm(filename, start, end):
    graph = Graph(filename)
    ruta_retornada, distancia_retornada = graph.ruta_mas_corta(start, end)
    print("-------------------Resultados---------------------")
    print('Inicio/Fin Nodos: {0} -> {1}'.format(start, end))
    print('Camino mas corto: {0}'.format(list(ruta_retornada)))
    print('Distancia Total: {0}'.format(distancia_retornada))


if __name__ == "__main__":
    main()
