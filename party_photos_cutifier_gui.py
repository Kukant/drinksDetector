import cv2
import os
import base64
import numpy
import easygui
import argparse

from utils import replace_drinks, get_beer_detector

parser = argparse.ArgumentParser(description='Change ugly photos of beer into cute photos of kittens!')
parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')


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
    args = parser.parse_args()
    verbose = args.verbose
    if not verbose:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    print("Loading model...")
    detector = get_beer_detector(verbose)
    input_img = read_image_interactive()
    if input_img is None:
        print("Bye...")
        exit()

    # compute this using the NN
    detected_drinks = detector.get_beer_positions(input_img)
    replaced = replace_drinks(detected_drinks, input_img)
    cv2.imshow("output", replaced)
    cv2.waitKey(0)
