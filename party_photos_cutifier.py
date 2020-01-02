import cv2
import os
import sys
import base64
import numpy
import easygui
from math import fabs


def block_print(verbose):
    if not verbose:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')


def enable_print(verbose):
    if not verbose:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def import_beer_detector(verbose):
    block_print(verbose)
    from beer_learning.detector import BeerDetector
    __detector = BeerDetector("beer_learning" + os.path.sep + "models" + os.path.sep + "resnet-model_latest.h5")
    enable_print(verbose)
    return __detector


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


def read_image_interactive():
    # Using GUI as standard input() can't handle large strings
    uri = easygui.enterbox("Paste raw image there:")
    if not uri:
        return None

    if len(uri.split(',')) > 1:
        uri = uri.split(',')[1]

    data = bytearray(uri, 'ascii')
    nparr = numpy.fromstring(base64.b64decode(data), numpy.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


if __name__ == "__main__":
    verbose = len(sys.argv) > 1 and (sys.argv[1] == "--verbose" or sys.argv[1] == "-v")
    if not verbose:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("Party Photos Cutifier")
        print("Change ugly photos of beer into cute photos of kittens!")
        print("Usage:")
        print("\t-v, --verbose: Verbose output.")
        print("\t-b, --batch: Process content of the input folder.")
        print("\t-h, --help: Display this manual.")
        print("\t<otherwise>: Interactive mode. Opens drag&drop window for user-supplied input photo.")

    else:
        kittens = []
        load_kittens()
        kittens_folder = "kittens"
        print("Loading the model...")
        detector = import_beer_detector(verbose)

        if (len(sys.argv) == 2 and (sys.argv[1] == "--batch" or sys.argv[1] == "-b")) \
        or (len(sys.argv) == 3 and (sys.argv[2] == "--batch" or sys.argv[2] == "-b")):
            print("Processing the input folder...")
            for filename in [x for x in os.listdir("input") if (x.endswith(".jpg") or x.endswith(".png"))]:
                file_path = "input" + os.path.sep + filename
                input_img = cv2.imread(file_path)
                # compute this using the NN
                detected_drinks = detector.get_beer_positions(input_img)
                replaced = replace_drinks(detected_drinks, input_img)
                cv2.imshow("output", replaced)
                cv2.waitKey(0)

        else:
            if len(sys.argv) > 1:
                print("Defaulting to the interactive mode as no valid arguments were passed. Try -h for more info...")

            input_img = read_image_interactive()
            if input_img is None:
                print("bye...")
                exit()

            # compute this using the NN
            detected_drinks = detector.get_beer_positions(input_img)
            replaced = replace_drinks(detected_drinks, input_img)
            cv2.imshow("output", replaced)
            cv2.waitKey(0)
