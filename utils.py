import cv2
import os
from math import fabs

kittens = []
kittens_folder = "kittens"


def load_kittens(folder="kittens"):
    for filename in [x for x in os.listdir(folder) if x.endswith(".png")]:
        kittens.append(cv2.imread(os.path.join(folder, filename), -1))

    if kittens.__len__() == 0:
        raise Exception("No kitten images found")


def load_best_fitting_kitten(size_x, size_y):
    ratio = size_x / size_y
    best_image = kittens[0]
    best_ratio_diff = fabs(ratio - kittens[0].shape[1] / kittens[0].shape[0])
    for img in kittens:
        ratio_diff = fabs(ratio - img.shape[1] / img.shape[0])
        if ratio_diff < best_ratio_diff:
            best_image = img
            best_ratio_diff = ratio_diff
    return cv2.resize(best_image, (size_x, size_y))


def widen_coordinates(coordinates, img, ratio=0.9):
    x1, y1, x2, y2 = coordinates
    diff_x = (x2 - x1) * ratio / 2
    diff_y = (y2 - y1) * ratio / 2
    height, width, channels = img.shape

    x1 = int(x1 - diff_x) if x1 - diff_x > 0 else 0
    y1 = int(y1 - diff_y) if y1 - diff_y > 0 else 0
    x2 = int(x2 + diff_x) if x2 + diff_x < width else width
    y2 = int(y2 + diff_y) if y2 + diff_y < height else height

    return x1, y1, x2, y2


def replace_drinks(detected_drinks, input_img):
    for coordinates in detected_drinks:
        x1, y1, x2, y2 = widen_coordinates(coordinates, input_img)
        size_x = x2 - x1
        size_y = y2 - y1

        kitten = load_best_fitting_kitten(size_x, size_y)

        alpha_s = kitten[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            input_img[y1:y2, x1:x2, c] = (alpha_s * kitten[:, :, c] + alpha_l * input_img[y1:y2, x1:x2, c])

    return input_img

def block_print(verbose):
    if not verbose:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')


def enable_print(verbose):
    if not verbose:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

load_kittens()


