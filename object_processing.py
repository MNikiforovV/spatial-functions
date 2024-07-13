import geojson
import numpy as np


def is_polygon_rectangular(filename: str):
    """
    Метод проверяет полигоны, содержащиеся в файле GeoJSON на наличие неправильных углов и исправляет их.
    filename: str - имя файла или путь к файлу GeoJSON
    """
    with open(filename) as f:
        polygons = geojson.load(f)

    for p in polygons["features"]:
        coordinates = p["geometry"]["coordinates"][0][0]
        if len(coordinates)-1 == 4:
            coordinates.append(coordinates[1])

            for point1, point2, point3 in zip(coordinates[:-2], coordinates[1:-1], coordinates[2:]):
                angle = angle_between_vectors(point1, point2, point3)
                """ debug >>
                print(angle)
                << debug """ 
                diff = 90 - angle
                if diff >= -1 and diff <= 1 and diff != 0:
                    diff_px = point3[0] - point2[0]
                    diff_py = point3[1] - point2[1]

                    i2 = coordinates.index(point2)
                    i3 = coordinates.index(point3)

                    point2 = [point2[0] - diff_px / 2, point2[1] - diff_py / 2]
                    point3 = [point3[0] + diff_px / 2, point3[1] + diff_py / 2]


                    coordinates[i2] = point2.copy()
                    coordinates[i3] = point3.copy()

                print(angle_between_vectors(point1, point2, point3))

            #coordinates.pop()
        p["geometry"]["coordinates"][0][0] = coordinates.copy()

    #print(p["geometry"]["coordinates"][0][0], coordinates)
    with open(filename, "w") as f:
        geojson.dump(polygons, f)
            

def angle_between_vectors(point1, point2, point3):
    point1, point2, point3 = np.array(point1), np.array(point2), np.array(point3)
    vector1 = point1 - point2
    vector2 = point3 - point2
    return np.degrees(np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))


is_polygon_rectangular("test2.geojson")
