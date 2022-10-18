import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
from io import StringIO
import re
import base64
import numpy as np
from io import BytesIO
import json

img = cv2.imread('Bidv\\0.jpg')

res =  pytesseract.image_to_string(img,lang='vie')
print(res)

TRANS_COU = 0

trans = {
        'số tiền' : '',
        'nguồn tiền' :'',
        'tổng phí':'',
        'tên ví momo':'',
        'tên danh bạ':'',
        'số điện thoại':'',
        'mã giao dịch':'',
        'thời gian thanh toán':''
    }
res =  pytesseract.image_to_string(img,lang='vie')
print(res.split())