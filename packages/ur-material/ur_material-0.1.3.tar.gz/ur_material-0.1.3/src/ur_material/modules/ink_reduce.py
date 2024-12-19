import cv2
import numpy as np
import genalog.degradation.effect as effect
from genalog.degradation.degrader import Degrader

def salting_reduce(image, file_name=None, save=False):
    image = effect.salt(image, amount=0.1)
    return image

def dilate_erode_reduce(image, file_name=None, save=False):
    kernel = np.ones((2,2), np.uint8)

    image = cv2.erode(image, np.ones((3,3), np.uint8), iterations=1)

    image = cv2.dilate(image, kernel, iterations=1)

    return image

def ink_reduce_method(image, reduce_percentage, file_name=None, save=False, if_salt=True):

    if len(image.shape) != 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # percentage to imply how severe texts are reduced
    # less percentage, less reduced
    reduce_percentage = reduce_percentage

    mask = image < 255
    # 计算新的像素值
    image[mask] = (image[mask] + (255 - image[mask]) * reduce_percentage).astype(np.uint8)

    degradations = [
        ("salt", {"amount": 0.1}),
    ]
    # All of the referenced degradation effects are in submodule `genalog.degradation.effect`

    degrader = Degrader(degradations)
    if if_salt:
        image = degrader.apply_effects(image)

    if save:
        cv2.imwrite(f"./test/{file_name}_inkreduce.jpg", image)

    return image

# read from single file
if __name__ == "__main__":
    result = ink_reduce("s4.png", 1)
    cv2.imwrite("s4_reduce.png", result, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    cv2.imshow("result", result)
    cv2.waitKey(0)


