from mpois_columns import Columns
from mpois_polyline import Polyline 
from mpois_point import Point

def horizontalRayCrossSegment(p,v1,v2):
    """ Проверка пересечения горизонтальным лучом сегмента
        p - точка, откуда исходит вправо луч
        v1 и v2 - концы сегмента (точки)
    """
    # Горизонтальный сегмент   
    if v1.y == p.y and v2.y == p.y:
        if v1.x >= p.x or v2.x >= p.x: 
            return True
        else: return False

    # Сегмент ниже луча
    if v1.y <= p.y and v2.y <= p.y:   return False
    # Сегмент выше луча
    if v1.y >= p.y and v2.y >= p.y:   return False
    # Сегмент левее луча
    if v1.x <= p.x and v2.x <= p.x:   return False

    # Вертикальный сегмент   
    if v1.x == v2.x:    return True 


    # Обычный сегмент
    crossX = ((v1.x-v2.x)*p.y + v2.x*v1.y - v1.x*v2.y) / (v1.y-v2.y)
    if crossX < p.x: return False
    else: return True

class Region(Columns):
    def __init__(self):
        self.borders = []
    def __str__(self):
        mifStr = "Region %d\n" % (len(self.borders))
        for b in self.borders:
            mifStr += "%d\n" % (len(b.vertex))
            for v in b.vertex:
                mifStr += "%f %f\n" % (v.x, v.y)
        return mifStr
    def __len__(self):
        """ Возвращает количество границ полигона
            1 - простой полигон, 
            2 - полигон с одним островом и т.д.
        """
        return len(self.borders)

    def addBorder(self, *argVertexTuple):
        newBorder = Polyline(*argVertexTuple)
        self.borders.append(newBorder)
        
    def area(self, precision=None):
        a = 0.0
        for b in self.borders:
            for n, p in zip(b.vertex[:-1], b.vertex[1:]):
                dx = p.x - n.x 
                dy = abs(p.y - n.y)
                miny = min(p.y, n.y)
                a += dx*(dy/2 + miny);
        if precision != None: a = round(a, int(precision))
        return abs(a)        

    def centroid(self):
        a = cx = cy = 0.0
        for b in self.borders:
            for n, p in zip(b.vertex[:-1], b.vertex[1:]):
                cross = n.x*p.y - p.x*n.y
                a  += cross
                cx += (n.x+p.x) * cross
                cy += (n.y+p.y) * cross
        return Point(cx/(3*a), cy/(3*a))        

    def perimetr(self, precision=None):
        p = 0.0
        for b in self.borders:
            p += b.length()
        if precision != None: p = round(p, int(precision))
        return p

    def topoPointInside(self, point): 
        crossCnt = 0
        for b in self.borders:
            for n, p in zip(b.vertex[:-1], b.vertex[1:]):
                # Пересечения по внутренним точкам сегмента
                if horizontalRayCrossSegment(point, n, p):
                    crossCnt += 1
                # Пересечения по узлам
                if n.y == point.y and n.x > point.x:
                    crossCnt += 1
        if crossCnt % 2 == 0: return False
        else: return True

#------------------------------------------------------------------------------
if __name__ == '__main__':
    pass



