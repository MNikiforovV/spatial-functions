# -*- coding: utf-8 -*-

from mpois_point  import Point
from mpois_region import Region
import mpois_mif_layer as mif

def segmentsIntersectionPoint(startPnt1, endPnt1, startPnt2, endPnt2):
    x11, y11 = [float(val) for val in startPnt1]
    x12, y12 = [float(val) for val in endPnt1]
    x21, y21 = [float(val) for val in startPnt2]
    x22, y22 = [float(val) for val in endPnt2]
   
    A1, B1, C1 = y11 - y12, x12 - x11, x11*y12 - x12*y11
    A2, B2, C2 = y21 - y22, x22 - x21, x21*y22 - x22*y21
    D =  A1*B2-A2*B1
    if D!=0:
        x = (C2*B1 - C1*B2) / D
        y = (A2*C1 - A1*C2) / D
        if min(x11, x12) <= x <= max(x11, x12):
            # Intersection point is found
            return (x, y)
        else:
            # Intersection Point of lines outside segment
            return None
    else:
        DA = A1*C2-A2*C1
        DB = B1*C2-B2*C1
        if DA==0 and DB==0:
            # Lines match
            return None
        else:
            # Lines are parallel
            return None

def pointRespect2Vector(a, b, c):
    """ Определяем, с какой сторны от вектора BC находится A
        -1  = Справа
         1  = Слева 
         0  = На Линии
    """
    cross_product_z = (c.x - b.x)*(a.y - b.y) - (c.y - b.y)*(a.x - b.x)
    return cmp(cross_product_z, 0)

def isBoundingBoxCross(a1, a2, b1, b2):
    def isIntervalCross(a, b ,c ,d):
        """ Проверка на пересечение двух интервалов 
            [a,b] и [c,d]
        """
        if (a > b):    a, b = b, a
        if (c > d):    c, d = d, c
        return max(a,c) <= min(b,d)
    if not isIntervalCross(a1.x, a2.x, b1.x, b2.x): return False
    if not isIntervalCross(a1.y, a2.y, b1.y, b2.y): return False
    return True

def isSegmentCross(a,b,c,d):
    """ Проверка на пересечение двух отрезков AB и CD
    """
    def between(a,b,c):
        """ Проверяем, что a принадлежит интервалу (b,c)
        """
        if min(b,c) < a < max(b,c): return True
        return False
    def pointInSegment(p,a,b):
        if abs(b.x-a.x) > abs(b.y-a.y):
            if between(p.x,  a.x,b.x): return True
        else:
            if between(p.y,  a.y,b.y): return True
        return False

    if not isBoundingBoxCross(a,b,c,d): return False
    # Вычисляем положение вершин отрезка относительно другого 
    c2ab = pointRespect2Vector(c, a,b) 
    d2ab = pointRespect2Vector(d, a,b)
    a2cd = pointRespect2Vector(a, c,d)
    b2cd = pointRespect2Vector(b, c,d)
    # Если вершина отрезка лежит на прямой, заданной другим отрезком
    if c2ab==0.0 and pointInSegment(c, a,b): return True
    if d2ab==0.0 and pointInSegment(d, a,b): return True
    if a2cd==0.0 and pointInSegment(a, c,d): return True
    if b2cd==0.0 and pointInSegment(b, c,d): return True
    # Отрезки пересекаются?
    if not c2ab * d2ab < 0: return False
    if not a2cd * b2cd < 0: return False
    return True

def convexHull(P, makeRegion=False):            
    points = sorted(P)
    def cross(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    if makeRegion:
        R = Region()
        R.addBorder(*(lower[:-1] + upper))
        return R
    else:
        return lower[:-1] + upper[:-1]

            
#------------------------------------------------------------------------------
if __name__ == '__main__':
    #print (segmentsIntersectionPoint((0,0), (10,0), (5,10), (5,-10)) == (5,0))
    #print (segmentsIntersectionPoint((0,0), (10,10), (0,10), (10,0)) == (5,5))

    #myLayer=[Point(0,0),  Point(0,10), Point(10,10), 
    #         Point(10,0), Point(0,0),  Point(10,10),
    #         Point(0,10), Point(10,0), Point(5,15),
    #         Point(5,5), Point(1,9),  Point(5,14),
    #        ]

    #r = convexHull(myLayer)
    #for rr in r: print (rr)

    
    #print (isSegmentCross(Point(0,0), Point(10,10), Point(9,9), Point(15,15)))

    print (ccw(Point(1,1), Point(0,0), Point(-1,-4)))




