import os

from PIL import Image, ImageEnhance

def make_b_and_w_image(user_id: str):
    path_to_images = os.path.join('users_images/', user_id)
    images_list = os.listdir(path_to_images)

    img = Image.open(os.path.join(path_to_images, images_list[-1]))
    img = img.convert('L')
    # print(img.tobytes())
    img = img.point(lambda x: 255 if x > 100 else 0)
    img.show()

