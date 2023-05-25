from PIL import Image
import numpy as np


def swap_and_save(image_path, save_swapped_lr_path, save_swapped_tb_path):
    # Открываем изображение с помощью Pillow
    image = Image.open(image_path)

    # Преобразуем изображение в массив NumPy
    img_array = np.array(image)

    # Меняем местами левую и правую части
    height, width, _ = img_array.shape
    split_point = width // 2
    left_part = img_array[:, :split_point, :]
    right_part = img_array[:, split_point:, :]

    swapped_array_lr = np.concatenate((right_part, left_part), axis=1)

    # Создаем изображение для поменянных левой и правой частей
    swapped_image_lr = Image.fromarray(swapped_array_lr)

    # Сохраняем поменянные левую и правую части изображения
    swapped_image_lr.save(save_swapped_lr_path)

    # Меняем местами верхнюю и нижнюю части
    split_point = height // 2
    top_part = img_array[:split_point, :, :]
    bottom_part = img_array[split_point:, :, :]

    swapped_array_tb = np.concatenate((bottom_part, top_part), axis=0)

    # Создаем изображение для поменянных верхней и нижней частей
    swapped_image_tb = Image.fromarray(swapped_array_tb)

    # Сохраняем поменянные верхнюю и нижнюю части изображения
    swapped_image_tb.save(save_swapped_tb_path)


# Пример использования
image_path = "static/input-image/god.jpg"
save_left_right_path = "static/output-image/output_left_right.jpg"
save_top_bottom_path = "static/output-image/output_top_bottom.jpg"

swap_and_save(image_path, save_left_right_path, save_top_bottom_path)