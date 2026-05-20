import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapTeams = {}
        self._grafo = nx.Graph()
        self._teams = []
        self._bestPath = []
        self._bestObjVal = 0

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

        #for u in self._grafo.nodes:
        #    for v in self._grafo.nodes:
        #        if u != v:
        #            self._grafo.add_edge(u, v)

        myedges = list(itertools.combinations(self._teams,2))
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesTeams(year,self._idMapTeams)
        for e in self._grafo.edges:
            salario1 = mapSalary[e[0]]
            salario2 = mapSalary[e[1]]
            peso = salario1+salario2
            self._grafo[e[0]][e[1]]["weight"] = peso


    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self,year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams

    def getGrafoDetails(self):
        return len(self._grafo.nodes),len(self._grafo.edges)

    def getVicini(self,source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v,self._grafo[source][v]["weight"]))
        return viciniTuples

    def getPath(self,v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]
        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def _ricorsione(self,parziale):
        # 1 condizione di ottimalità verifico se parziale meglio del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)
        # 2 condizione di terminazione verifico se posso continuare

        # 3 faccio la ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            peso = self._grafo[parziale[-1]][v]["weight"]
            if peso < self._grafo[parziale[-2]][parziale[-1]]["weight"] and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def getPathV2(self,v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0])
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal

    def _ricorsioneV2(self,parziale):
        # 1 condizione di ottimalità verifico se parziale meglio del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)
        # 2 condizione di terminazione verifico se posso continuare

        # 3 faccio la ricorsione
        #listaVicini = []
        #for v in self._grafo.neighbors(parziale[-1]):
        #    edgeV = self._grafo[parziale[-1]][v]["weight"]
        #    listaVicini.append((v,edgeV))
        #
        #listaVicini.sort(key=lambda x: x[1],reverse=True)

        listaVicini = self.getVicini(parziale[-1])

        for v in listaVicini:
            if v[0] not in parziale and v[1] < self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

        #for v in self._grafo.neighbors(parziale[-1]):
        #    peso = self._grafo[parziale[-1]][v]["weight"]
        #    if peso < self._grafo[parziale[-2]][parziale[-1]]["weight"] and v not in parziale:
        #        parziale.append(v)
        #        self._ricorsione(parziale)
        #        parziale.pop()

    def _score(self, parziale):
        score = 0
        for i in range(0,len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return score

    def getRandomNode(self):
        index = random.randint(0,len(self._teams))
        return self._teams[index]