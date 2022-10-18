import cv2
from numpy import double
import pytesseract
import re
from pytesseract import Output

img = cv2.imread('Dataset\Vietcombank\\8.jpg')

d = pytesseract.image_to_data(img, output_type=Output.DICT)
print(d.keys())
n_boxes = len(d['text'])
for i in range(n_boxes):
    if double(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x> img.shape[1]*0.5  and d['top'][i]> img.shape[0] *0.2 and re.findall('[0-9]{2}:[0-9]{2}',d['text'][i]) :
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) 
cv2.imwrite('res.png',img)
