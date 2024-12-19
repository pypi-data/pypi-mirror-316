import cv2
import numpy as np

# check if an image contains gray parts, so that it can't be binaryzied
# return true if there are gray parts
def contains_gray_method(image, threshold=10, gray_range=(30, 30)):  #gray_range=(70, 230)
    """
    判断给定的灰度图像是否包含灰色阴影。
    :param image: cv2读取后的灰度图像
    :param threshold: 阈值，用于判断灰色像素的数量是否足够多
    :param gray_range: 灰色范围，非纯黑和纯白之间的灰度值区间
    :return: True 如果图像包含灰色阴影，否则 False
    """
    # 检查图像是否已经是灰度图
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        pass
    # 计算灰度直方图
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # 计算gray_range内的像素总数
    gray_pixel_count = np.sum(hist[gray_range[0]:gray_range[1]])

    # 判断是否含有显著的灰色阴影
    return gray_pixel_count > threshold