from general_models import Point, PolyLine, Polygon
import os, geojson


class GeoJSONReader():
    def __init__(self, file, path) -> None:
        self.file = file
        self.path = path
        
        
    def read_points(self) -> list:
        with open(os.path.join(self.path, self.file)) as f:
            contents = geojson.load(f)
            
        points = []
        for c in contents["features"]:
            if c["geometry"]["type"] == "Point":
                if len(c["geometry"]["coordinates"][0][0]) == 3:
                    z = c["geometry"]["coordinates"][0][0][2]
                else:
                    z = None
                    
                new_point = Point(
                    x = c["geometry"]["coordinates"][0][0][0],
                    y = c["geometry"]["coordinates"][0][0][1],
                    z = z
                )
                points.append(new_point)
            else:
                raise TypeError("Wrong type")
            
        return points
    
    def read_polylines(self) -> list:
        with open(os.path.join(self.path, self.file)) as f:
            contents = geojson.load(f)
            
        polylines_list = []
        for c in contents["features"]:
            if c["geometry"]["type"] == "PolyLine":
                new_polyline = PolyLine()
                for point in c["geometry"]["coordinates"][0][0]:
                    new_point = Point(
                        x = point[0],
                        y = point[1]
                    )
                    new_polyline.add_point(new_point)
                polylines_list.append(new_polyline)
            else:
                raise TypeError
            
        return polylines_list
    
    
    def read_polygons(self) -> list:
        with open(os.path.join(self.path, self.file)) as f:
            contents = geojson.load(f)
            
        polylines_list = []
        for c in contents["features"]:
            if c["geometry"]["type"] == "MultiPolygon":
                new_polygon = 
                    