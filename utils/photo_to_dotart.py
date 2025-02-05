import os
import base64
import cv2

from io import BytesIO
from PIL import Image

def make_b_and_w_image(user_id: str, scale_percent=25) -> str:
    path_to_images = os.path.join('users_images', user_id)
    images_list = sorted(os.listdir(path_to_images))

    img_path = os.path.join(path_to_images, images_list[-1])
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Уменьшаем изображение
    width = int(img.shape[1] * (scale_percent + 40) / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    # Бинаризация
    _, im_bw = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('img', im_bw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    with open('file.txt', 'w') as f:
        for y in range(im_bw.shape[0]):
            for x in range(im_bw.shape[1]):
                f.write("." if im_bw[y, x] == 0 else " ")
            f.write("\n")

    # (thresh, im_bw)= cv2.threshold(img, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow('img', im_bw)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # img = Image.open(img_path)
    # img = img.convert('L')
    # img = img.point(lambda x: 255 if x > 100 else 0)
    #
    # # Кодируем изображение в base64
    # buffered = BytesIO()
    # img.save(buffered, format='JPEG')
    # return base64.b64encode(buffered.getvalue()).decode()


