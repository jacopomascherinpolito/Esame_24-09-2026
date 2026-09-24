import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._compagnie = [None]
        self._dict_nodes = {}
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, soglia):
        n_aer = soglia
        self._compagnie = DAO.get_compagnie(n_aer)
        for c in self._compagnie:
            self._dict_nodes[c.ID] = c
        self.G.add_nodes_from(self._compagnie)

        self._edges = DAO.get_tratte()
        for e in self._edges:
            try:
                c1 = self._dict_nodes[e[0]]
                c2 = self._dict_nodes[e[1]]
                peso = int(e[2])
                if c1 in self._compagnie and c2 in self._compagnie:
                    self.G.add_edge(c1, c2, weight=peso)
            except KeyError:
                pass
        return self._compagnie, self._edges, self._dict_nodes

    def get_stats(self):
        return len(self.G.nodes()), len(self.G.edges())

    def vicini(self, idnodo):
        try:
            nodo = self._dict_nodes[int(idnodo)]
        except KeyError:
            pass
        vicini = nx.neighbors(self.G, nodo)
        for n in vicini:
            self.get_peso(nodo, n)
        return vicini


    def get_peso(self, nodo, n):
        peso = nx.get_edge_attributes(self.G,"weight")





