import cv2
import numpy as np

import json
from scipy.ndimage import gaussian_filter, map_coordinates
import os
from ur_material.modules import perspective_transform,warp_texture_blur_sticker,rotate
from ur_material.modules import bg_extraction
from pqdm.processes import pqdm


def crop_contour(contour, image):
    x, y, w, h = cv2.boundingRect(contour)
    blank_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    cv2.fillPoly(blank_image, [contour], 255)
    blank_image[y:y+int(h/3), x:x+w] = 0
    contours, _ = cv2.findContours(blank_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    min_area = float('inf')
    min_contour = 0
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area < min_area:
            min_area = area
            min_contour = i
    return contours[min_contour]

# 定义颜色
def single_color_extraction(image_path, file_name, det_type, label, json_output_file, from_path):
    colors_mapp_else = {
        "option": {"color": [0,255,0]},
        "blank": {"color": [0, 255, 255]},
        "formula": {"color": [255, 0, 255]},
        "underline": {"color": [153,50,204]},
        "waveline": {"color": [0, 100, 0]},
        "key": {"color": [0, 0, 255]},
        "snumber": {"color": [75, 0, 130]},
        "number": {"color": [128, 128, 0]},
        "drawing": {"color": [160, 198, 255]},
        "table": {"color": [221, 160, 221]},
        "ssnumber": {"color": [173, 216, 230]},
        "legend": {"color": [128, 0, 0]}
    }
    #        "legend": {"color": [211, 211, 211]},"bracket": {"color": [128, 128, 128]}, "test": {"color": [189, 183, 107]}, "fuwen": {"color": [186, 85, 211]},
    colors_mapp_line = {
            "line": {"color": [0,255,0]},
            "header": {"color": [0, 255, 255]},
            "footer": {"color": [255, 0, 255]},
            "heading": {"color": [0,139,139]},
    }
    colors_mapp_paragraph = {
            "paragraph_1": {"color": [205, 133, 63]},
            "paragraph_2": {"color": [221, 160, 221]},
    }
    if det_type == "else":
        rgb_color = colors_mapp_else[f"{label}"]["color"]
    if det_type == "line":
        rgb_color = colors_mapp_line[f"{label}"]["color"]
    if det_type == "paragraph":
        rgb_color = colors_mapp_paragraph[f"{label}"]["color"]

    # 将 RGB 颜色转换为 BGR 格式
    bgr_color = rgb_color[::-1]  # [0, 255, 0] -> [0, 255, 0]

    # 将 BGR 颜色转换为 HSV 颜色
    hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)

    # 提取 HSV 值
    hsv_value = hsv_color[0][0]
    # print(hsv_value[0])

    # 打印结果
    # print("HSV 颜色:", hsv_value)
    if from_path:
        image = cv2.imread(image_path)
    else:
        image = image_path
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blur = cv2.medianBlur(hsv ,11)
    threshold = 10
    # 把目标颜色的色块提取出来
    lower = np.array([hsv_value[0]-4 if hsv_value[0]-4 >= 0 else hsv_value[0],
                     hsv_value[1]-threshold if hsv_value[1]-threshold >= 0 else hsv_value[1],
                     hsv_value[2]-threshold if hsv_value[2]-threshold >= 0 else hsv_value[2]])
    # print(lower)
    upper = np.array([hsv_value[0]+4 if hsv_value[0]+4 <= 179 else hsv_value[0],
                     hsv_value[1]+threshold if hsv_value[1]+threshold <= 255 else hsv_value[1],
                     hsv_value[2]+threshold if hsv_value[2]+threshold <= 255 else hsv_value[2]])
    # print(upper)
    mask = cv2.inRange(blur, lower, upper)
    res = cv2.bitwise_and(image,image, mask= mask)
    result = np.hstack([image, res])
    # cv2.imwrite('res.png', result)

    # 找轮廓
    gray_res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    gray_res[gray_res == 255] = 0
    _, binary = cv2.threshold(gray_res, 20, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('./test_1.jpg', binary)
    # print(binary.shape)
    # cv2.imwrite('./enhanced-image/label_color/test_2.jpg', binary)

    # dilated = cv2.dilate(binary, np.ones((1,6), np.uint8), iterations=5)
    # dilated = cv2.erode(dilated, np.ones((1, 2), np.uint8), iterations=5)
    # filled_image = filled.fill(dilated)
    # cv2.imwrite('./test_3.jpg', filled_image)

    # cv2.imwrite('./enhanced-image/label_color/test_3.jpg', binary)
    # if label in ["number", "snumber", "table", "blank", "drawing"]:
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # elif label in ["drawing", "blank", "option", "key", "formula"]:
    # else:
    #     contours, _ = cv2.findContours(filled_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [contour for contour in contours if cv2.contourArea(contour)>400]
    # print(len(contours))
    # blank_image = np.zeros_like(gray_res)
    # cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 2)
    # for contour in contours:
    #     cv2.polylines(blank_image, [contour], True, (255, 255, 255), 2)
    # cv2.imwrite('./test_4.jpg', blank_image)

    # 转json格式
    if not os.path.exists(json_output_file):
        data = {"shapes":[]}
        data["imagePath"] = f"{file_name}.png"
        data["imageData"] = None
        data["version"] = "2.3.6"
        data["imageHeight"], data["imageWidth"], _ = image.shape
    else:
        with open(json_output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    for contour in contours:
        mask = {}
        points = []
        # contour = crop_contour(contour,image)
        for point in contour:
            x, y = point[0]
            points.append([int(x), int(y)])
        mask["points"] = points
        mask["label"] = label
        mask["shape_type"] = "polygon"
        # mask["area"] = cv2.contourArea(contour)
        data["shapes"].append(mask)
    with open(json_output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def color_extraction_method(image_path, file_name, det_type, json_output_file, from_path):
    colors_mapp_else = {
        "option": {"color": [0, 255, 0]},
        "blank": {"color": [0, 255, 255]},
        "formula": {"color": [255, 0, 255]},
        "underline": {"color": [153,50,204]},
        "waveline": {"color": [0, 100, 0]},
        "key": {"color": [0, 0, 255]},
        "snumber": {"color": [75, 0, 130]},
        "number": {"color": [128, 128, 0]},
        "drawing": {"color": [205, 133, 63]},
        "table": {"color": [221, 160, 221]},
        "ssnumber": {"color": [173, 216, 230]},
        "legend": {"color": [128, 0, 0]}
    }  #         "legend": {"color": [211, 211, 211]}, "bracket": {"color": [128, 128, 128]}
    colors_mapp_line = {
        "line": {"color": [255, 0, 255]},
        "header": {"color": [0, 255, 0]},
        "footer": {"color": [0, 255, 255]},
        "heading": {"color": [127, 127, 127]},
    }
    colors_mapp_paragraph = {
        "paragraph_1": {"color": [127, 0, 0]},
        "paragraph_2": {"color": [0, 0, 255]},
    }
    if det_type == "else":
        rgb_colors = colors_mapp_else
    if det_type == "line":
        rgb_colors = colors_mapp_line
    if det_type == "paragraph":
        rgb_colors = colors_mapp_paragraph
    for label in rgb_colors:
        # if label in ["option", "blank"]:
        single_color_extraction(image_path, file_name, det_type, label, json_output_file, from_path)
    # print("颜色提取完成")


def warp_mask(json_file, json_file_warped, file_name, shape_change, warp, crop_amount=None, is_rotated=False, is_s_image=False,random_seed=42, save=True,from_path=True):
    if from_path:
        with open(json_file, "r", encoding="utf-8") as f:
            data_ori = json.load(f)
    else:data_ori = json_file
    contours_warped = []
    # mask = data["shapes"][i]
    # print(f"file name: {json_file}")
    for mask in data_ori["shapes"]:
        blank_image = np.ones((data_ori["imageHeight"], data_ori["imageWidth"]), np.uint8) * 255
        # cv2.polylines(blank_image, np.array([mask['points']], dtype=np.int_), True, (255, 255, 255), 2)
        cv2.fillPoly(blank_image, [np.array([mask['points']], dtype=np.int_).reshape((-1, 1, 2))], (0, 0, 0))
        # cv2.imwrite('./test_5.jpg', blank_image)
        if shape_change:
            if is_s_image:
                blank_image = perspective_transform.main_gentle(blank_image, '', False, random_seed=random_seed)
            else:
                blank_image = perspective_transform.main(blank_image,'',False,random_seed=random_seed)
        if warp:
            blank_image = warp_texture_blur_sticker.elastic_transform(blank_image,'', random_seed=random_seed, crop_by_amount=True, crop_amount=crop_amount)
        if is_rotated:
            blank_image = rotate.rotate_method(blank_image,'',False,random_seed=random_seed)
        blank_image = cv2.bitwise_not(blank_image)
        # cv2.imwrite(f'./1/{file_name}.jpg', perspective_transform.main(cv2.imread(image_path)))
        # cv2.imwrite('./test_5.jpg', blank_image)
        contours, _ = cv2.findContours(blank_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [contour for contour in contours if cv2.contourArea(contour) > 100]
        # print(len(contours))
        min_area = float('inf')
        min_contour = 0

        # 遍历所有轮廓，找出面积最小的轮廓
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < min_area:
                min_area = area
                min_contour = i
        mask_warped = {}
        mask_warped["contours"] = contours[min_contour]
        mask_warped["label"] = mask["label"]
        contours_warped.append(mask_warped)

    data = {"shapes":[]}
    data["imagePath"] = f"{file_name}.png"
    data["imageData"] = None
    data["version"] = "2.3.6"
    data["imageHeight"] = data_ori["imageHeight"]
    data["imageWidth"] = data_ori["imageWidth"]
    for mask_warped in contours_warped:
        mask = {}
        points = []
        for point in mask_warped["contours"]:
            x, y = point[0]
            points.append([int(x), int(y)])
        mask["points"] = points
        mask["label"] = mask_warped["label"]
        mask["shape_type"] = "polygon"
        data["shapes"].append(mask)
    # data["shapes"] = sorted(data["shapes"], key=lambda x: x["index"])
    if save:
        with open(json_file_warped, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    return data




if __name__ == "__main__":

    # file_name = "test"
    # image_path = f'./{file_name}.png'
    # json_output_file = f'./{file_name}.json'
    # file_name = "else_15726443(1)_03"
    # image_path = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\paper\image\else_15726443(1)\else_15726443(1)_03.png"
    # json_output_file = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\paper\image\else_15726443(1)\else_15726443(1)_03.json"
    # json_file_warped = r"D:\desktop\intern\hexin\ultralytics-main\ultralytics-main\datasets\paper\image\else_15726443(1)\warped\else_15726443(1)_03.json"
    # color_extraction(image_path, file_name, "else", json_output_file, True)
    # single_color_extraction(image_path, "else_15726443(1)_02", "else",'snumber', json_output_file, True)
    # warp_mask(json_output_file, json_file_warped, file_name, True, True, 42)

    folder_path = r"D:\Downloads\result(2)\image"
    filenames = [f for f in os.listdir(folder_path)]
    for file in filenames:
        if 'new' in file:
            file_name = os.path.splitext(file)[0]
            image_path = os.path.join(folder_path, file)
            json_output_file = os.path.join(folder_path, f"{file_name}.json")
            single_color_extraction(image_path, file_name, "else",'drawing', json_output_file, True)
            with open(json_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["shapes"].reverse()
            with open(json_output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)