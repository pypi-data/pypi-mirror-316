import cv2
import numpy as np
import random
import genalog.degradation.effect as effect
from ur_material.modules import add_ink_leak
from augraphy import *


import os
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

def apply_pepper_noise_in_regions(image, num_region=(20,50), region_size=(100, 100), noise_amount=0.05, random_seed=42):

    random.seed(random_seed)

    height, width = image.shape[:2]
    output_image = np.copy(image)

    num_regions = random.randint(num_region[0], num_region[1])

    for _ in range(num_regions):
        # 随机确定区域的位置
        x = random.randint(0, width - region_size[1])
        y = random.randint(0, height - region_size[0])

        # 在选定的区域应用椒盐噪声
        output_image[y:y+region_size[0], x:x+region_size[1]] = effect.pepper(
            output_image[y:y+region_size[0], x:x+region_size[1]], amount=noise_amount)

    return output_image

def apply_salt_noise_in_regions(image, num_region=(20,50), region_size=(100, 100), noise_amount=0.05, random_seed=42):

    random.seed(random_seed)

    height, width = image.shape[:2]
    output_image = np.copy(image)

    num_regions = random.randint(num_region[0], num_region[1])

    for _ in range(num_regions):
        # 随机确定区域的位置
        x = random.randint(0, width - region_size[1])
        y = random.randint(0, height - region_size[0])

        # 在选定的区域应用椒盐噪声
        output_image[y:y+region_size[0], x:x+region_size[1]] = effect.salt(
            output_image[y:y+region_size[0], x:x+region_size[1]], amount=noise_amount)

    return output_image
    

def erode_alot_l(image, file_name=None, save=False):
    # 先腐蚀，增加黑色面积，然后做lines_degradation，起到
    # 随机增加减少的效果，然后膨胀，然后二值化，然后做后续细处理（增墨，墨渍，jpeg压缩）

    kernel = np.ones((2,2), np.uint8)

    image = cv2.erode(image, np.ones((1,1), np.uint8), iterations=1)

    # image = add_ink_leak.make_old(image)


    lines_degradation = LinesDegradation(line_roi = (0.0, 0.0, 1.0, 1.0),
                                     line_gradient_range=(100, 150),
                                     line_gradient_direction= (2,2),
                                     line_split_probability=(0.2, 0.3),
                                     line_replacement_value=(125,125),
                                     line_min_length=(15, 15),
                                     line_long_to_short_ratio = (3,3),
                                     line_replacement_probability = (0.5, 0.6),
                                     line_replacement_thickness = (2, 2)
                                     )

    image = lines_degradation(image)

    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=2)

    image = cv2.dilate(image, kernel, iterations=2)

    ret, image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=2)


    inkbleed = InkBleed(intensity_range=(0.4, 0.7),
                    kernel_size=(2, 2),
                    severity=(0.2, 0.4)
                    )

    image = inkbleed(image)

    # jpeg quality reduce
    jpeg_5 = Jpeg(quality_range=(30, 40))
    image = jpeg_5(image)
    
    return image

def erode_alot_s(image, file_name=None, save=False):
    # 先腐蚀，增加黑色面积，然后做lines_degradation，起到
    # 随机增加减少的效果，然后膨胀，然后二值化，然后做后续细处理（增墨，墨渍，jpeg压缩）

    kernel = np.ones((1,1), np.uint8)

    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=1)

    lines_degradation = LinesDegradation(line_roi = (0.0, 0.0, 1.0, 1.0),
                                    line_gradient_range=(0, 255),
                                    line_gradient_direction= (2,2),
                                    line_split_probability=(0.2, 0.3),
                                    line_replacement_value=(250,250),
                                    line_min_length=(15, 15),
                                    line_long_to_short_ratio = (3,3),
                                    line_replacement_probability = (1.0, 1.0),
                                    line_replacement_thickness = (2, 2)
                                    )

    image = lines_degradation(image)

    image = cv2.dilate(image, kernel, iterations=2)



    inkbleed = InkBleed(intensity_range=(0.4, 0.7),
                    kernel_size=(3, 3),
                    severity=(0.2, 0.4)
                    )

    image = inkbleed(image)

    # jpeg quality reduce
    jpeg_5 = Jpeg(quality_range=(5, 10))
    image = jpeg_5(image)
    
    return image

# 实现图片内容做旧的效果
def make_it_old(image, file_name=None, save=False, partial_old=False, random_seed=42):

    random.seed(random_seed)
    


    # 大图dilate size： 2， erode size： 4

    erode_size = 4
    dilate_size = 2


    if image.ndim > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    og_width = image.shape[1]
    og_height = image.shape[0]

    # 提升图片像素
    new_width = image.shape[1] * 3
    new_height = image.shape[0] * 3

    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    threshold_value = 200

    # 对灰度图进行二值化处理
    # ret, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    ret, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel_dilate = np.ones((dilate_size,dilate_size), np.uint8)
    kernel_erode = np.ones((erode_size,erode_size), np.uint8)

    
    # 腐蚀膨胀针对的都是白色区域
    image = cv2.dilate(binary_image,kernel_dilate, iterations=2)   # 白色膨胀， 黑色变小
    image = cv2.erode(image, kernel_erode, iterations=2)    # 白色被腐蚀，黑色变大


    image = cv2.resize(image, (og_width, og_height), interpolation=cv2.INTER_LANCZOS4)

    # partially apply salting
    if partial_old:
        if image.shape[0] > 100 and image.shape[1] > 100:
            image = apply_salt_noise_in_regions(image, num_region=(20,50), region_size=(100, 100), noise_amount=0.3, random_seed=random_seed)
            image = apply_pepper_noise_in_regions(image, num_region=(10,15), region_size=(30, 50), noise_amount=0.05, random_seed=random_seed)
        elif image.shape[0] > 30 and image.shape[1] > 50:
            image = apply_pepper_noise_in_regions(image, num_region=(10,15), region_size=(30, 50), noise_amount=0.05, random_seed=random_seed)
        else:
            pass

    if save:
        cv2.imwrite(f"./test/{file_name}_inkadd.jpg", image)

    return image