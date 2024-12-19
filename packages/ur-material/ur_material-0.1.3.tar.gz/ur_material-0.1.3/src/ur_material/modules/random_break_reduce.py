import cv2
import numpy as np
import random

def add_random_speckles_mask(image_shape, num_points=4000, random_seed=42):
    """
    生成具有随机不规则形状黑色斑点的掩码。

    参数：
    - image_shape: 图像的形状（高度，宽度，通道数）
    - num_points: 添加的黑色斑点数量
    - random_seed: 随机数种子

    返回值：
    - mask: 掩码，具有与输入图像相同的高度和宽度，单通道
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    height, width = image_shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    if num_points is None:
        num_points = random.randint(10, 15)

    for _ in range(num_points):
        # 生成斑点的随机中心坐标
        center_x = random.randint(0, width - 1)
        center_y = random.randint(0, height - 1)

        # 生成不规则形状的随机顶点
        vertices = []
        num_vertices = random.randint(3, 6)  # 3-6个顶点的多边形
        for _ in range(num_vertices):
            angle = random.uniform(0, 2 * np.pi)
            radius = random.randint(2, 3)        # 调整斑点大小
            vertex_x = int(center_x + radius * np.cos(angle))
            vertex_y = int(center_y + radius * np.sin(angle))
            # 确保顶点在图像边界内
            vertex_x = np.clip(vertex_x, 0, width - 1)
            vertex_y = np.clip(vertex_y, 0, height - 1)
            vertices.append([vertex_x, vertex_y])

        # 将顶点转换为适合cv2.polylines的numpy数组
        pts = np.array(vertices, np.int32)
        pts = pts.reshape((-1, 1, 2))

        # 在掩码上绘制不规则多边形
        cv2.fillPoly(mask, [pts], 255)

    return mask

def apply_mask_on_image(image, mask, reduce_percentage=0.4, method='reduce'):
    """
    使用掩码对图像进行涂白或颜色降低处理。

    参数：
    - image: 输入图像（通过cv2.imread读取）
    - mask: 与图像高度和宽度相同的掩码
    - reduce_percentage: 颜色降低的比例（0到1之间）
    - method: 处理方法，'reduce'表示降低颜色，'white'表示涂白

    返回值：
    - 处理后的图像
    """
    processed_image = image.copy()
    channels = processed_image.shape[2] if len(processed_image.shape) > 2 else 1

    if method == 'white':
        # 涂白处理
        if channels == 1:
            processed_image[mask == 255] = 255
        else:
            for c in range(channels):
                img_channel = processed_image[:, :, c]
                img_channel[mask == 255] = 255
                processed_image[:, :, c] = img_channel
    elif method == 'reduce':
        # 颜色降低处理
        if channels == 1:
            mask_indices = mask == 255
            processed_image[mask_indices] = (
                processed_image[mask_indices] + (255 - processed_image[mask_indices]) * reduce_percentage
            ).astype(np.uint8)
        else:
            for c in range(channels):
                img_channel = processed_image[:, :, c]
                img_channel[mask == 255] = (
                    img_channel[mask == 255] + (255 - img_channel[mask == 255]) * reduce_percentage
                ).astype(np.uint8)
                processed_image[:, :, c] = img_channel
    else:
        raise ValueError("Invalid method. Use 'white' or 'reduce'.")

    return processed_image

def process(image, reduce_percentage=0.4, method="white", num_points=4000, file_name=None, save=False, random_seed=42):
    mask = add_random_speckles_mask(image.shape, random_seed=random_seed)
    image = apply_mask_on_image(image, mask, reduce_percentage=reduce_percentage, method=method)
    return image

# 示例使用
if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('../img_src/1022104527_01df78fd-245d-4301-9e5b-19690d0206a9.png', cv2.IMREAD_UNCHANGED)

    # 生成斑点掩码
    mask = add_random_speckles_mask(image.shape, random_seed=42)

    # 对掩码区域进行颜色降低或涂白处理
    processed_image = apply_mask_on_image(image, mask, reduce_percentage=0.4, method='reduce')

    # 显示并保存处理后的图像
    cv2.imshow('Processed Image', processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite('processed_image.png', processed_image)