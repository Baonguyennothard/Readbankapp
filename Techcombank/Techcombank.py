from cv2 import split
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
from io import StringIO
import re
# from flask import Flask
# from flask import request
# from flask import jsonify
import base64
import numpy as np
from io import BytesIO
import json

img = cv2.imread('Techcombank\Techcombank\z3527566897248_7a2b590a536472fd6e99064bd0431e87.jpg')
h, w, c = img.shape
img = img[0:h,0:round(w*0.85)]
trans = {
    'accnum' : '',
    'money' :'',
    'time':'',
    'remainder':'',
    'transcontent':''
}
res = pytesseract.image_to_string(img,lang='vie')
listtext = []
if len(re.findall('\d{14}',res))>0 :
    listtext = res.split(re.findall('\d{14}',res)[0])
    for i in range(1,len(listtext)):
        transcontent=listtext[i]
        trans['accnum']=re.findall('\d{14}',res)[0].strip()
        money = re.findall('(?<=D:)(.*)',listtext[i])
        if len(money)>0:
            trans['money']=money[0].strip()
        else:
            if len( re.findall('-\S+',listtext[i]))>0:
                trans['money']=re.findall('-\S+',listtext[i])[0].strip()
            else:
                if  len(re.findall('+\S+',listtext[i]))>0:
                    trans['money']=re.findall('+\S+',listtext[i])[0].strip()
        remainder = re.findall('(?<=u:)(.*)',listtext[i])
        if len(remainder)>0:
            trans['remainder']=remainder[0].strip()
            transcontent = transcontent.split(trans['remainder'])[1]
        # time = re.findall('(?<=\n)(.*, )[0-9]{4}',listtext[i])
        # if len(time)>0:
        #     trans['time']=time[0].strip()
        #     transcontent = transcontent.split(trans['time'])[0].strip()
        if transcontent!=listtext[i]:
            trans['transcontent']=transcontent.replace("\n", " ")
        print(trans)
        
    



# boxes = pytesseract.image_to_boxes(img) 
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)
