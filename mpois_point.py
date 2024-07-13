from math import sqrt
from mpois_columns import Columns
from mpois_polyline import Polyline

class Point(Columns):
    def __init__(self, x, y, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def __str__(self):
        if False:
            return "Point %s %s %s\n" % (str(self.x), str(self.y), str(self.z))
        else:
            return "Point %s %s\n" % (str(self.x), str(self.y))
    def __eq__(self, other):
        if self.x == other.x and self.y==other.y and self.z==other.z:
            return True
        else:
            return False        
    def __ne__(self, other):
        if not(self.x == other.x and self.y==other.y and self.z==other.z):
            return True
        else:
            return False        
    def __lt__(self, other):
        if self.x < other.x:    return True
        if self.x > other.x:    return False
        if self.y < other.y:    return True
        if self.y > other.y:    return False
        if self.z < other.z:    return True
        return False
    def __le__(self, other):
        if self.x <  other.x:    return True
        if self.x >  other.x:    return False
        if self.y <= other.y:    return True
        if self.y >= other.y:    return False
        if self.z <= other.z:    return True
        return False
    def __gt__(self, other):
        if self.x > other.x:    return True
        if self.x < other.x:    return False
        if self.y > other.y:    return True
        if self.y < other.y:    return False
        if self.z > other.z:    return True
        return False
    def __ge__(self, other):
        if self.x >  other.x:    return True
        if self.x <  other.x:    return False
        if self.y >= other.y:    return True
        if self.y <= other.y:    return False
        if self.z >= other.z:    return True
        return False
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def distance(self, otherPoint):
        return sqrt((self.x - otherPoint.x)**2 + (self.y - otherPoint.y)**2)

    def distance2Line(p1, p2):
        # Get line equation by twopoints
        A = p1.y-p2.y
        B = p2.x-p1.x
        C = (p1.x*p2.y-p2.x*p1.y)
        # Distance from point to line
        return abs(A*self.x + B*self.y + C) / sqrt(A**2+B**2)

    def distance2Segment(self, p1, p2):
        A = self.x - p1.x
        B = self.y - p1.y
        C = p2.x - p1.x
        D = p2.y - p1.y
        dot = A * C + B * D
        len_sq = C * C + D * D
        if (len_sq != 0):   param = dot / len_sq
        else:               param = -1
        if (param < 0):     xx, yy = p1.x, p1.y
        elif (param > 1):   xx, yy = p2.x, p2.y
        else:               xx, yy = p1.x + param*C, p1.y + param * D
        dx = self.x - xx
        dy = self.y - yy
        return sqrt(dx * dx + dy * dy)
    def distance2Polyline(self,polyline):
        return min([self.distance2Segment (sp,fp) for sp, fp in zip(polyline[:-1],polyline[1:])])

#------------------------------------------------------------
if __name__ == '__main__':
    pline=Polyline(Point(0,0),Point(0,4),Point(2,6),Point(5,5))
    p=Point(-1,3)
    print (p.distance2Polyline(pline))