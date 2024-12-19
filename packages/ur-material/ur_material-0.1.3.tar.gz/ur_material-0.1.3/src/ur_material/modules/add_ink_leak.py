import os
import cv2
from ur_material.modules import ink_leak_final
from ur_material.modules import overlap_final
from ur_material.modules import make_it_old_final
import random
import numpy as np
import cProfile
from augraphy import *
def increase_ink_by_percentage(image, percentage, file_name=None, save=False):
    mask = image < 255
    # 计算新的像素值
    image[mask] = (image[mask] + (255 - image[mask]) * percentage).astype(np.uint8)

    return image


def make_old(image):
    reduce_percentage = 1.1

    mask = image < 255
    # 计算新的像素值
    image[mask] = (image[mask] + (255 - image[mask]) * reduce_percentage).astype(np.uint8)

    return image


def make_old_partially(image, num_regions=(20,50), region_size=(60, 100), random_seed=42):
    random.seed(random_seed)

    height, width = image.shape[:2]
    output_image = np.copy(image)

    region_height = random.randint(0, height//10)
    region_width = random.randint(0, width//10)

    region_size = (region_height, region_width)

    num_regions = random.randint(num_regions[0], num_regions[1])

    for _ in range(num_regions):
        # 随机确定区域的位置
        x = random.randint(0, width - region_size[1])
        y = random.randint(0, height - region_size[0])

        # 在选定的区域应用增墨
        output_image[y:y+region_size[0], x:x+region_size[1]] = make_old(image[y:y+region_size[0], x:x+region_size[1]])

    return output_image

def pre_bleed(image, file_name=None, save=False):
    kernel = np.ones((2,2), np.uint8)

    image = cv2.erode(image, np.ones((1,1), np.uint8), iterations=1)

    # image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=2)

    # image = cv2.dilate(image, kernel, iterations=1)

    ret, image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=2)

    return image


def bleed(image, file_name=None, save=False, kernel_size=(4,4)):

    inkbleed = InkBleed(intensity_range=(0.4, 0.7),
                    kernel_size=kernel_size,
                    severity=(0.2, 0.4)
                    )

    image = inkbleed(image)

    return image



def add_ink_leak_method(image, file_name=None, save=False, partial_old=False, region_size=(60, 80), random_seed=42):

    random.seed(random_seed)

    # if len(image.shape) != 2:
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    source_image = image
    old_image = make_it_old_final.make_it_old(image, random_seed=random_seed)
    ink_leak_image = ink_leak_final.ink_leak(old_image)
    # .shape[1]: width    .shape[2]: height
    source_size = (source_image.shape[1], source_image.shape[0])

    ink_leak_image = cv2.resize(ink_leak_image, source_size, interpolation=cv2.INTER_LANCZOS4)

    # 设定平移距离，tx和ty分别为水平和垂直方向的平移距离
    tx, ty = 50, 30  # 你可以根据需要调整这些值

    # 创建平移矩阵
    M = np.float32([[1, 0, tx], [0, 1, ty]])

    # 使用warpAffine进行平移
    # 参数cv2.BORDER_CONSTANT指定边界填充为常数，这里使用白色填充
    shifted_image = cv2.warpAffine(ink_leak_image, M, (ink_leak_image.shape[1], ink_leak_image.shape[0]), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    # cv2.imshow("shifted img", shifted_image)
    # cv2.waitKey(0)
    # cv2.imshow("src img", source_image)
    # cv2.waitKey(0)

    result_image = overlap_final.overlap(shifted_image, source_image)
    # result_image = overlap_final.overlap(source_image, shifted_image)

    if save:
        cv2.imwrite(f"./test/{file_name}_inkleak.jpg", result_image)

    # partially add ink
    if partial_old:
        if result_image.shape[0] > region_size[0] and result_image.shape[1] > region_size[1]:
            result_image = make_old_partially(result_image, region_size, random_seed=random_seed)
        else:
            pass


    return result_image

if __name__ == "__main__":
    img_path = '../clean/clean_15726443_01.png'
    filename = os.path.basename(img_path).split('.')[0]
    image = cv2.imread(img_path)

    image = add_ink_leak(image,filename, save=True, partial_old=True)
    # cProfile.run('add_ink_leak(image,filename, save=True, partial_old=True)')
    cv2.imshow('result', image)
    cv2.waitKey(0)