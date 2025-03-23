import geojson
import numpy as np
import matplotlib.pyplot as plt
from hausdorff import detect_shape
from transformations import fix_rectangle


def read_geojson(filename, write_back=True):
    """
    Чтение файла GeoJSON.

    :param filename: Имя файла или путь к файлу GeoJSON.
    :write_back: Надо ли записывать результат метода в файл.
    :return: Содержимое файла GeoJSON.
    """
    def fix_rect(coordinates):
        if len(coordinates)-1 == 4:
            coordinates.pop()
            #coordinates.append(coordinates[1])

            print(coordinates)
            fixed = fix_rectangle(coordinates.copy())
            print(fixed)

        #fixed = rotate_coordinates(coordinates.copy(), 30)

        #fixed[4] = fixed[0]
        #fixed.pop()
        # Визуализация
        coords = np.array(coordinates)
        corrected_coords = np.array(fixed)

        plt.figure(figsize=(10, 6))

        # Оригинальные координаты
        plt.plot(coords[:, 0], coords[:, 1], 'ro-', label='Оригинальные координаты')  # Красные точки

        # Исправленные координаты
        plt.plot(corrected_coords[:, 0], corrected_coords[:, 1], 'bo-', label='Исправленные координаты')  # Синие точки

        # Настройки графика
        plt.title('Сравнение оригинальных и исправленных координат')
        plt.xlabel('X координаты (метры)')
        plt.ylabel('Y координаты (метры)')
        plt.legend()
        plt.grid()
        plt.axis('equal')  # Чтобы оси имели одинаковый масштаб

        plt.show()

        fixed.append(fixed[0])

        return fixed


    with open(filename) as f:
        polygons = geojson.load(f)

    for p in polygons["features"]:
        coordinates = p["geometry"]["coordinates"][0][0]
        
        #result = fix_rect(coordinates)
        result = detect_shape(coordinates)
        
        if write_back: p["geometry"]["coordinates"][0][0] = result.copy()

    if write_back:
        with open(filename, "w") as f:
            geojson.dump(polygons, f)

    return result

            
print(read_geojson("examples/test3.geojson", False))
