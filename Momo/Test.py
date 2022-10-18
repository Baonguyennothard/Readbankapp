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


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


img = cv2.imread('GDPOS\\3.jpg')
# gray = get_grayscale(img)
# thresh = thresholding(gray)
res =  pytesseract.image_to_string(img,lang='eng')
sotien = re.findall('(?<= )(.*)(?=đ)',res)
if len(sotien)>0:
    trans['số tiền']=sotien[0].strip()
nguontien = re.findall('(?<=Nguồn tiền)(.*)',res)
if len(nguontien)>0:
     trans['nguồn tiền']= nguontien[0].strip()
tongphi = re.findall('(?<=phí )(.*)',res)
if len(tongphi)>0:
     trans['tổng phí']= tongphi[0].strip()
tenvi = re.findall('(?<=MoMo )(.*)',res)
if len(tenvi)>0:
     trans['tên ví momo']= tenvi[0].strip()
tendanhba = re.findall('(?<=bạ)(.*)',res)
if len(tendanhba)>0:
     trans['tên danh bạ']= tendanhba[0].strip()
sdt = re.findall('(?<=thoại)(.*)',res)
if len(sdt)>0:
     trans['số điện thoại']= sdt[0].strip()
mdd = re.findall('(?<=dịch:)(.*)',res)
if len(mdd)>0:
     trans['mã giao dịch']= mdd[0].strip()
time = re.findall('[0-9]{1,2}:[0-9]{1,2}',res)#
day = re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}',res)
if len(time)>0 and len(day)>0:
     trans['thời gian thanh toán']= time[0].strip()+'-'+day[0].strip()

print(trans)






