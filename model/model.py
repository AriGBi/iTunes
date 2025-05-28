import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo= nx.Graph()
        self._allNodi=[]
        self._idMapAlbum={}
        self._bestSet={}
        self._maxLen=0


    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi= DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum={n.AlbumId: n for n in self._allNodi}
        self._allEdges= DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

    def getSetOfNodes(self, a1, soglia):
        self._bestSet = {}
        self._maxLen = 0
        parziale={a1}
        cc=nx.node_connected_component(self._grafo, a1)

        cc.remove(a1) #tanto a1 l'ho già inserito in parziale e quindi non ho bisongo di tenerlo nella cc e iterarci di nuovo
        for n in cc:
            parziale.add(n)
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia)
            parziale.remove(n) #backtracking
            cc.add(n)

        return self._bestSet, self._getDurataTot(self._bestSet)

    def _ricorsione(self, parziale, rimanenti, soglia): #tutti i nodi della componente connessa sono i rimanenti che posso ancora aggiungere
        if self._getDurataTot(parziale)>soglia: #non posso considerare parziale
            return #evito di andare avanti
        if len(parziale)>self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet=copy.deepcopy(parziale)
            #non devo interrompere la ricorsione, non metto return. Perchè potrebbe esserci ancora qualcosa di migliore
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n) #lo tolgo così so che non lo riguarda nel corso della sua ricorsione
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n) #lo riaggiungo perchè per le altre ricorsioni deve esserci





    def getInfoConnessa(self, a1):
        cc= nx.node_connected_component(self._grafo, a1)
        return len(cc), self._getDurataTot(cc)

    def _getDurataTot(self, listOfNodes):
        sumDurata=0
        for n in listOfNodes:
            sumDurata+=n.dTot
        return sumDurata


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()


    def getAllNodes(self):
        return list(self._grafo.nodes())
