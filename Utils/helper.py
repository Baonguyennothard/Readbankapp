import numpy as np
import cv2
from PIL import Image, ImageOps
import base64
from io import BytesIO


def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
def getbankname(model,cv2image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    im_pil = Image.fromarray(cv2image)
    size = (224, 224)
    image = ImageOps.fit(im_pil, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    return model.predict(data)