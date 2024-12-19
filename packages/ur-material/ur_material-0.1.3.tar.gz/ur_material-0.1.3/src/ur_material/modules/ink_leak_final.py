import cv2
import numpy as np
import genalog.degradation.effect as effect
from genalog.degradation.degrader import Degrader
from ur_material.modules import overlap_final

# Step 1: 读取灰度图像
def ink_leak(image):

    if len(image.shape) != 2:
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # percentage to imply how severe texts are reduced
    # less percentage, less reduced
    reduce_percentage = 0.9
    mask = image < 255
    # 计算新的像素值
    image[mask] = (image[mask] + (255 - image[mask]) * reduce_percentage).astype(np.uint8)

    # setup threshold to filter parts totally leak over the page
    threshold_value = 150
    ret, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)


    image1_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image2_rgb = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)

    combined_image = overlap_final.overlap(image1_rgb, image2_rgb)

    # 腐蚀方法

    # kernel = np.ones((2,2), np.uint8)

    # dilated_image = cv2.dilate(combined_image, kernel, iterations=1)
    # dilated_image = cv2.dilate(image1_rgb, kernel, iterations=1)


    # 盐化方法
    degradations = [
        ("salt", {"amount": 0.8}),
    ]
    # All of the referenced degradation effects are in submodule `genalog.degradation.effect`

    degrader = Degrader(degradations)
    dilated_image = degrader.apply_effects(combined_image)


    # flip the image
    dilated_image = cv2.flip(dilated_image, 1)


    def reduce_non_white_pixels(image, reduction_factor=0.8):
        """降低非白色像素的值，白色保持不变"""
        result_image = image.copy()
        
        # 对所有非白色像素应用比例降低
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] < 255:  # 非白色像素
                    result_image[i, j] = int(image[i, j] * reduction_factor)
        
        return result_image

    return dilated_image

