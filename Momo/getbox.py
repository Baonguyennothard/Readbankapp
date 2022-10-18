
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

img = cv2.imread('D:\Working\Octa\Readbankapp\Momo\datasets\h.jpg')
trans = {
    'money' :'',
    'time':'',
    'phonenumber':'',
    'transID':''
}
d = pytesseract.image_to_data(img, output_type=Output.DICT,lang='vie')
pattern1 = '-\S+'
pattern2 = '+\S+'
for i in range(len(d['text'])):
    try:
        if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > img.shape[1]/6 and np.double(d['top'][i]) < img.shape[0]/6 and np.double(d['left'][i]) < img.shape[1]/4 and re.match(pattern1, d['text'][i]) or  re.match(pattern2, d['text'][i]) :
            trans['money'] = d['text'][i]     
    except:
        continue                                                                                                                
pattern1 = '[0-9]{1,2}:[0-9]{1,2}'
pattern2 = '[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}'
for i in range(len(d['text'])):
    try:
        if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > img.shape[1]/2 and np.double(d['top'][i]) < img.shape[0]/2.5 and re.match(pattern1, d['text'][i])  : trans['time'] = str(d['text'][i]).replace('-','')
        if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > img.shape[1]/2 and np.double(d['top'][i]) < img.shape[0]/2.5 and re.match(pattern2, d['text'][i])  : trans['time'] +='-'+str(d['text'][i]).replace('-','')        
    except:
        continue   
pattern1 = '[0-9]{9,13}'
for i in range(len(d['text'])):
    try:
        if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > img.shape[1]/3 and np.double(d['top'][i]) < img.shape[0]/4 and re.match(pattern1, d['text'][i])  : 
            trans['transID'] = d['text'][i]    
    except:
        continue    
pattern1 = '[0-9]{9,12}'
for i in range(len(d['text'])):
    try:
        if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > img.shape[1]/2 and np.double(d['top'][i]) > img.shape[0]*0.6 and re.match(pattern1, d['text'][i])  : 
            trans['phonenumber'] = d['text'][i]    
    except:
        continue   
MOMO_LOCATE = []
for i in range(len(d['text'])):
    try:
        if np.double(d['conf'][i]) > 50 and re.search('MoMo', d['text'][i] ) and np.double(d['left'][i]) < img.shape[1]/2 and np.double(d['top'][i]) > img.shape[0]*0.6: 
            MOMO_LOCATE.append((d['left'][i], d['top'][i], d['width'][i], d['height'][i]))
    except:
        continue   
if len(MOMO_LOCATE)==1:
    (x,y,w,h) = MOMO_LOCATE[0]
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 50  and np.double(d['left'][i]) > img.shape[1]/2 and np.double(d['top'][i]) > y-10 and np.double(d['top'][i]) < y+10: 
                trans['wallet'] +=' '+ d['text'][i]      
                trans['wallet'].strip()
        except:
            continue  
                                                                                                     
print(trans)
cv2.imwrite('Momo\imgres.png', img)

