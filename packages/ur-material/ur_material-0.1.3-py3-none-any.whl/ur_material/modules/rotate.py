import cv2
import numpy as np
import random

def rotate_method(image, file_name=None, save=False, random_seed=42):
    """
    旋转图像并用指定颜色填充空白区域。
    
    :param image: 输入的图像
    :param angle: 旋转的角度，正值为逆时针，负值为顺时针
    :param fill_color: 填充颜色，默认为白色
    :return: 旋转后的图像
    """
    random.seed(random_seed)

    interval = [(-5,-2), (2,5)]

    selected_interval = random.choice(interval)

    angle = random.uniform(*selected_interval)
    fill_color = (255,255,255)

    # 获取图像尺寸
    height, width = image.shape[:2]

    # 计算旋转中心
    center = (width // 2, height // 2)

    # 计算旋转矩阵
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 计算新图像的尺寸
    cos = np.abs(matrix[0, 0])
    sin = np.abs(matrix[0, 1])

    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))

    # 调整旋转矩阵以考虑平移
    matrix[0, 2] += (new_width / 2) - center[0]
    matrix[1, 2] += (new_height / 2) - center[1]

    # 执行仿射变换
    rotated = cv2.warpAffine(image, matrix, (new_width, new_height), borderValue=fill_color)

    return rotated

if __name__ == "__main__":
    # 读取图像
    image_path = '../media/image5.png'
    image = cv2.imread(image_path)

    # 旋转图像
    rotated_image = rotate(image, -7)  # 旋转45度逆时针

    # 显示图像
    cv2.imshow('Original Image', image)
    cv2.waitKey(0)
    cv2.imshow('Rotated Image', rotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()