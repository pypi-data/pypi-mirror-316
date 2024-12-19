from ur_material.small.image_enhance_small import *

def ink_on_paper(image):
    return image_augmentation_2(image)

def ink_on_paper_light(image):
    return image_augmentation_11(image)

def ink_bleed(image):
    return image_augmentation_18(image)

def low_quality(image):
    return image_augmentation_12(image)

def erosed_light(image):
    return image_augmentation_13(image)

def erosed_heavy(image):
    return image_augmentation_17(image)

def low_quality_on_paper(image):
    return image_augmentation_16(image)

def noised(image):
    return image_augmentation_15(image)

def cutted(image):
    return image_augmentation_14(image)

def erosed_cutted(image):
    return image_augmentation_7(image)
