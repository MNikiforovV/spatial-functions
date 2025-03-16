import geojson
import numpy as np
import matplotlib.pyplot as plt
import math


def shift_coordinates(coordinates, distances):
    """
    Сдвигает координаты по заданным осям

    :param coordinates: список координат
    :param distances: словарь с расстояниями сдвига {'x': значение, 'y': значение}
    :return: новый список координат
    """
    shifted_coordinates = []
    for x, y in coordinates:
        new_x = x + distances.get('x', 0)
        new_y = y + distances.get('y', 0)
        shifted_coordinates.append((new_x, new_y))

    return shifted_coordinates


def scale_coordinates(coordinates, scale_factor):
    """
    Масштабирует список координат на заданный коэффициент

    :param coordinates: список координат
    :param scale_factor: коэффициент масштабирования
    :return: новый список координат
    """
    scaled_coordinates = [(x * scale_factor, y * scale_factor) for (x, y) in coordinates]
    return scaled_coordinates


def rotate_coordinates(points, angle):
    """
    Поворачивает объект на заданный угол

    :param coordinates: список координат
    :param angle: угол поворота в градусах
    :return: новый список координат
    """
    angle_rad = math.radians(angle)
    
    centroid_x = sum(x for x, y in points) / len(points)
    centroid_y = sum(y for x, y in points) / len(points)
    
    rotated_points = []
    for x, y in points:
        x -= centroid_x
        y -= centroid_y
        
        x_new = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        y_new = x * math.sin(angle_rad) + y * math.cos(angle_rad)

        x_new += centroid_x
        y_new += centroid_y
        
        rotated_points.append((x_new, y_new))
    
    return rotated_points

# def angle_between_vectors(A, B, C):
#     A, B, C = np.array(A), np.array(B), np.array(C)
#     AB = B - A
#     BC = C - B
#     return np.degrees(np.arccos(np.dot(AB, BC) / (np.linalg.norm(AB) * np.linalg.norm(BC))))

# def correct_rectangular(coordinates):
#     """
#     Метод исправляет координаты прямоугольника, если углы не равны 90.
#     coordinates: list - список координат прямоугольника
#     """
#     print(list(zip(coordinates[:-2], coordinates[1:-1], coordinates[2:])))
#     for A, B, C in zip(coordinates[:-2], coordinates[1:-1], coordinates[2:]):
#         angle = angle_between_vectors(A, B, C)
#         print(angle, "angle")
#         diff = 90 - angle
#         print(diff, "diff")
#         if np.abs(diff) > 1:
#             diff_px = B[0] - A[0]
#             diff_py = B[1] - A[1]
#             print(diff_px, diff_py, "diff_px, diff_py")

#             B = [B[0] + np.abs(diff_px) / 2, B[1] + np.abs(diff_py) / 2]
#             A = [A[0] - np.abs(diff_px) / 2, A[1] - np.abs(diff_py) / 2]

#         print(angle_between_vectors(A, B, C), "result")

#     return coordinates


def calculate_angle(A, B, C):
    """Вычисляет угол ABC, используя скалярное произведение векторов.
    param A: координаты точки A
    param B: координаты точки B
    param C: координаты точки C
    return: угол ABC в градусах
    """
    AB = B - A
    BC = C - B
    cosine_angle = np.dot(AB, BC) / (np.linalg.norm(AB) * np.linalg.norm(BC))
    return np.degrees(np.arccos(cosine_angle))

def fix_rectangle(coords):  # Пока что не работает правильно. В результате достраивается квадрат, вместо исправления координат.
    """Корректирует координаты четырёхугольника так, чтобы все углы были 90 градусов.
    param coords: список координат четырёхугольника
    return: исправленные координаты четырёхугольника
    """
    assert len(coords) == 4, "Должно быть 4 координаты."

    A, B, C, D = [np.array(p) for p in coords]

    AB = B - A

    perpendicular_AB = np.array([AB[1], -AB[0]])
    C = B + perpendicular_AB

    BC = C - B

    perpendicular_BC = np.array([BC[1], -BC[0]])
    D = C + perpendicular_BC
    
    return [A.tolist(), B.tolist(), C.tolist(), D.tolist()]


def read_geojson(filename):
    """
    Чтение файла GeoJSON.

    :param filename: Имя файла или путь к файлу GeoJSON.
    :return: Содержимое файла GeoJSON.
    """
    with open(filename) as f:
        polygons = geojson.load(f)

    for p in polygons["features"]:
        coordinates = p["geometry"]["coordinates"][0][0]
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
        p["geometry"]["coordinates"][0][0] = fixed.copy()

    #print(p["geometry"]["coordinates"][0][0], coordinates)
    with open("1"+filename, "w") as f:
        geojson.dump(polygons, f)
    
            
read_geojson("test4.geojson")
