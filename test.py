import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def plot_color_distribution(image_path):
    # Загрузка изображения с помощью Pillow
    image = Image.open(image_path)

    # Преобразование изображения в массив NumPy
    image_array = np.array(image)

    # Получение гистограммы распределения цветов по каналам
    red_hist = np.histogram(image_array[:, :, 0], bins=256, range=(0, 256))
    green_hist = np.histogram(image_array[:, :, 1], bins=256, range=(0, 256))
    blue_hist = np.histogram(image_array[:, :, 2], bins=256, range=(0, 256))

    # Рисование графика распределения цветов
    plt.figure(figsize=(10, 6))
    plt.title('Color Distribution')
    plt.xlabel('Color Intensity')
    plt.ylabel('Frequency')
    plt.xlim(0, 255)
    plt.plot(red_hist[1][:-1], red_hist[0], color='red', label='Red')
    plt.plot(green_hist[1][:-1], green_hist[0], color='green', label='Green')
    plt.plot(blue_hist[1][:-1], blue_hist[0], color='blue', label='Blue')
    plt.legend()

    plt.savefig(f"graph/{image_path.split('/')[1]}.png", dpi=300, bbox_inches='tight')
    plt.close()


# Пример использования функции
image_path = 'upload/vlasov.jpg'  # Замените на путь к вашему изображению
plot_color_distribution(image_path)