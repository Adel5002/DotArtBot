import os
import base64
import cv2

from io import BytesIO
from PIL import Image


def make_b_and_w_image(user_id, output_txt="file.txt"):
    # Путь до последней картинки
    path_to_images = os.path.join('users_images', user_id)
    img = cv2.imread(os.path.join(path_to_images, sorted(os.listdir(path_to_images))[-1]), cv2.IMREAD_GRAYSCALE)

    # Изменяем размер
    img_resized = cv2.resize(img, (img.shape[1] * 25 // 100, img.shape[0] * 10 // 100), interpolation=cv2.INTER_AREA)

    # Применяем пороговое преобразование
    _, binary_img = cv2.threshold(img_resized, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Преобразуем в ASCII (255 → '.', 0 → ' ')
    ascii_art = "\n".join("".join("." if pixel == 255 else " " for pixel in row) for row in binary_img)

    # Записываем в файл
    with open(output_txt, "w") as f:
        f.write(ascii_art)


