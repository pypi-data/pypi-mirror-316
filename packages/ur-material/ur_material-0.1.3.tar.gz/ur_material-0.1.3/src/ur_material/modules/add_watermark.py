import cv2
import numpy as np
import os
import random

from ur_material.modules import overlap_final

def add_water_mark(image,  file_name=None, save=False, random_seed=42):

    random.seed(random_seed)

    water_mark_folder = f"{os.path.dirname(__file__)}/../../watermarks"
    water_marks = [f"{water_mark_folder}/{f}" for f in os.listdir(water_mark_folder) if f.endswith(".png")]
    water_mark = cv2.imread(random.choice(water_marks))
    # print(random.choice(water_marks))
    content = image
    content_height, content_width = content.shape[:2]
    cropped_watermark = water_mark[:content_height, :content_width]

    # result = overlap_final.overlap(cropped_watermark, content)
    result = overlap_final.overlap(cropped_watermark, content)
    if save:
        cv2.imwrite(f"./test/{file_name}_watermark.jpg", result)

    return result
