import json
import random
from PIL import Image
import os
import cv2
from ur_material.modules import add_watermark, add_ink_leak, make_it_old_final, ink_reduce,\
    general_quality_reduce, seperate_lines, add_dots, random_break_reduce
from ur_material.modules import warp_texture_blur_sticker
from tqdm import tqdm
from pqdm.processes import pqdm
from augraphy import *
import numpy as np
from functools import partial
import subprocess
import shutil
import argparse



# 有转灰度的步骤： perspective_transform

# 效果六： 先走效果五， 然后写一个函数，二值化或灰度图后随机选择内容进行涂抹，降低黑度或者直接涂白。
# 直接涂白的功能可以用在随机断线上

def image_augmentation_1(image, save=False, random_seed=42): # 3M -> 14M
    image = pre_process(image)
    random.seed(random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    image = add_watermark.add_water_mark(image, save=False, random_seed=random_seed)
    return image

def image_augmentation_2(image, save=False, random_seed=42):     # 对应效果一    3M -> 88M
    image = pre_process(image)
    random.seed(random_seed)
    og_width = image.shape[1]
    og_height = image.shape[0]
    image = add_ink_leak.pre_bleed(image, save=save)
    image = warp_texture_blur_sticker.add_texture(image, save=save, random_seed=random_seed)
    image = add_ink_leak.bleed(image, save=save, kernel_size=(4,4))
    image = cv2.resize(image, (og_width, og_height), interpolation=cv2.INTER_LANCZOS4)
    return image

def image_augmentation_3(image, save=False, random_seed=42): # 3M -> 12M
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.make_it_old(image, save=False)
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    return image

def image_augmentation_4(image, save=False, random_seed=42):     # 3M -> 17M
    image = pre_process(image)
    random.seed(random_seed)
    image = add_ink_leak.add_ink_leak_method(image, save=False, partial_old=False, random_seed=random_seed)   # partial_old=True
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    return image

def image_augmentation_5(image, save=False, random_seed=42):     # 3M -> 15M
    image = pre_process(image)
    random.seed(random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=save)
    return image

def image_augmentation_6(image, save=False, random_seed=42):      # 油墨减少，纸张纹理，弹性变换     # 3M -> 17M
    image = pre_process(image)
    random.seed(random_seed)
    image = ink_reduce.ink_reduce_method(image, 0.3, save=False)
    image = general_quality_reduce.reduce(image,(15,20), (3,3), save=False)
    return image

def image_augmentation_7(image, save=False, random_seed=42):    # 对应效果十     # 3M -> 17M
    image = pre_process(image)
    random.seed(random_seed)
    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=1)
    image = seperate_lines.process_image(image,num_shapes=100, reduce_percentage=0.1, method="white", save=False, random_seed=random_seed)
    image = make_it_old_final.erode_alot_s(image, save=False)
    return image

def image_augmentation_8(image, save=False, random_seed=42):     # 3M -> 75.6M
    image = pre_process(image)
    random.seed(random_seed)   
    image = make_it_old_final.make_it_old(image, save=False, partial_old=False)  # partial_old=True
    image = warp_texture_blur_sticker.add_texture(image, save=False, random_seed=random_seed)
    return image

def image_augmentation_9(image, save=False, random_seed=42):     # 3M -> 12M
    image = pre_process(image)
    random.seed(random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    image = general_quality_reduce.reduce(image,(5,10),(5,5), save=False)
    return image

def image_augmentation_10(image, save=False, random_seed=42):        # 3M -> 16M
    image = pre_process(image)
    random.seed(random_seed)
    image = ink_reduce.ink_reduce_method(image, 0.3, save=False)
    image = general_quality_reduce.reduce(image, (40, 50), (2,2), save=False)
    return image

def image_augmentation_11(image, save=False, random_seed=42):      # 对应效果二      # 3M -> 20M
    image = pre_process(image)
    random.seed(random_seed)
    image = ink_reduce.ink_reduce_method(image, 0.4, save=save, if_salt=False)
    image = warp_texture_blur_sticker.add_texture(image, save=False, random_seed=random_seed)
    image = general_quality_reduce.blur(image, (11,11), save=False)
    image = general_quality_reduce.reduce(image, (40,50), (5,5), save=False)
    return image

def image_augmentation_12(image, save=False, random_seed=42):        # 对应效果四        # 3M -> 12M
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.make_it_old(image, save=False, random_seed=random_seed)
    image = general_quality_reduce.blur(image, (7,7), save=False)
    image = general_quality_reduce.reduce(image, (5,6), (5,5), save=False)
    return image

def image_augmentation_13(image, save=False, random_seed=42):    # 对应效果五        # 3M -> 20M
    image = pre_process(image)
    random.seed(random_seed)
    image = general_quality_reduce.dilate(image, (2,2), save=False)
    if random.random() < 0.5:
        image = general_quality_reduce.blur(image, (3,3), save=False)
    return image

def image_augmentation_14(image, save=False, random_seed=42):    # 效果九        # 3M -> 13M
    image = pre_process(image)
    random.seed(random_seed)
    image = seperate_lines.process_image(image, num_shapes=20, reduce_percentage=0.1, method="white", save=False, random_seed=random_seed)
    image = general_quality_reduce.blur(image, (5,5), save=False)
    image = general_quality_reduce.reduce(image, (40,50), (5,5), save=False)
    return image

def image_augmentation_15(image, save=False, random_seed=42):    # 效果八        # 3M -> 19M
    image = pre_process(image)
    random.seed(random_seed)
    image = add_dots.add_random_speckles(image, save=False, random_seed=random_seed)
    image = general_quality_reduce.dilate(image, (3,3), save=False)
    return image

def image_augmentation_16(image, save=False, random_seed=42):    # 效果七    # 3M -> 19M
    image = pre_process(image)
    random.seed(random_seed)
    image = warp_texture_blur_sticker.add_texture(image, save=False, random_seed=random_seed)
    image = general_quality_reduce.blur(image, (7,7), save=False)
    image = general_quality_reduce.reduce(image, (20,30), (5,5), save=False)
    return image

def image_augmentation_17(image, save=False, random_seed=42):    # 效果六        # 3M -> 4M
    image = pre_process(image)
    random.seed(random_seed)
    image = cv2.erode(image, np.ones((4,4), np.uint8), iterations=1)
    image = random_break_reduce.process(image, method="reduce", num_points=1000000,save=False, random_seed=random_seed)
    lines_degradation = LinesDegradation(line_roi = (0.0, 0.0, 1.0, 1.0),
                                line_gradient_range=(75, 255),
                                line_gradient_direction= (2,2),
                                line_split_probability=(0.4, 0.5),
                                line_replacement_value=(230,255),
                                line_min_length=(5, 5),
                                line_long_to_short_ratio = (3,3),
                                line_replacement_probability = (1.0, 1.0),
                                line_replacement_thickness = (1, 1)
                                )
    image = lines_degradation(image)
    image = general_quality_reduce.blur(image, (3,3), save=False)

    return image

def image_augmentation_18(image, save=False, random_seed=42):    # 效果三        # 3M -> 10M
    image = pre_process(image)
    random.seed(random_seed)
    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=1)
    image = general_quality_reduce.blur(image, (3,3),  save=False)
    image = add_ink_leak.bleed(image,  save=False)
    image = general_quality_reduce.reduce(image, (70,80), (5,5), save=False)
    return image

def image_augmentation_19(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    # List of effects and their parameters
    effects = [
        lambda img: warp_texture_blur_sticker.motionblur(img, save=False),
        lambda img: add_ink_leak.add_ink_leak_method(img, save=False, partial_old=True, random_seed=random_seed),
        lambda img: ink_reduce.ink_reduce_method(img, 0.2, save=False),
        lambda img: add_watermark.add_water_mark(img, save=False, random_seed=random_seed),
        lambda img: general_quality_reduce.reduce(img, (30, 40), (2, 2), save=False),
        lambda img: general_quality_reduce.blur(img, (3, 3), save=False)
    ]

    # Randomly decide how many effects to apply (1 to 3)
    num_effects = random.randint(1, 3)

    # Randomly select the effects to apply
    selected_effects = random.sample(effects, num_effects)

    # Apply each selected effect to the image
    for effect in selected_effects:
        image = effect(image)

    return image
    

# convert image to grayscale
def pre_process(image):
    num_channels = image.shape[2] if len(image.shape) == 3 else 1
    if num_channels > 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    image = convert_to_grayscale_8uc1(image)

    return image

    
def convert_to_grayscale_8uc1(img):
    """
    Convert any image to 8-bit single channel grayscale image.

    Args:
    img (np.array): Input image.

    Returns:
    np.array: Grayscale image of type CV_8UC1.
    """

    # 首先检查图像是否已经是灰度图
    if len(img.shape) == 2:
        gray_img = img
    else:
        # 转换彩色图像为灰度图
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 检查图像的数据类型并转换为8位
    if gray_img.dtype == np.uint16:
        # 如果是16位图像，转换为8位
        gray_img_8uc1 = cv2.convertScaleAbs(gray_img, alpha=(255.0/65535.0))
    elif gray_img.dtype == np.uint8:
        # 如果已经是8位图像，则直接使用
        gray_img_8uc1 = gray_img
    else:
        # 其他情况，先尝试转换为8位
        gray_img_8uc1 = cv2.normalize(gray_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    return gray_img_8uc1

if __name__ == "__main__":
    image = cv2.imread("../../img_src/1.png", cv2.IMREAD_UNCHANGED)

    image = image_augmentation_19(image)

    cv2.imshow("augmented", image)
    cv2.waitKey(0)