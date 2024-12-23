import numpy as np
import random

class Layer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layer = np.zeros((height, width, 3), dtype=np.uint8)  # RGB слой

    def random_noise(self):
        """Генерация случайного цветного шума."""
        self.layer = np.random.randint(0, 256, (self.height, self.width, 3), dtype=np.uint8)

    def add_random_circles(self, count=10):
        """Добавление случайных кругов на слой."""
        for _ in range(count):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            radius = random.randint(5, min(self.width, self.height) // 10)
            color = [random.randint(0, 255) for _ in range(3)]  # Случайный цвет
            self._draw_circle(x, y, radius, color)

    def _draw_circle(self, cx, cy, radius, color):
        """Простой алгоритм для отрисовки круга."""
        for x in range(self.width):
            for y in range(self.height):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    self.layer[y, x] = color

    def get_data(self):
        """Возврат текущего слоя как numpy array."""
        return self.layer
