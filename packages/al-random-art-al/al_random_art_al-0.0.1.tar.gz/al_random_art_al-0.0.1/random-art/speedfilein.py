from PIL import Image
import numpy as np

def save_image(filename, data):
    """Сохраняет numpy array в изображение."""
    image = Image.fromarray(data)
    image.save(filename)
    print(f"Изображение сохранено: {filename}")

def load_image(filename):
    """Загружает изображение в numpy array."""
    image = Image.open(filename)
    return np.array(image)

def read_file_fast(filepath):
    """Чтение файла с данными и создание изображения."""
    data = load_image(filepath)
    return data

def write_file_fast(filepath, content):
    """Запись изображений с использованием функции сохранения."""
    save_image(filepath, content)

# Пример использования
if __name__ == "__main__":
    from layers import Layer

    layer = Layer(256, 256)
    layer.random_noise()
    write_file_fast("random_art.png", layer.get_data())
