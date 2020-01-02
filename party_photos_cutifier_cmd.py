import cv2
import os
import argparse

from utils import replace_drinks, get_beer_detector

parser = argparse.ArgumentParser(description='Change ugly photos of beer into cute photos of kittens!')
parser.add_argument('input_folder', type=str, help='The directory to process.')
parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')


if __name__ == "__main__":
    args = parser.parse_args()
    input_folder = args.input_folder
    verbose = args.verbose
    if not verbose:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    print("Loading model...")
    detector = get_beer_detector(verbose)

    print("Processing the input folder...")
    # for each .png file
    for filename in [x for x in os.listdir(input_folder) if (x.endswith(".jpg") or x.endswith(".png"))]:
        file_path = os.path.join(input_folder, filename)
        print("Processing {}...".format(file_path))
        input_img = cv2.imread(file_path)
        # find drinks in the photo
        detected_drinks = detector.get_beer_positions(input_img)
        # replace them with kittens
        replaced = replace_drinks(detected_drinks, input_img)
        cv2.imshow("output", replaced)
        cv2.waitKey(0)
