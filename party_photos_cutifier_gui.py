import cv2
import os
import sys
import base64
import numpy
import easygui

from utils import replace_drinks


def block_print(verbose):
    if not verbose:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')


def enable_print(verbose):
    if not verbose:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def get_beer_detector(verbose):
    block_print(verbose)
    from beer_learning.detector import BeerDetector
    beer_detector = BeerDetector()
    enable_print(verbose)
    return beer_detector


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
        detector = get_beer_detector(verbose)

        if (len(sys.argv) == 2 and (sys.argv[1] == "--batch" or sys.argv[1] == "-b")) \
            or (len(sys.argv) == 3 and (sys.argv[2] == "--batch" or sys.argv[2] == "-b")):
            print("Processing the input folder...")
            for filename in [x for x in os.listdir("input") if (x.endswith(".jpg") or x.endswith(".png"))]:
                file_path = "input" + os.path.sep + filename
                input_img = cv2.imread(file_path)
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
