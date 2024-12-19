import os

import cv2
import numpy as np
import random
from tqdm import tqdm
from pqdm.processes import pqdm
# from demo import is_significant_overlap

def crop_white_borders(image_path, output_path, padding=0, save=False, from_path=True, with_watermarks=False, with_page=False):
    if from_path:
        image = cv2.imread(image_path)
        image_gray = cv2.imread(image_path, 0)
    else:
        image = image_path
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if with_watermarks:
        image = image[:int(image.shape[0]/3),:]
        image_gray = image_gray[:int(image.shape[0] / 3), :]
    if with_page:
        image = image[:int(image.shape[0]-100),:]
        image_gray = image_gray[:int(image.shape[0]-100), :]
    _, binary = cv2.threshold(image_gray, 254, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite('1.png',binary)
    # contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # x, y, w, h = cv2.boundingRect(contours[0])
    # cropped_image = image[y:y+h, x:x+w]
    # 找到非白色区域的边界框
    rows, cols = binary.shape
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1
    # 找到边界
    for i in range(rows):
        if np.sum(binary[i, :]) != 0:
            top = i
            break
    for i in range(rows - 1, -1, -1):
        if np.sum(binary[i, :]) != 0:
            bottom = i
            break
    for i in range(cols):
        if np.sum(binary[:, i]) != 0:
            left = i
            break
    for i in range(cols - 1, -1, -1):
        if np.sum(binary[:, i]) != 0:
            right = i
            break
    if (top < padding) or (bottom + 1 + padding) > image.shape[0] or (left < padding) or (right + 1 + padding) > image.shape[1]:
        padding = 0
    cropped_image = image[(top - padding):(bottom + 1 + padding), (left - padding):(right + padding)]
    if save:
        cv2.imwrite(output_path, cropped_image)
    return cropped_image

def generate_random_points(width, height, num_points=10, random_seed=42):

    random.seed(random_seed)

    points = []
    for _ in range(num_points):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        points.append((x, y))
    return points

def expand_points(points, binary_image):
    max_empty_area = 0
    max_empty_rect = None
    height, width = binary_image.shape
    for (rx, ry) in points:
        if binary_image[ry, rx] == 0:  # 如果点在黑色区域，跳过
            continue
        max_w, max_h = width - rx, height - ry
        for rw in range(1, max_w):
            for rh in range(1, max_h):
                if rx + rw >= width or ry + rh >= height:
                    break
                if np.any(binary_image[ry:ry+rh, rx:rx+rw] == 0):  # 如果区域内包含黑色像素，跳过
                    break
                area = rw * rh
                if area > max_empty_area:
                    max_empty_area = area
                    max_empty_rect = (rx, ry, rw, rh)
    return max_empty_rect

def find_max_white_region(binary_image, random_seed=42):

    random.seed(random_seed)

    height, width = binary_image.shape
    random_points = generate_random_points(width, height, num_points=10)
    max_white_rect = expand_points(random_points, binary_image)
    return max_white_rect

def bg_extraction_method(output_file,file_image="./hs_che_examples/0ca9e36096694648a90cfa8817c836e6.jpg", save=True):
    # image_gray = cv2.imread(file_image, 0)
    image = crop_white_borders(file_image, "s0.jpg", save=False)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    max_white_rect = find_max_white_region(binary_image)
    x, y, w, h = max_white_rect
    # result_image = cv2.rectangle(image, (x, y), (x + w, y + h), (127, 127, 127), 2)
    bg = image[y:y+h, x:x+w]
    # cv2.imwrite("s4.jpg", result_image)
    bg_height, bg_width = bg.shape[:2]
    bg_area = bg_height * bg_width
    # _, binary_image_bg = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY)
    if save and bg_area > 2000 and np.sum(bg == 255)/bg.size <= 0.8 and bg_height>40 and bg_width>40:
        cv2.imwrite(output_file, bg)

def crop_watermark(image):
    cropped_image = image[:, 40:]
    return cropped_image

if __name__ == "__main__":
    # bg_folder_path = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\enhanced-image\bg\texture"
    # cmd = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\mask\images\little_images_11000_processed\process"
    # filenames = [f for f in os.listdir(cmd)][1639:]
    # for file in tqdm(filenames):
    #     img_path = os.path.join(cmd, file)
    #     file_name = os.path.splitext(file)[0]
    #     output_file = os.path.join(bg_folder_path, file)
    #     bg_extraction(output_file, img_path)
    # pqdm([{"output_file": os.path.join(bg_folder_path, file), "file_image": os.path.join(cmd, file)} for file in
    #       filenames], bg_extraction, n_jobs=20,argument_type='kwargs')
    cmd = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\enhanced-image\image_augmentation\image_augmentation\texture"
    filenames = [f for f in os.listdir(cmd) if f.startswith("Adobe")]
    for file in tqdm(filenames):
        img_path = os.path.join(cmd, file)
        file_name = os.path.splitext(file)[0]
        img_path_output = os.path.join('./texture/test', file)
        image = cv2.imread(img_path)
        image = crop_watermark(image)
        cv2.imwrite(img_path_output, image)


