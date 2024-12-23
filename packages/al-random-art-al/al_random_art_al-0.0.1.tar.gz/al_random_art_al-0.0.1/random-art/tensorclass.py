import numpy as np

class TensorClass:
    def __init__(self, data):
        self.data = np.array(data)

    def apply_grayscale(self):
        """Конвертирует RGB в оттенки серого."""
        grayscale = np.mean(self.data, axis=2).astype(np.uint8)
        self.data = np.stack([grayscale] * 3, axis=2)

    def blend(self, other, alpha=0.5):
        """Смешивает текущий тензор с другим."""
        self.data = (self.data * alpha + other.data * (1 - alpha)).astype(np.uint8)

    def get_data(self):
        """Возврат данных numpy."""
        return self.data

# Пример использования
if __name__ == "__main__":
    t1 = TensorClass(np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8))
    t2 = TensorClass(np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8))
    t1.blend(t2, alpha=0.7)
    print("Тензоры смешаны.")
