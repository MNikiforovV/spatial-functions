# -*- coding: utf-8 -*-

import mpois_mif_layer as mif
from mpois_point import Point
from mpois_polyline import Polyline

from heapq import heappush, heappop

class Graph():
    def __init__(self, vertexList, edgeList):
        self.V = vertexList
        self.E = []
        self.N = {} 
        for p1 in self.V:
            self.N[p1] = []
            for p2 in self.V:
                for e in edgeList:
                    if e.isEndPoint(p1) and e.isEndPoint(p2):
                        if p1  < p2: self.E.append((p1,p2))
                        if p1 != p2: self.N[p1].append(p2)

    def neighbours(self, p):
        return self.N[p]
    def closestVertex(self, p):
        D = {}
        for v in self.V:
            D[v] = v.distance(p)
        return min(D.items(), key=lambda x: x[1])[0]

    def dijkstra(self,source):
        distances={}
        predecessors={}
        seen={ source: 0 }
        Q =  { source: 0 }

        cnt=0
        while Q:
            v, v_dist = min(Q.items(), key=lambda x: x[1])
            distances[v] = v_dist
            del Q[v]
            for w in self.neighbours(v):
                vw_dist = v_dist + v.distance(w)
                if (w not in seen or seen[w]>vw_dist) and w not in distances:
                    seen[w]=vw_dist
                    Q[w] = vw_dist
                    predecessors[w] = v
        return distances, predecessors

#------------------------------------------------------------------------------
if __name__ == '__main__':
    mifFile = open('v.mif')
    vertexLayer = mif.MifLayer()
    vertexLayer.loadFromFile(mifFile)
    mifFile.close()

    mifFile = open('e.mif')
    edgeLayer = mif.MifLayer()
    edgeLayer.loadFromFile(mifFile)
    mifFile.close()

    G = Graph(vertexLayer, edgeLayer)

    startVertex = G.closestVertex(Point(0.0,0.0))
    distDijkstra, predDijkstra = G.dijkstra(startVertex)

    print ("""Version 300
Charset "WindowsCyrillic"
Delimiter ","
CoordSys Earth Projection 1, 0
Columns 1
  id Integer
Data
""")

    for d in predDijkstra:
        p = Polyline(*(d, predDijkstra[d]))
        print (p)    

