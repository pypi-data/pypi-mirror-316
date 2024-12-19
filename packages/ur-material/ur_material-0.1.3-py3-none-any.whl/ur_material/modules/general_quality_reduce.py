import cv2
import numpy as np
from augraphy import *

def blur(image, kernel_size, file_name=None, save=False):
    image = cv2.GaussianBlur(image, kernel_size, 0)
    return image

def dilate(image, kernel_size, file_name=None, save=False):
    kernel = np.ones((1,1), np.uint8)

    # image = cv2.erode(image, np.ones((2,2), np.uint8), iterations=2)

    lines_degradation = LinesDegradation(line_roi = (0.0, 0.0, 1.0, 1.0),
                                    line_gradient_range=(75, 255),
                                    line_gradient_direction= (2,2),
                                    line_split_probability=(0.2, 0.3),
                                    line_replacement_value=(255,255),
                                    line_min_length=(1, 1),
                                    line_long_to_short_ratio = (3,3),
                                    line_replacement_probability = (1.0, 1.0),
                                    line_replacement_thickness = (1, 1)
                                    )

    image = lines_degradation(image)

    image = cv2.dilate(image, kernel, iterations=2)

    inkbleed = InkBleed(intensity_range=(0.4, 0.6),
                    kernel_size=(1, 1),
                    severity=(0.2, 0.4)
                    )

    # image = inkbleed(image)

    # jpeg quality reduce
    # jpeg_5 = Jpeg(quality_range=(60, 70))
    # image = jpeg_5(image)
    
    return image

def reduce_by_size(image, file_name=None, save=False):
    if image.ndim > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    og_width = image.shape[1]
    og_height = image.shape[0]

    new_width = og_width // 2
    new_height = og_height // 2

    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

    return image

def reduce(image,reduce_range, kernel_size, file_name=None, save=False):
    # jpeg质量降低

    # inkbleed = InkBleed(intensity_range=(0.4, 0.7),
    #                 kernel_size=kernel_size,
    #                 severity=(0.2, 0.4)
    #                 )

    # image = inkbleed(image)

    # jpeg quality reduce
    jpeg_5 = Jpeg(quality_range=reduce_range)
    image = jpeg_5(image)
    image = jpeg_5(image)
    image = jpeg_5(image)
    
    return image

# def reduce(image,reduce_range, file_name=None, save=False):
#     # jpeg quality reduce
#     jpeg_5 = Jpeg(quality_range=reduce_range)
#     image = jpeg_5(image)
    
#     return image