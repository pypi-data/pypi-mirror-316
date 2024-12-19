import cv2
import numpy as np
import random
import sys

def separate_layers(image):
    """
    分离纸张层和文字层。

    参数：
    - image: 输入的图像，彩色或灰度。

    返回：
    - paper_layer: 纸张层图像。
    - text_layer: 文字层图像。
    """
    # 如果是四通道，转换为三通道
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = image[:, :, :3]

    # 判断图像是灰度还是彩色
    if len(image.shape) == 3 and image.shape[2] == 3:
        # 彩色图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        # 灰度图像
        gray = image.copy()

    threshold_value = 40
    ret, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # 使用Otsu's阈值分割来分离文字
    # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 创建文字层
    if len(image.shape) == 3:
        text_mask = cv2.cvtColor(255 - thresh, cv2.COLOR_GRAY2BGR)
        text_layer = cv2.bitwise_and(image, text_mask)
    else:
        text_layer = cv2.bitwise_and(image, 255 - thresh)

    # 创建纸张层
    paper_mask = thresh
    if len(image.shape) == 3:
        paper_mask = cv2.cvtColor(paper_mask, cv2.COLOR_GRAY2BGR)
    paper_layer = cv2.bitwise_and(image, paper_mask)

    return paper_layer, text_layer

def add_shadow(
    paper_layer,
    shadow_side='random',
    shadow_width_range=(0.2, 0.5),
    shadow_color=(0, 0, 0),
    shadow_opacity_range=(0.5, 0.6),
    shadow_blur_kernel_range=(11, 21),
    shadow_type='linear',  # 可选值：'linear', 'wavy', 'expanding', 'random'
    wave_frequency_range=(1, 3),  # 适用于 'wavy' 阴影
    inverse=None,  # 是否反转阴影宽度变化
    add_overexposure=False,  # 是否添加过曝区域
    overexposure_radius_range=(5, 15),  # 过曝区域的半径范围
    overexposure_intensity_range=(0.3, 0.6),  # 过曝区域的强度范围
    overexposure_blur_kernel_range=(5, 11),  # 过曝区域的模糊核大小范围
    random_seed=42
):
    """
    在纸张层上添加不规则阴影和可选的过曝（光晕）效果。

    参数说明：
    - paper_layer: 纸张层图像。
    - shadow_side: 阴影所在的边，'left'，'right'，'top'，'bottom' 或 'random'。
    - shadow_width_range: 阴影宽度占图像尺寸的比例范围（0到1之间）。
    - shadow_opacity_range: 阴影不透明度的范围（0到1之间）。
    - shadow_blur_kernel_range: 阴影模糊核大小的范围（必须为正奇数）。
    - shadow_type: 阴影类型，'linear'（线性），'wavy'（波浪形），'expanding'（扩展）或 'random'。
    - wave_frequency_range: 波浪频率范围，仅适用于 'wavy' 类型。
    - inverse: 是否反转阴影宽度变化方向。
    - add_overexposure: 是否添加过曝效果。
    - overexposure_radius_range: 过曝区域半径的范围。
    - overexposure_intensity_range: 过曝区域强度的范围。
    - overexposure_blur_kernel_range: 过曝区域模糊核大小的范围。
    - random_seed: 随机数种子，用于结果可重复性。

    返回值：
    - paper_with_effects: 添加阴影和过曝效果后的纸张层图像。
    """

    random.seed(random_seed)
    np.random.seed(random_seed)

    h, w = paper_layer.shape[:2]

    # 确定随机阴影边
    if shadow_side == 'random':
        shadow_side = random.choice(['left', 'right', 'top', 'bottom'])

    # 确定随机阴影类型
    if shadow_type == 'random':
        shadow_type = random.choice(['linear', 'wavy', 'expanding'])

    # 随机决定是否反转阴影宽度变化
    if inverse is None:
        inverse = random.choice([True, False])

    # 随机选择阴影参数
    max_shadow_width = random.uniform(*shadow_width_range)
    shadow_opacity = random.uniform(*shadow_opacity_range)
    blur_kernel_size = random.randint(*shadow_blur_kernel_range)
    if blur_kernel_size % 2 == 0:
        blur_kernel_size += 1  # 确保核大小为奇数

    # 创建空白阴影掩码
    shadow_mask = np.zeros((h, w), dtype=np.float32)

    # 根据阴影边和类型生成阴影掩码
    if shadow_side in ['left', 'right']:
        length = h
        max_width_pixels = int(w * max_shadow_width)
        width_variation = get_width_variation(length, max_width_pixels, shadow_type, wave_frequency_range, inverse, random_seed=random_seed)

        for y in range(h):
            current_width = int(width_variation[y])
            if shadow_side == 'left':
                shadow_mask[y, :current_width] = 1.0
            else:
                shadow_mask[y, w - current_width:] = 1.0

    else:  # 'top' 或 'bottom'
        length = w
        max_width_pixels = int(h * max_shadow_width)
        width_variation = get_width_variation(length, max_width_pixels, shadow_type, wave_frequency_range, inverse, random_seed=random_seed)

        for x in range(w):
            current_width = int(width_variation[x])
            if shadow_side == 'top':
                shadow_mask[:current_width, x] = 1.0
            else:
                shadow_mask[h - current_width:, x] = 1.0

    # 对阴影掩码进行模糊处理
    shadow_mask = cv2.GaussianBlur(shadow_mask, (blur_kernel_size, blur_kernel_size), 0)

    # 调整阴影不透明度
    shadow_mask = shadow_mask * shadow_opacity

    # 将纸张层转换为浮点型并归一化
    paper_layer_float = paper_layer.astype(np.float32) / 255.0

    # 确保 paper_layer_float 有三个维度
    if paper_layer_float.ndim == 2:
        # 灰度图像，增加一个通道维度
        paper_layer_float = paper_layer_float[:, :, np.newaxis]

    # 应用阴影到纸张层
    paper_with_shadow = paper_layer_float * (1 - shadow_mask[:, :, np.newaxis])

    # 添加过曝（光晕）效果（如果启用）
    if add_overexposure:
        # 确定阴影的相对边（用于过曝效果的位置）
        opposite_side = get_opposite_side(shadow_side)

        # 确保过曝模糊核大小为奇数
        overexposure_blur_kernel_size = random.randint(*overexposure_blur_kernel_range)
        if overexposure_blur_kernel_size % 2 == 0:
            overexposure_blur_kernel_size += 1

        # 随机选择过曝区域的半径和强度
        radius = random.randint(*overexposure_radius_range)
        intensity = random.uniform(*overexposure_intensity_range)

        # 根据相对边确定可能的中心位置
        if opposite_side in ['left', 'right']:
            y_positions = np.arange(h)
            if opposite_side == 'left':
                x_positions = np.arange(0, int(w * 0.5))
            else:
                x_positions = np.arange(int(w * 0.5), w)
        else:  # 'top' 或 'bottom'
            x_positions = np.arange(w)
            if opposite_side == 'top':
                y_positions = np.arange(0, int(h * 0.5))
            else:
                y_positions = np.arange(int(h * 0.5), h)

        # 创建可能的位置网格
        X, Y = np.meshgrid(x_positions, y_positions)
        possible_positions = np.column_stack((Y.ravel(), X.ravel()))

        # 过滤掉被阴影严重覆盖的位置
        mask_threshold = 0.3  # 可根据需要调整
        mask_values = shadow_mask[possible_positions[:, 0], possible_positions[:, 1]]
        valid_indices = np.where(mask_values < mask_threshold)[0]
        if len(valid_indices) > 0:
            # 随机选择一个有效的位置
            idx = random.choice(valid_indices)
            center_y, center_x = possible_positions[idx]

            # 创建过曝的 alpha 掩码
            y, x = np.ogrid[:h, :w]
            distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            overexposure_mask = np.clip(1 - (distance / radius), 0, 1) * intensity

            # 对过曝掩码进行模糊处理
            overexposure_mask = cv2.GaussianBlur(
                overexposure_mask,
                (overexposure_blur_kernel_size, overexposure_blur_kernel_size),
                0
            )

            # 确保过曝掩码不超过最大强度
            overexposure_mask = np.clip(overexposure_mask, 0, intensity)

            # 创建全白图像用于过曝效果
            white_img = np.ones_like(paper_with_shadow)

            # 扩展过曝掩码以匹配图像通道数
            overexposure_mask_3ch = overexposure_mask[:, :, np.newaxis]

            # 使用 alpha 混合应用过曝效果
            paper_with_effects = paper_with_shadow * (1 - overexposure_mask_3ch) + white_img * overexposure_mask_3ch
        else:
            paper_with_effects = paper_with_shadow
    else:
        paper_with_effects = paper_with_shadow

    # 将值裁剪到 [0, 1] 并转换回 uint8
    paper_with_effects = np.clip(paper_with_effects * 255, 0, 255).astype(np.uint8)

    # 如果原始图像是灰度图像，转换回二维数组
    if paper_layer.ndim == 2 or (paper_layer.ndim == 3 and paper_layer.shape[2] == 1):
        paper_with_effects = paper_with_effects[:, :, 0]

    return paper_with_effects

def get_opposite_side(side):
    """
    Returns the side opposite to the given side.
    """
    opposite = {
        'left': 'right',
        'right': 'left',
        'top': 'bottom',
        'bottom': 'top'
    }
    return opposite.get(side, 'center')

def get_width_variation(length, max_width, shadow_type, wave_frequency_range, inverse, random_seed=42):
    """
    生成阴影宽度的变化数组。

    参数：
    - length: 阴影长度（图像的高或宽）。
    - max_width: 阴影的最大宽度（像素）。
    - shadow_type: 阴影类型，'linear', 'wavy', 'expanding'。
    - wave_frequency_range: 波浪频率范围，仅适用于 'wavy' 类型。
    - inverse: 是否反转宽度变化方向。

    返回：
    - width_variation: 包含每个像素位置阴影宽度的数组。
    """

    random.seed(random_seed)

    if shadow_type == 'linear':
        # 线性变化
        width_variation = np.linspace(0, max_width, length)
    elif shadow_type == 'expanding':
        # 非线性变化（加速或减速）
        width_variation = max_width * np.sin(np.linspace(0, np.pi / 2, length))  # 从0到最大值的sin曲线
    elif shadow_type == 'wavy':
        # 波浪形变化
        frequency = random.uniform(*wave_frequency_range)
        x = np.linspace(0, 2 * np.pi * frequency, length)
        width_variation = (np.sin(x) + 1) / 2 * max_width  # 归一化到0到max_width
    else:
        # 默认线性
        width_variation = np.linspace(0, max_width, length)

    if inverse:
        width_variation = width_variation[::-1]

    return width_variation

# og version
def merge_layers(paper_layer, text_layer, text_alpha=1.0):
    """
    合并纸张层和文字层，并支持调整文字层的透明度。

    参数：
    - paper_layer: 纸张层图像。
    - text_layer: 文字层图像。
    - text_alpha: 文字层的透明度，0到1之间。

    返回：
    - merged: 合并后的图像。
    """
    # 确保图像为float32类型
    paper_layer_f = paper_layer.astype(np.float32)
    text_layer_f = text_layer.astype(np.float32)


    # 使用addWeighted函数合并
    merged = cv2.addWeighted(paper_layer_f, 1.0, text_layer_f, text_alpha, 0)
    merged = np.clip(merged, 0, 255).astype(np.uint8)

    return merged


def main(image, file_name=None, save=False, random_seed=42):
    random.seed(random_seed)

    paper_layer, text_layer = separate_layers(image)

    width, height = image.shape[:2]

    avg = (width + height) / 2

    shadow_blur_kernel_range = (int(0.64 * avg), int(0.71 * avg))
    overexposure_radius_range = (int(0.64 * avg), int(0.71 * avg))
    overexposure_blur_kernel_range = (int(0.05 * avg), int(0.1 * avg))



    paper_with_shadow = add_shadow(
    paper_layer,
    shadow_side='random',
    shadow_blur_kernel_range=shadow_blur_kernel_range,
    shadow_type='random',
    inverse=None,  # Randomly decide whether to inverse
    add_overexposure=True,  # Enable overexposure (halo)
    overexposure_radius_range=overexposure_radius_range,
    overexposure_intensity_range=(0.6, 0.7),  # Adjust intensity as needed
    overexposure_blur_kernel_range=overexposure_blur_kernel_range,
    random_seed=random_seed
)


    # 合并图层
    merged_image = merge_layers(paper_with_shadow, text_layer, text_alpha=1.0)

    if save:
        cv2.imwrite(f"./test/{file_name}_shadow.jpg", merged_image)
    return merged_image

if __name__ == "__main__":
    # 读取图像
    image = cv2.imread('s4.png')

    # 分离图层
    paper_layer, text_layer = separate_layers(image)
    # cv2.imshow("paper", paper_layer)
    # cv2.waitKey(0)

    # 在纸张层添加阴影
    paper_with_shadow = add_shadow(
        paper_layer,
        shadow_side='random',            # 阴影方向
        shadow_vertices_range=(3, 10),   # 阴影形状的顶点数范围
        shadow_width_range=(0.3, 0.8),   # 阴影宽度范围
        shadow_height_range=(0.3, 0.8),  # 阴影高度范围
        shadow_color=(0, 0, 0),          # 阴影颜色
        shadow_opacity_range=(0.2, 0.3), # 阴影不透明度范围   保证比较低，否则会让文字突兀
        shadow_iterations_range=(1, 2),  # 阴影迭代次数范围
        shadow_blur_kernel_range=(101, 201), # 阴影模糊核大小范围
        random_seed=42
    )

    # 合并图层
    merged_image = merge_layers(paper_with_shadow, text_layer, text_alpha=1.0)

    # 保存或显示结果
    # cv2.imwrite('s4_shadowed.png', merged_image)
    cv2.imshow('Merged Image', merged_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()