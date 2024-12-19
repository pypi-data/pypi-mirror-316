import cv2
import numpy as np

def ensure_four_channels(image):
    """
    确保图像为四通道格式，如果不是则转换。
    :param image: 输入图像
    :return: 四通道图像
    """
    if image.ndim == 2 or (image.shape[2] == 1):  # 灰度图
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.shape[2] == 3:  # RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    elif image.shape[2] == 2:  # 灰度+透明度
        bgra = np.zeros((image.shape[0], image.shape[1], 4), dtype=image.dtype)
        bgra[:, :, 0] = image[:, :, 0]
        bgra[:, :, 1] = image[:, :, 0]
        bgra[:, :, 2] = image[:, :, 0]
        bgra[:, :, 3] = image[:, :, 1]
        image = bgra
    return image

def blend_images(foreground_image, background_image, alpha=0.8):
    """
    将两张图像按照指定的透明度进行叠加。
    :param foreground_image: 前景图，其透明度将被调整。
    :param background_image: 背景图。
    :param alpha: 前景图的透明度，范围从0到1，其中1表示完全不透明。
    :return: 叠加后的图像。
    """
    # 确保图像为四通道
    foreground_image = ensure_four_channels(foreground_image)
    background_image = ensure_four_channels(background_image)

    target_size = (background_image.shape[1], background_image.shape[0])
    foreground_image = cv2.resize(foreground_image, target_size, interpolation=cv2.INTER_LANCZOS4)

    # 调整前景图的透明度
    foreground_alpha = foreground_image[:, :, 3] * alpha
    background_alpha = background_image[:, :, 3] * (1 - alpha)

    # 新的alpha通道
    new_alpha = foreground_alpha + background_alpha

    # 计算RGB通道
    foreground_rgb = foreground_image[:, :, :3].astype(float)
    background_rgb = background_image[:, :, :3].astype(float)
    new_rgb = cv2.addWeighted(foreground_rgb, alpha, background_rgb, 0.6, 0)

    # 合并RGB通道和新的Alpha通道
    blended_image = np.dstack((new_rgb, new_alpha))

    # 将结果图像的数据类型改回uint8
    return blended_image.astype(np.uint8)

if __name__ == "__main__":

    # 示例读取和使用
    # 读取图像，确保使用cv2.IMREAD_UNCHANGED保留所有通道
    # 前景图为深色纹理，背景图为合成后半成品
    foreground = cv2.imread('./texture_dst/texture_8.png', cv2.IMREAD_UNCHANGED)
    background = cv2.imread('./enhanced_image/clean_15726443_01_aug_2.png', cv2.IMREAD_UNCHANGED)

    # 叠加图像
    blended_image = blend_images(foreground, background, alpha=0.3)

    # 显示结果
    cv2.imshow('Blended Image', blended_image[:, :, :3])  # 只显示RGB通道
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("./texture_created/texture_8_15.png", blended_image)