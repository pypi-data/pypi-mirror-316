import cv2
import numpy as np
import random

def main(image,  file_name=None, save=False, crazy=False, random_seed=42):

    random.seed(random_seed)

    if len(image.shape) != 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 获取图像尺寸
    h, w = image.shape[:2]

    # 原始图像中的点坐标（选择图像的四个角）
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    # 从右往左拍，左小右大
    # 模拟倾斜拍摄效果，左侧的点向外扩展，右侧的点向内移动
    pts2 = np.float32([[0,0], [w * 0.95, h * 0.05], [0, h], [w * 0.92, h * 0.95]])
    # 计算透视变换矩阵
    matrix_right2left = cv2.getPerspectiveTransform(pts1, pts2)

    # 从右下往左上拍，右下大左上小
    pts3 = np.float32([[w * 0.05,h * 0.02], [w * 0.92, 0], [w * 0.08, h * 0.97], [w * 0.92, h]])
    matrix_btmright2topleft = cv2.getPerspectiveTransform(pts1, pts3)

    # 从左下往右上拍，左下大右上小
    pts4 = np.float32([[w * 0.08, 0], [w * 0.92, h * 0.05], [0, h], [w * 0.95, h * 0.92]])
    matrix_btmleft2topright = cv2.getPerspectiveTransform(pts1, pts4)

    # 从左往右拍， 左大右小
    pts5 = np.float32([[0,0], [w, h * 0.05], [0, h], [w, h * 0.95]])
    matrix_left2right = cv2.getPerspectiveTransform(pts1, pts5)

    # 从上往下拍，上大下小
    pts6 = np.float32([[0, 0], [w, 0], [w * 0.05, h], [w * 0.92, h]])
    matrix_top2bottom = cv2.getPerspectiveTransform(pts1, pts6)

    # 从下往上拍，下大上小
    pts7 = np.float32([[w * 0.08, 0], [w * 0.92, 0], [0, h], [w, h]])
    matrix_bottom2top = cv2.getPerspectiveTransform(pts1, pts7)

    matrixes = [matrix_right2left, matrix_btmright2topleft, matrix_btmleft2topright, matrix_left2right, matrix_top2bottom, matrix_bottom2top]

    matrix = random.choice(matrixes)

    # 应用透视变换
    tilted = cv2.warpPerspective(image, matrix, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    if save:
        cv2.imwrite(f"./test/{file_name}_perspective.jpg", tilted)

    return tilted

def main_mad(image,  file_name=None, save=False, random_seed=42):

    random.seed(random_seed)

    if len(image.shape) != 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 获取图像尺寸
    h, w = image.shape[:2]

    # 原始图像中的点坐标（选择图像的四个角）
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

   # crazy mode
    # 从右往左拍，左小右大
    # 模拟倾斜拍摄效果，左侧的点向外扩展，右侧的点向内移动
    pts8 = np.float32([[0,0], [w * 0.9, h * 0.08], [0, h], [w * 0.9, h * 0.92]])
    # 计算透视变换矩阵
    matrix_right2left_crazy = cv2.getPerspectiveTransform(pts1, pts8)

    # 从右下往左上拍，右下大左上小
    pts9 = np.float32([[w * 0.1,h * 0.07], [w * 0.98, 0], [w * 0.12, h * 0.92], [w * 0.95, h]])
    matrix_btmright2topleft_crazy = cv2.getPerspectiveTransform(pts1, pts9)

    # 从左下往右上拍，左下大右上小
    pts10 = np.float32([[w * 0.1, 0], [w * 0.9, h * 0.1], [0, h], [w * 0.95, h * 0.9]])
    matrix_btmleft2topright_crazy = cv2.getPerspectiveTransform(pts1, pts10)

    # 从左往右拍， 左大右小
    pts11 = np.float32([[0,0], [w, h * 0.1], [0, h], [w, h * 0.9]])
    matrix_left2rightz_crazy = cv2.getPerspectiveTransform(pts1, pts11)

    # 从上往下拍，上大下小
    pts12 = np.float32([[0, 0], [w, 0], [w * 0.15, h], [w * 0.88, h]])
    matrix_top2bottom_crazy = cv2.getPerspectiveTransform(pts1, pts12)

    # 从下往上拍，下大上小
    pts13 = np.float32([[w * 0.08, 0], [w * 0.93, 0], [0, h], [w, h]])
    matrix_bottom2top_crazy = cv2.getPerspectiveTransform(pts1, pts13)

    matrixes = [matrix_right2left_crazy, matrix_btmright2topleft_crazy, matrix_btmleft2topright_crazy, matrix_left2rightz_crazy, matrix_top2bottom_crazy, matrix_bottom2top_crazy]

    matrix = random.choice(matrixes)

    # 应用透视变换
    tilted = cv2.warpPerspective(image, matrix, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    if save:
        cv2.imwrite(f"./test/{file_name}_perspective.jpg", tilted)

    return tilted

def main_gentle(image,  file_name=None, save=False, random_seed=42):

    # print(f'main gentle seed: {random_seed}')

    random.seed(random_seed)

    if len(image.shape) != 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 获取图像尺寸
    h, w = image.shape[:2]

    # 原始图像中的点坐标（选择图像的四个角）
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    # 从右往左拍，左小右大
    # 模拟倾斜拍摄效果，左侧的点向外扩展，右侧的点向内移动
    pts2 = np.float32([[0,0], [w * 0.98, h * 0.03], [0, h], [w * 0.95, h * 0.98]])
    # 计算透视变换矩阵
    matrix_right2left = cv2.getPerspectiveTransform(pts1, pts2)

    # 从右下往左上拍，右下大左上小
    pts3 = np.float32([[w * 0.03,h * 0.02], [w * 0.95, 0], [w * 0.03, h * 0.97], [w * 0.95, h]])
    matrix_btmright2topleft = cv2.getPerspectiveTransform(pts1, pts3)

    # 从左下往右上拍，左下大右上小
    pts4 = np.float32([[w * 0.03, 0], [w * 0.95, h * 0.03], [0, h], [w * 0.96, h * 0.95]])
    matrix_btmleft2topright = cv2.getPerspectiveTransform(pts1, pts4)

    # 从左往右拍， 左大右小
    pts5 = np.float32([[0,0], [w, h * 0.03], [0, h], [w, h * 0.97]])
    matrix_left2right = cv2.getPerspectiveTransform(pts1, pts5)

    # 从上往下拍，上大下小
    pts6 = np.float32([[0, 0], [w, 0], [w * 0.02, h], [w * 0.97, h]])
    matrix_top2bottom = cv2.getPerspectiveTransform(pts1, pts6)

    # 从下往上拍，下大上小
    pts7 = np.float32([[w * 0.04, 0], [w * 0.96, 0], [0, h], [w, h]])
    matrix_bottom2top = cv2.getPerspectiveTransform(pts1, pts7)

    matrixes = [matrix_right2left, matrix_btmright2topleft, matrix_btmleft2topright, matrix_left2right, matrix_top2bottom, matrix_bottom2top]

    matrix = random.choice(matrixes)

    # 应用透视变换
    tilted = cv2.warpPerspective(image, matrix, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    if save:
        cv2.imwrite(f"./test/{file_name}_perspective.jpg", tilted)

    return tilted

if __name__=="__main__":
    image = cv2.imread("./texture_yellow/texture_42.png", cv2.IMREAD_UNCHANGED)
    image = main_gentle(image)
    cv2.imshow("result", image)
    cv2.waitKey(0)