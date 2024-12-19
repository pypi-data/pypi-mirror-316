import copy
import random
from PIL import Image
import imgaug.augmenters as iaa
import os
import cv2
import numpy as np
from ur_material.modules import overlap_final
from ur_material.modules import perspective_transform
from ur_material.modules import elastic_transform as ela
from ur_material.modules import texture_overlap
import genalog.degradation.effect as effect
from augraphy import *

def elastic_transform(image, file_name=None,alpha_range=None, movement=None, alpha=None, sigma=None, alpha_affine=None, random_seed=42, save=False, crop_by_amount=False, crop_amount=None):
    # print("elastic transform seed: ", random_seed)
    random.seed(random_seed)
    image = ela.process(copy.copy(image),alpha_range=alpha_range, movement=movement, alpha=alpha, sigma=sigma,
                    alpha_affine=alpha_affine, random_seed=random_seed, save=save, crop_by_amount=crop_by_amount, crop_amount=crop_amount)

    return image

def motionblur(image, file_name=None, k=(4,4), angle=(0, 360), save=False):
    blur = iaa.MotionBlur(k, angle)
    result_image = blur(image=image)
    # result_image = Image.fromarray(result_image)
    if save:
        # result_image.save(f'./test/{file_name}_blur.jpg')
        cv2.imwrite(f'./test/{file_name}_blur.jpg', result_image)
    return result_image

def add_texture(image, file_name=None, save=False, use_synthetic=False, random_seed=None):
    # 先用浅色有纹理纸张使用overlap_final.overlap()函数合并内容

    if random_seed is None:
        random_seed = 42

    random.seed(random_seed)

    if use_synthetic:
        texture_paths = [f"{os.path.dirname(__file__)}/../../texture/{f}" for f in os.listdir(f"{os.path.dirname(__file__)}/../../texture") if f.endswith(".jpg")]
    else:
        texture_paths = [f"{os.path.dirname(__file__)}/../../texture/{f}" for f in os.listdir(f"{os.path.dirname(__file__)}/../../texture") if f.endswith(".png")]
    texture_path = random.choice(texture_paths)
    background = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    # pepper the background img
    # background = effect.salt(background, 0.0005)

    result = overlap_final.overlap(background, image)

    if save:
        cv2.imwrite(f"./test/{file_name}_texture.jpg", result)
    return result

def increase_darkness(image, file_name=None, save=False, random_seed=42):

    random.seed(random_seed)

    # 加深
    foreground_path = [f"../../texture_dark_combine/{f}" for f in os.listdir("../texture_dark_combine") if f.endswith(".png")]
    foreground = cv2.imread(random.choice(foreground_path), cv2.IMREAD_UNCHANGED)

    result = texture_overlap.blend_images(foreground, image, 0.3)

    if save:
        cv2.imwrite(f"./test/{file_name}_texture.jpg", result)
    return result

def sticker(images, output_size=(1536, 1236), random_seed=42):

    random.seed(random_seed)

    augmentations = [motionblur, perspective_transform.main]
    output_image = Image.new('RGB', output_size, (255, 255, 255))
    # 计算每张图片的粘贴位置
    x_offset = 100
    y_offset = 50

    for image in images:
        # 随机应用图像增强处理
        augmentation = random.choice(augmentations)
        augmented_image = augmentation(image, "1")

        # 获取增强后图片的尺寸
        width, height = augmented_image.size

        # 如果当前行的高度超过空白图像的高度，则停止粘贴
        if y_offset + height > output_size[1]:
            break

        # 粘贴图片到空白图像上，左侧对齐
        output_image.paste(augmented_image, (x_offset, y_offset))

        # 更新偏移量
        y_offset += height + 30
    output_image.save("./enhanced-image/splice/111.jpg")
    return output_image


if __name__=="__main__":
    image = cv2.imread("./test/clean_15726443_01.png", cv2.IMREAD_UNCHANGED)
    image = add_texture(image)
    cv2.imshow("result", image)
    cv2.waitKey(0)