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



model = models.load_model("models/model6.h5", backbone_name='resnet50')
model = models.convert_model(model)

for filename in [x for x in os.listdir("validation") if x.endswith(".jpg")]:
    file_path = os.path.join("validation", filename)
    print("processing ", file_path)
    image = cv2.imread(file_path)
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # Process image
    start = time.time()
    boxes, probs, bla = model.predict_on_batch(np.expand_dims(image, axis=0))

    image = cv2.imread(file_path)
    trans = [x for x in probs[0]]
    boxes /= scale
    boxes = [x for x in boxes[0]]

    for i, prob in enumerate(trans):
        if prob < 0.42:
            continue

        d = boxes[i]
        image = cv2.rectangle(image, (d[0], d[1]), (d[2], d[3]), (0, 255, 0), 2)

    cv2.imshow('image', image)
    cv2.waitKey(0)
# print(boxes)
# print(scores)
# print("Processing time: ", time.time() - start)



