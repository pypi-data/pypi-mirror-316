import cv2
import numpy as np
import os

# USM Image Sharpening
def ImageSharp(src, nAmount=1000):
    sigma = 3  
    threshold = 1  
    amount = nAmount / 100.0  
    imgBlurred = cv2.GaussianBlur(src, ksize=(0, 0), sigmaX=sigma, sigmaY=sigma)
    lowContrastMask = np.abs(src - imgBlurred) < threshold
    dst = src * (1 + amount) - imgBlurred * amount
    dst = np.where(lowContrastMask, src, dst)
    return dst

def main(image, file_name=None, save=False):
    src = image
    src = src.astype(np.float32) / 255.0

    dst1 = src.copy()
    dst2 = src.copy()

    # Apply Gaussian Blur
    gauss = cv2.GaussianBlur(src, ksize=(101, 101), sigmaX=0)
    gauss[gauss == 0] = 1e-8  # Avoid division by zero
    dst1 = src / gauss

    # Apply Mean Blur
    gauss = cv2.blur(src, ksize=(101, 101))
    gauss[gauss == 0] = 1e-8  # Avoid division by zero
    dst2 = src / gauss

    # Apply Image Sharpening
    dst2 = ImageSharp(dst2, 101)

    dst2 = np.clip(dst2 * 255, 0, 255).astype(np.uint8)

    # dst2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2GRAY)
    
    ret, dst3 = cv2.threshold(dst2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return dst3

    # Display or save the result images as needed
    # cv2.imshow('Original Image', src)
    # cv2.waitKey(0)
    # cv2.imshow('Gaussian Division', dst1)
    # cv2.waitKey(0)
    # cv2.imshow('Mean Division with Sharpening', dst2)
    # cv2.waitKey(0)
    # cv2.imshow('Thresholded Gaussian Division', dst3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    # input_dir = "./enhanced_image"
    # output_dir = "./scanned_image"

    # for file_names in os.listdir(input_dir):
    #     image = cv2.imread(os.path.join(input_dir, file_names))
    #     result = main(image)
    #     cv2.imwrite(os.path.join(output_dir, file_names), result, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    #     cv2.imshow("result", result)
    #     cv2.waitKey(0)

    image = cv2.imread("../img_src/1011094525_f22f4e26-96a8-4059-842a-ba9fad98623c_aug_2.png")
    image = main(image)
    cv2.imshow("image", image)
    cv2.waitKey(0)