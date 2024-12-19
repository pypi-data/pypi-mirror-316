import cv2
import numpy as np
import random

def process_image(image, num_shapes=200, reduce_percentage=0.4, method='white',file_name=None, save=False, random_seed=42):
    """
    对输入的图像进行二值化，然后在内容部分随机选择一些区域进行涂白或降低颜色处理。

    参数：
    - image: 输入的图像（通过cv2.imread读取）。
    - num_shapes: 随机形状的数量。
    - reduce_percentage: 颜色降低的比例（0到1之间）。
    - method: 处理方法，'reduce'表示降低颜色，'white'表示涂白。

    返回值：
    - 处理后的图像。
    """

    random.seed(random_seed)
    np.random.seed(random_seed)

    height, width = image.shape[:2]
    channels = image.shape[2] if len(image.shape) > 2 else 1

    if image.dtype == np.uint16:
        # 创建一个新的空白图像用于输出
        img_8uc1 = np.zeros(image.shape, dtype=np.uint8)

        # 将16位图像转换为8位
        cv2.convertScaleAbs(image, dst=img_8uc1, alpha=(255.0/65535.0))

        image = img_8uc1

    # 将图像转换为灰度并二值化
    if channels > 1:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 找到内容区域的轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 创建一个内容区域的掩码
    content_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.drawContours(content_mask, contours, -1, 255, -1)

    # 在内容区域上随机生成形状
    shape_mask = np.zeros((height, width), dtype=np.uint8)
    shape_types = ['circle', 'rectangle']  # 形状类型

    # 获取内容区域的像素坐标
    content_indices = np.column_stack(np.where(content_mask == 255))

    for _ in range(num_shapes):
        shape_type = random.choice(shape_types)

        # 从内容区域中随机选择一个点作为形状的参考点
        if len(content_indices) == 0:
            break  # 如果内容区域为空，退出循环
        idx = random.randint(0, len(content_indices) - 1)
        ref_point = tuple(content_indices[idx])

        if shape_type == 'circle':
            # 随机生成圆形
            radius = random.randint(4, 5)  # 半径范围，可根据需要调整
            cv2.circle(shape_mask, ref_point, radius, 255, -1)
        else:
            # 随机生成矩形
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            top_left = (max(ref_point[1] + x_offset, 0), max(ref_point[0] + y_offset, 0))
            bottom_right = (min(top_left[0] + random.randint(5, 10), width), min(top_left[1] + random.randint(5, 10), height))
            cv2.rectangle(shape_mask, top_left, bottom_right, 255, -1)


    # 将形状掩码与内容掩码相交
    final_mask = cv2.bitwise_and(content_mask, shape_mask)

    # 处理图像
    processed_image = image.copy()

    if method == 'white':
        # 涂白处理
        if channels == 1:
            processed_image[final_mask == 255] = 255
        else:
            for c in range(channels):
                img_channel = processed_image[:, :, c]
                img_channel[final_mask == 255] = 255
                processed_image[:, :, c] = img_channel
    # elif method == 'reduce':
    #     # 按比例降低颜色
    #     if channels == 1:
    #         mask_indices = final_mask == 255
    #         processed_image[mask_indices] = (
    #             processed_image[mask_indices] + (255 - processed_image[mask_indices]) * reduce_percentage
    #         ).astype(np.uint8)
    #     else:
    #         for c in range(channels):
    #             img_channel = processed_image[:, :, c]
    #             img_channel[final_mask == 255] = (
    #                 img_channel[final_mask == 255] + (255 - img_channel[final_mask == 255]) * reduce_percentage
    #             ).astype(np.uint8)
    #             processed_image[:, :, c] = img_channel
    else:
        raise ValueError("Invalid method. Use 'white' or 'reduce'.")

    return processed_image

# 示例使用
if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('../img_src/1022104527_01df78fd-245d-4301-9e5b-19690d0206a9.png', cv2.IMREAD_UNCHANGED)

    # 调用处理函数
    processed_image = process_image(image, num_shapes=20, reduce_percentage=0.1, method='white', random_seed=42)

    # 显示并保存处理后的图像
    cv2.imshow('Processed Image', processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite('processed_image.png', processed_image)