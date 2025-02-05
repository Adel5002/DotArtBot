import os
import base64
import cv2
import numpy as np

from io import BytesIO
from PIL import Image


def make_b_and_w_image(user_id, output_txt="file.txt"):
    # Путь до последней картинки
    path_to_images = os.path.join('users_images', user_id)
    img = cv2.imread(os.path.join(path_to_images, sorted(os.listdir(path_to_images))[-1]), flags=0)

    # Размытие + границы
    img_blur = cv2.GaussianBlur(img, (3, 3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image=img_blur, threshold1=90, threshold2=170)

    # Уменьшенный размер для ASCII (примерно в 3-4 раза меньше)
    resize_edges = cv2.resize(edges, (edges.shape[1] * 30 // 100, edges.shape[0] * 15 // 100), interpolation=cv2.INTER_AREA).astype(np.uint8)

    # Градиент ASCII (можно менять)
    ascii_chars = "@%#*+=-:. "[::-1]  # От темного к светлому

    # Функция для преобразования пикселей в ASCII-символы
    def pixel_to_ascii(pixel):
        index = int(pixel / 255 * (len(ascii_chars) - 1))
        return ascii_chars[index]

    # Создаем ASCII-арт
    dot_art = "\n".join("".join(pixel_to_ascii(pixel) for pixel in row) for row in resize_edges)

    # Запись в файл
    with open(output_txt, 'w') as f:
        f.write(dot_art)

    # Отображение уменьшенного изображения
    cv2.imshow('Resized Image', resize_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




