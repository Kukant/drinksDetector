import keras_resnet
from keras.models import load_model
import cv2
import numpy
from keras_retinanet.models import retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
import time
import numpy as np
import os


class BeerDetector:
    def __init__(self, model_path):
        model = models.load_model(model_path, backbone_name='resnet50')
        self.model = models.convert_model(model)

    def get_beer_positions(self, image):
        pimage = preprocess_image(image)
        pimage, scale = resize_image(pimage)

        boxes, probs, bla = self.model.predict_on_batch(np.expand_dims(pimage, axis=0))

        trans = [x for x in probs[0]]
        boxes /= scale
        boxes = [x for x in boxes[0]]

        ret = []
        for i, prob in enumerate(trans):
            if prob < 0.42:
                continue

            ret.append([int(x) for x in boxes[i]])
        return ret



