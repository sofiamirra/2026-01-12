import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._constructors = []
        self._idMapConstructors = {}
        self._lista_archi = []

    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1, year2):
        self._graph.clear()
        self._idMapConstructors = {}
        nodes = DAO.getConstructors(year1, year2)
        self._graph.add_nodes_from(nodes)
        for c in nodes:
            self._idMapConstructors[c.constructorId] = c
        allEdges = DAO.getAllEdges(year1, year2, self._idMapConstructors)
        for e in allEdges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)
            self._lista_archi.append(e)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        """Restituisce i 3 archi con peso maggiore in ordine decrescente"""
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:3]

    def getComponentiConnesseDetails(self):
        # Conta quante "isole separate" ci sono nel grafo (A -- B -- C), (D -- F)
        # restituisce tutte le componenti, ogni componente è un insieme di nodi
        componenti = list(nx.connected_components(self._graph))

        # Prende la componente con più nodi
        largest = max(componenti, key=len)
        nodi_ordinati = sorted(largest, key=lambda n: self._graph.degree(n), reverse=True)

        return len(componenti), largest, nodi_ordinati



