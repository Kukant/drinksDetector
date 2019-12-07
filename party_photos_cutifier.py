import cv2
import os
from math import fabs

kittens = []


def load_kittens(folder="kittens"):
    for filename in os.listdir(folder):
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


def replace_drinks(detected_drinks, input_img):
    for x1, y1, x2, y2 in detected_drinks:
        size_x = x2 - x1
        size_y = y2 - y1

        kitten = load_best_fitting_kitten(size_x, size_y)

        alpha_s = kitten[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            input_img[y1:y2, x1:x2, c] = (alpha_s * kitten[:, :, c] + alpha_l * input_img[y1:y2, x1:x2, c])

    return input_img


if __name__ == "__main__":
    load_kittens()
    input_img = cv2.imread("matej.jpg")
    kittens_folder = "kittens"
    # compute this using the NN
    detected_drinks = [
        # (x1, y1, x2, y2)
        (100, 100, 1000, 1000),
        (500, 100, 1000, 300),
    ]

    replaced = replace_drinks(detected_drinks, input_img)
    cv2.imwrite("output.jpg", replaced)


