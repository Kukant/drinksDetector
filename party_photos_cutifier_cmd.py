import cv2
import os
import argparse

from beer_learning.detector import BeerDetector
from utils import replace_drinks


def get_input_folder():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('input_folder', type=str, help='The directory to process.')
    args = parser.parse_args()
    return args.input_folder


if __name__ == "__main__":
    input_folder = get_input_folder()
    detector = BeerDetector()
    print("Processing the input folder...")
    # for each .png file
    for filename in [x for x in os.listdir(input_folder) if (x.endswith(".jpg") or x.endswith(".png"))]:
        file_path = os.path.join(input_folder, filename)
        print("processing {}".format(file_path))
        input_img = cv2.imread(file_path)
        # find drinks in the photo
        detected_drinks = detector.get_beer_positions(input_img)
        # replace them with kittens
        replaced = replace_drinks(detected_drinks, input_img)
        cv2.imshow("output", replaced)
        cv2.waitKey(0)
