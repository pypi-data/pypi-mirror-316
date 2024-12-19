import json
import random
from PIL import Image
import os
import cv2
from ur_material.modules import add_shadow_final, add_watermark, add_ink_leak, perspective_transform, make_it_old_final, ink_reduce\
    , general_quality_reduce, half_paper, add_dots
from ur_material.modules import warp_texture_blur_sticker
from tqdm import tqdm
from pqdm.processes import pqdm
from augraphy import *
import numpy as np
from functools import partial
import subprocess
import shutil
import argparse

def image_augmentation_1(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=save)
    image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, random_seed=random_seed, save=save)
    if random.random() < 0.5:
        image = perspective_transform.main(image, save=save, random_seed=random_seed)
    image = add_watermark.add_water_mark(image, save=False, random_seed=random_seed)
    return image

def image_augmentation_2(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, random_seed=random_seed, save=save)
    if random.random() < 0.8:
        image = perspective_transform.main(image, save=save, random_seed=random_seed)
    image = add_ink_leak.increase_ink_by_percentage(image, 1.1, save=False)
    image = warp_texture_blur_sticker.add_texture(image, save=save, random_seed=random_seed)
    image = add_ink_leak.add_ink_leak_method(image, save=False, random_seed=random_seed)
    if random.random() < 0.5:
        image = warp_texture_blur_sticker.increase_darkness(image, save=False, random_seed=random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    image = add_shadow_final.main(image, save=save, random_seed=random_seed)
    return image

def image_augmentation_3(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.make_it_old(image, save=False, random_seed=random_seed)
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    if random.random() < 0.8:
        image = perspective_transform.main(image, save=False, random_seed=random_seed)
        image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, save=False, random_seed=random_seed)
    return image

def image_augmentation_4(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = add_ink_leak.add_ink_leak_method(image, save=False, partial_old=True, random_seed=random_seed)   # partial_old=True
    image = warp_texture_blur_sticker.motionblur(image, save=False)
    if random.random() < 0.8:
        image = perspective_transform.main(image, save=save, random_seed=random_seed)
    return image

def image_augmentation_5(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = perspective_transform.main(image, save=save, random_seed=random_seed)
    image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, random_seed=random_seed, save=save)
    image = warp_texture_blur_sticker.motionblur(image, save=save)
    return image

def image_augmentation_6(image, save=False, random_seed=42): 
    image = pre_process(image)
    random.seed(random_seed)
    image = ink_reduce.ink_reduce_method(image, 0.3, save=False)
    return image

def image_augmentation_7(image, save=False, random_seed=42):   
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.make_it_old(image, save=False, random_seed=random_seed)
    image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, random_seed=random_seed, save=False)
    image = add_ink_leak.add_ink_leak_method(image, save=False, random_seed=random_seed)
    return image

def image_augmentation_8(image, save=False, random_seed=42):  
    image = pre_process(image)   
    random.seed(random_seed)
    image = make_it_old_final.make_it_old(image, save=False, partial_old=True, random_seed=random_seed)  # partial_old=True
    image = warp_texture_blur_sticker.add_texture(image, save=False, random_seed=random_seed)
    # if random.random() < 0.3:
    #     image = scanned.main(image, save=False)
    return image

def image_augmentation_9(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.erode_alot_l(image, save=False)
    if random.random() < 0.5:
        image, crop_amount = warp_texture_blur_sticker.elastic_transform(image, save=False,random_seed=random_seed)
    return image

def image_augmentation_10(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = general_quality_reduce.reduce(image, (30, 40), (2,2), save=False)
    return image

def image_augmentation_11(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = ink_reduce.dilate_erode_reduce(image, save=False)
    image = ink_reduce.ink_reduce_method(image, 0.2, save=False)
    image = general_quality_reduce.reduce(image, (20, 30), (2,2), save=False)
    return image

def image_augmentation_12(image, save=False, random_seed=42):
    image = pre_process(image)
    random.seed(random_seed)
    image = make_it_old_final.erode_alot_l(image, save=False)
    image = half_paper.half_paper_method(image, save=False, random_seed=random_seed)
    return image

def image_augmentation_13(image, save=False, random_seed=42):
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

def image_augmentation_14(image, save=False, random_seed=42):
    image = pre_process(image)
    image = add_dots.add_random_speckles(image, save=save, random_seed=random_seed)
    image = add_ink_leak.bleed(image, save=save, kernel_size=(2,2))
    # image = scanned.main(image, save=save)
    image = general_quality_reduce.blur(image, (5,5), save=save)
    image = general_quality_reduce.reduce(image, (40,50), (3,3), save=save)
    
    return image

def image_augmentation_15(image, save=False, random_seed=20):
    image = pre_process(image)
    image = add_ink_leak.increase_ink_by_percentage(image, 1.1, save=False)
    image, crop_amount = warp_texture_blur_sticker.elastic_transform(image,alpha_range=100, movement=100, random_seed=random_seed, save=save)
    image = warp_texture_blur_sticker.add_texture(image, save=save, random_seed=random_seed)
    image = add_ink_leak.add_ink_leak_method(image, save=False, random_seed=random_seed)
    image = general_quality_reduce.blur(image, (3,3), save=save)

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

# convert image to grayscale
def pre_process(image):
    num_channels = image.shape[2] if len(image.shape) == 3 else 1
    if num_channels > 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    image = convert_to_grayscale_8uc1(image)

    return image