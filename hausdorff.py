import numpy as np
from math import isclose
from transformations import rotate_coordinates


def normalize_polygon(points):
    """Центрирует полигон и нормализует его размер."""
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    max_dist = np.max(np.linalg.norm(centered, axis=1))
    return centered / max_dist if max_dist > 0 else centered


def hausdorff_distance(u, v):
    """Вычисляет метрику Хаусдорфа между двумя множествами точек."""
    pairwise_dist = np.linalg.norm(u[:, np.newaxis] - v, axis=2)
    return max(np.max(np.min(pairwise_dist, axis=1)), 
               np.max(np.min(pairwise_dist, axis=0)))


def detect_shape(points, dist_threshold=0.05):
    """Определяет тип фигуры с учётом поворотов и смещений."""
    # Нормализуем полигон (центрируем и приводим к единичному размеру)
    normalized = normalize_polygon(np.array(points))
    
    # Проверяем повороты на 90°
    matches = 0
    for angle in [90, 180, 270, 360]:
        rotated = rotate_coordinates(normalized, angle)
        distance = hausdorff_distance(normalized, rotated)
        if distance < dist_threshold:
            matches += 1
        print(distance)
    
    # Определяем тип фигуры
    if matches == 4:
        return "square"
    elif matches == 2:
        # Проверяем соотношение сторон для прямоугольника
        side1 = np.linalg.norm(normalized[0] - normalized[1])
        side2 = np.linalg.norm(normalized[1] - normalized[2])
        ratio = max(side1, side2) / min(side1, side2)
        
        if isclose(ratio, 1, abs_tol=0.01):
            return "square"  # Квадрат - частный случай прямоугольника
        return "rectangle"
    else:
        n = len(normalized)
        return f"regular {n}-gon"