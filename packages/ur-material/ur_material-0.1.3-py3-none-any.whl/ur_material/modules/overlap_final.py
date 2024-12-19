import cv2
import numpy as np

def overlap(background_image_path, foreground_image_path, from_path=None):

    # foreground_image is the content
    # background_image is watermark or something else
    background_image = background_image_path
    foreground_image = foreground_image_path

    if len(background_image.shape) == 2:
        background_image = cv2.cvtColor(background_image, cv2.COLOR_GRAY2BGR)

    if len(foreground_image.shape) == 2:
        foreground_image = cv2.cvtColor(foreground_image, cv2.COLOR_GRAY2BGR)

    # keep both size to content(forground_image)
    target_size = (foreground_image.shape[1], foreground_image.shape[0])
    background_image = cv2.resize(background_image, target_size, interpolation=cv2.INTER_LANCZOS4)
    # foreground_image = cv2.resize(foreground_image, target_size, interpolation=cv2.INTER_LANCZOS4)

    # Step 1: 确保前景图像有4个通道（BGRA）
    if foreground_image.shape[2] == 3:  # 如果只有3通道，添加Alpha通道
        foreground_image = cv2.cvtColor(foreground_image, cv2.COLOR_BGR2BGRA)

    # Step 3: 确保背景图像也有Alpha通道，如果没有则添加
    if background_image.shape[2] == 3:  # 背景图像只有BGR通道
        background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2BGRA)

    bgr = foreground_image[:, :, :3]  # 获取BGR通道
    alpha = foreground_image[:, :, 3]  # 获取Alpha通道

    # 创建一个遮罩，标识前景图像中接近白色的背景区域
    mask = cv2.inRange(bgr, (240, 240, 240), (255, 255, 255))  # 选择接近白色的区域为背景

    # 将背景区域的Alpha值设为0（透明），内容区域的Alpha值设为255（不透明）
    alpha[mask == 255] = 0    # 背景区域
    alpha[mask != 255] = 255  # 内容区域
    foreground_image[:, :, 3] = alpha  # 更新前景图像的Alpha通道
    
    # Step 4: 使用Alpha混合将前景图像叠加到背景图像上s
    # 归一化Alpha通道到0到1之间的浮点数
    alpha_foreground = alpha / 255.0
    alpha_background = 1.0 - alpha_foreground

    # 初始化结果图像
    blended_image = np.zeros_like(foreground_image)

    # 对每个颜色通道进行Alpha混合
    for c in range(0, 3):
        blended_image[:, :, c] = (alpha_foreground * foreground_image[:, :, c] +
                                alpha_background * background_image[:, :, c])

    # 如果需要保留Alpha通道，可以如下处理
    blended_image[:, :, 3] = np.maximum(foreground_image[:, :, 3], background_image[:, :, 3])

    return blended_image

if __name__=="__main__":
    colored = cv2.imread("./texture_yellow/texture_42.png", cv2.IMREAD_UNCHANGED)
    foreground = cv2.imread("./img_src/clean_15726443_02.png", cv2.IMREAD_UNCHANGED)
    result = overlap(colored, foreground)
    cv2.imshow("result", result)
    cv2.waitKey(0)