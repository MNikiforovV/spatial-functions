import numpy as np


def hausdorff_distance(u, v):
    """
    Вычисляет метрику Хаусдорфа между двумя множествами точек u и v.
    Использует векторизацию для ускорения вычислений.
    """
    # Вычисляем попарные расстояния между всеми точками u и v
    pairwise_distances = np.linalg.norm(u[:, np.newaxis] - v, axis=2)

    # Находим минимальные расстояния от каждой точки u до любой точки v
    min_u_to_v = np.min(pairwise_distances, axis=1)
    # Находим минимальные расстояния от каждой точки v до любой точки u
    min_v_to_u = np.min(pairwise_distances, axis=0)

    # Вычисляем двустороннее расстояние Хаусдорфа
    return max(np.max(min_u_to_v), np.max(min_v_to_u))

def generate_regular_polygon(n, radius=1, center=(0, 0)):
    """Генерирует правильный n-угольник."""
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))

def generate_rectangle(width, height, center=(0, 0)):
    """Генерирует прямоугольник."""
    x = np.array([-width / 2, width / 2, width / 2, -width / 2])
    y = np.array([-height / 2, -height / 2, height / 2, height / 2])
    return np.column_stack((x + center[0], y + center[1]))

def generate_square(side, center=(0, 0)):
    """Генерирует квадрат."""
    return generate_rectangle(side, side, center)

def detect_shape(points):
    """Определяет тип фигуры на основе метрики Хаусдорфа."""
    # Центрируем фигуру: переносим её центр в начало координат
    centroid = np.mean(points, axis=0)
    points_centered = points - centroid

    # Вычисляем размеры фигуры
    max_dist = np.max(np.linalg.norm(points_centered, axis=1))
    radius = max_dist / np.sqrt(2)  # Для квадрата и прямоугольника

    # Генерируем эталонные фигуры (центрированные в начале координат)
    square = generate_square(2 * radius, center=(0, 0))
    rectangle = generate_rectangle(2 * radius, radius, center=(0, 0))
    triangle = generate_regular_polygon(3, radius, center=(0, 0))
    hexagon = generate_regular_polygon(6, radius, center=(0, 0))

    # Вычисляем расстояния Хаусдорфа до эталонных фигур
    distances = {
        "square": hausdorff_distance(points_centered, square),
        "rectangle": hausdorff_distance(points_centered, rectangle),
        "triangle": hausdorff_distance(points_centered, triangle),
        "hexagon": hausdorff_distance(points_centered, hexagon),
    }

    # Находим фигуру с минимальным расстоянием
    detected_shape = min(distances, key=distances.get)
    return detected_shape, distances