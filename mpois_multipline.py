from mpois_columns import Columns

class MultiPline(Columns):
    def __init__(self):
        self.parts = []

    def __len__(self):
        """ Возвращает количество частей составной полилинии
        """
        return len(self.parts)
    def __str__(self):
        mifStr = "Pline Multiple %d\n" % (len(self.parts))
        for p in self.parts:
            mifStr += "%d\n" % (len(p.vertex))
            for v in p.vertex:
                mifStr += "%f %f\n" % (v.x, v.y)
        return mifStr

    def addPart(self, newPart):
        self.parts.append(newPart)

    def length(self, precision=None):
        l = 0.0
        for p in self.parts:
            l += p.length()
        if precision != None: l = round(l, int(precision))
        return l
        
