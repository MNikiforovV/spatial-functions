class Point():
    def __init__(self, x: float, y: float, z: float = None) -> None:
        self.x = x
        self.y = y
        if z is not None: self.z = z
        
    def __str__(self) -> str:
        if self.z:
            return f"Point ({self.x}, {self.y}, {self.z})"
        else:
            return f"Point ({self.x}, {self.y})"
        
        
class PolyLine():
    def __init__(self) -> None:
        self.points = []
        self.current = 0
        
        
    def __str__(self) -> str:
        return f"Polyline {self.points}"
    
    
    def __iter__(self):
        return iter(self.points)
    
    
    def __next__(self):
        if self.current >= len(self.points):
            raise StopIteration
        result = self.points[self.current]
        self.current += 1
        return result            
    
    
    def add_point(self, point: Point) -> None:
        self.points.append(point)


class Polygon():
    def __init__(self) -> None:
        self.points = []
        
            
    def __str__(self) -> str:
        return f"Polygon {self.points}"
    
    
    def add_point(self, point: Point):
        len = len(self.points)
        if len == 0:
            self.points.append(point)
            self.points.append(point)
        else:
            self.points.insert(len, point)
