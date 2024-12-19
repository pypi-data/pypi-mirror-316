import cv2
import time
import copy
import random
import numpy as np

def expand_image(image, border_color=(255, 255, 255)):
    og_width, og_height = image.shape[:2]

    border_size = (og_width + og_height) // 8

    image = cv2.copyMakeBorder(
        image,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=border_color
    )

    return image, og_width, og_height

# def crop_image(image, og_width, og_height):

#     # 如果输入不是灰度图，转换为灰度图
#     if image.ndim == 2:
#         gray = image
#     elif image.ndim == 3:
#         # 三通道图像，假设是RGB
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     else:
#         # 四通道图像，假设是RGBA
#         gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

#     # 二值化
#     # set thredhold to 200
#     _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

#     # 寻找轮廓
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # 初始化外接矩形的边界
#     min_x, min_y = binary.shape[1], binary.shape[0]
#     max_x = max_y = 0

#     # 计算包含所有轮廓的最小外接矩形
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         min_x = min(min_x, x)
#         min_y = min(min_y, y)
#         max_x = max(max_x, x + w)
#         max_y = max(max_y, y + h)

#     expand_x = abs(og_width - (max_x - min_x)) // 8
#     expand_y = abs(og_height - (max_y - min_y)) // 8

#     # print(f'expand x: {expand_x}, expand y: {expand_y}')

#     min_x = min_x - expand_x if min_x - expand_x >= 0 else 0
#     min_y = min_y - expand_y if min_y - expand_y >= 0 else 0
#     max_x = max_x + expand_x if max_x + expand_x <= binary.shape[1] else binary.shape[1]
#     max_y = max_y + expand_y if max_y + expand_y <= binary.shape[0] else binary.shape[0]

#     # 裁剪图片
#     cropped_image = image[min_y:max_y, min_x:max_x]

#     return cropped_image

def crop_image(image, og_width, og_height):
    # Convert image to grayscale if it's not already
    if image.ndim == 2:
        gray = image
    elif image.ndim == 3:
        # Assume RGB
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        # Assume RGBA
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # Binary thresholding
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize bounding rectangle borders
    min_x, min_y = binary.shape[1], binary.shape[0]
    max_x, max_y = 0, 0

    # Compute the minimum bounding rectangle containing all contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    expand_x = abs(og_width - (max_x - min_x)) // 8
    expand_y = abs(og_height - (max_y - min_y)) // 8

    # Adjust min and max coordinates with expansion, ensuring they are within image bounds
    min_x_expanded = max(min_x - expand_x, 0)
    min_y_expanded = max(min_y - expand_y, 0)
    max_x_expanded = min(max_x + expand_x, binary.shape[1])
    max_y_expanded = min(max_y + expand_y, binary.shape[0])

    # Calculate the amount cropped from each side
    cropped_left = min_x_expanded
    cropped_right = binary.shape[1] - max_x_expanded
    cropped_top = min_y_expanded
    cropped_bottom = binary.shape[0] - max_y_expanded

    # Crop image
    cropped_image = image[min_y_expanded:max_y_expanded, min_x_expanded:max_x_expanded]

    # Create a dictionary with the amounts cropped
    cropped_amounts = {
        'left': cropped_left,
        'right': cropped_right,
        'top': cropped_top,
        'bottom': cropped_bottom
    }

    return cropped_image, cropped_amounts

def crop_image_by_amounts(image, crop_amounts):
    # Extract crop amounts
    cropped_left = crop_amounts.get('left', 0)
    cropped_right = crop_amounts.get('right', 0)
    cropped_top = crop_amounts.get('top', 0)
    cropped_bottom = crop_amounts.get('bottom', 0)
    
    # Ensure crop amounts are within image dimensions
    height, width = image.shape[:2]
    new_left = max(cropped_left, 0)
    new_right = width - max(cropped_right, 0)
    new_top = max(cropped_top, 0)
    new_bottom = height - max(cropped_bottom, 0)
    
    # Validate that the new coordinates are within the image bounds
    new_left = min(new_left, width)
    new_right = max(new_right, new_left)
    new_top = min(new_top, height)
    new_bottom = max(new_bottom, new_top)
    
    # Crop the image
    cropped_image = image[new_top:new_bottom, new_left:new_right]
    
    return cropped_image


def deform(img, perturbed_mesh):
    h, w = img.shape[:2]
    perturbed_mesh_x = perturbed_mesh[:,0]
    perturbed_mesh_y = perturbed_mesh[:,1]

    perturbed_mesh_x = perturbed_mesh_x.reshape((h,w))
    perturbed_mesh_y = perturbed_mesh_y.reshape((h,w))
    # img = img + 1 # 保护下不是 0 的部分
    remapped = cv2.remap(img, perturbed_mesh_x, perturbed_mesh_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    # remapped[remapped <= 20] = 255
    return remapped


def get_perturbed_mesh(img, alpha_range=100, movement=100, min_movement=15,  curve_type="style_01", random_seed=42):
    """ Author: papabiceps
        https://stackoverflow.com/q/53907633
    """
    # print("get pertubed mesh seed: ", random_seed)

    random.seed(random_seed)
    np.random.seed(random_seed)

    # mesh row & col
    mr, mc = img.shape[:2]
    xx = np.arange(0, mr, 1)
    yy = np.arange(mc-1, -1, -1)

    # yy = np.arange(0, mc, 1)
    [Y, X] = np.meshgrid(xx, yy)
    ms = np.transpose(np.asarray([X.flatten('F'), Y.flatten('F')]), (1,0))

    perturbed_mesh = ms
    nv = np.random.randint(50) - 1

    for k in range(nv):
        # Choosing one vertex randomly
        vidx = np.random.randint(np.shape(ms)[0])
        vtex = ms[vidx, :]
        #Vector between all vertices and the selected one
        xv = perturbed_mesh - vtex
        # Random movement
        mv = (np.random.rand(1,2) - 0.5) * movement
        # mv = np.clip(mv, -movement / 2, movement / 2)
        if np.linalg.norm(mv) < min_movement:
            mv = mv / np.linalg.norm(mv) * min_movement
        hxv = np.zeros((np.shape(xv)[0], np.shape(xv)[1] +1) )
        hxv[:, :-1] = xv
        hmv = np.tile(np.append(mv, 0), (np.shape(xv)[0],1))
        d = np.cross(hxv, hmv)
        d = np.absolute(d[:, 2])
        d = d / (np.linalg.norm(mv, ord=2))
        wt = d

        if curve_type == "style_01":
            alpha = np.random.rand(1) * alpha_range + alpha_range
            wt = alpha / (wt + alpha)
        else:
            alpha = np.random.rand(1) + 1
            wt = 1 - (wt / 100 )**alpha

        msmv = mv * np.expand_dims(wt, axis=1)
        perturbed_mesh = perturbed_mesh + msmv
        perturbed_mesh = perturbed_mesh.astype(np.float32)
        if perturbed_mesh is not None:
            result = deform(img, perturbed_mesh)
            flipped = cv2.flip(result,1)
            return flipped


def process(image,alpha_range=None, movement=None, alpha=None, sigma=None, alpha_affine=None, random_seed=42, save=False, crop_by_amount=False, crop_amount=None):
    """ 仿射弹性变换函数
    """
    # print("crop amount: ", crop_amount)
    # print("ela process seed: ", random_seed)
    og_width, og_height = image.shape[:2]
    # expand white boarder for better deformation
    image, og_width, og_height = expand_image(image)

    # cv2.imshow("expanded", image)
    # cv2.waitKey(0)

    random.seed(random_seed)
    np.random.seed(random_seed)
    
    random_state = np.random.RandomState(random_seed)
    if alpha is None:
        alpha = image.shape[1] * 4
    if sigma is None:
        sigma = image.shape[0] * 0.08
    if alpha_affine is None:
        alpha_affine = 10
    
    shape = image.shape
    shape_size = shape[:2]
    
    # Random affine
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([center_square + square_size,
                       [center_square[0] + square_size, center_square[1] - square_size],
                       center_square - square_size])
    pts2 = pts1 + random_state.uniform(-alpha_affine, alpha_affine, size=pts1.shape).astype(np.float32)
    
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, shape_size[::-1], borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    # cv2.imwrite(f"../test/sss_{o}_ori.jpg", image)
    # 更精细的扭曲和处理
    update_alpha_movement_value = (og_height + og_width) // 10
    flip_image = None
    flip_image = get_perturbed_mesh(image, alpha_range=update_alpha_movement_value, movement=update_alpha_movement_value, curve_type="style_01", random_seed=random_seed)
    # image = get_perturbed_mesh(image, alpha_range=update_alpha_movement_value, movement=update_alpha_movement_value, curve_type="style_01", random_seed=random_seed)

    # crop image back to original size
    if flip_image is not None and not crop_by_amount:
        image, crop_amount = crop_image(flip_image, og_width, og_height)
    elif flip_image is not None and crop_by_amount:
        image = crop_image_by_amounts(flip_image, crop_amount)
    elif flip_image is None and not crop_by_amount:
        image, crop_amount = crop_image(image, og_width, og_height)
    else:
        image = crop_image_by_amounts(image, crop_amount)

    # cv2.imshow("cropped", image)
    # cv2.waitKey(0)

    if not crop_by_amount: 
        return image, crop_amount
    else:
        return image


if __name__ == "__main__":
    image = cv2.imread("../test/clean_15726443_01.png")
    # image = cv2.imread("../test/20241009-114939.jpg")
    for o in range(10):
        ts = time.time()
        random_seed = random.randint(0, 2 ** 32 - 1)
        image_res = process(copy.copy(image), 
                            alpha=image.shape[1] * 4, sigma=image.shape[0] * 0.08, 
                            alpha_affine=10, random_seed=random_seed, save=False)
        if image_res is not None:
            cv2.imwrite(f"../test/sss_{o}.jpg", image_res)
        print(time.time() - ts)