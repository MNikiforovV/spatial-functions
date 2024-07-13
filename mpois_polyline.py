from mpois_columns import Columns
from math import sqrt

class Polyline(Columns):
    def __init__(self, *argVertexTuple):
        self.vertex = []
        for v in argVertexTuple:
            self.vertex.append(v) 
    def __str__(self):
        mifStr = "Pline %d\n" % (len(self.vertex))
        for v in self.vertex:
            mifStr += "%f %f\n" % (v.x, v.y)
        return mifStr
    def __len__(self):
        """ Возвращает количество вершин
        """
        return len(self.vertex)
    def __getitem__(self,i):
        """ Возвращает i-ю вершину
        """
        return self.vertex[i]

    def __add__(self, summand):
        if self.vertex[0] == summand.vertex[0]:
            newVertexChain = summand.vertex[::-1] + self.vertex[1:]
        elif self.vertex[0] == summand.vertex[-1]:
            newVertexChain = summand.vertex[:-1] + self.vertex
        elif self.vertex[-1] == summand.vertex[0]:
            newVertexChain = self.vertex + summand.vertex[1:]
        elif self.vertex[-1] == summand.vertex[-1]:
            newVertexChain = self.vertex[:-1] + summand.vertex[::-1] 
        else:
            newVertexChain = self.vertex + summand.vertex
        if newVertexChain: 
            return Polyline(*newVertexChain)
    def reverse(self):
        self.vertex.reverse()
    def length(self, precision=None):
        l = 0.0
        for n, p in zip(self.vertex[:-1], self.vertex[1:]):
            dx, dy = p.x - n.x, p.y - n.y
            l += sqrt(dx**2 + dy**2)
        if precision != None: l = round(l, int(precision))
        return l
    def isEndPoint(self, P):
        if self.vertex[0]  == P: return True
        if self.vertex[-1] == P: return True
        return False