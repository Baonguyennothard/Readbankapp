from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
from io import StringIO
import re
import base64
from io import BytesIO
import json
from sqlalchemy import null
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
#Định nghĩa
model = load_model('keras_model.h5')
BANK_LIST =['VIETCOM'
            ,'TECH'
            ,'BIDV'
            ,'MOMO'
            ,'MB'
            ]

#****************************************CLASSIFY*********************************
def getbankname(cv2image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    im_pil = Image.fromarray(cv2image)
    size = (224, 224)
    image = ImageOps.fit(im_pil, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    return model.predict(data)
def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)   
#****************************************VIETCOM**********************************
def getresVIETCOM(img):
    listtrans=[]
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    LIST_LOCAT = []
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if  x> img.shape[1]*0.5  and d['top'][i]> img.shape[0] *0.2 and re.findall('[0-9]{2}:[0-9]{2}',d['text'][i]) :
            LIST_LOCAT.append((x,y,w,h))
    LIST_LOCAT.sort(key=lambda i : i[1])
    if len(LIST_LOCAT):
        for ind,(x,y,w,h) in enumerate(LIST_LOCAT):
            if ind != len(LIST_LOCAT)-1 :
                x = h*2
                y = y+(2*h)
                w = img.shape[1] - 4*h
                h = LIST_LOCAT[ind+1][1] -y -h
                
                listtrans.append(img[y:y+h, x:x+w])
            else:
                x = h*2
                y=y+(h*2)
                w = img.shape[1] - 4*h
                h = img.shape[0] - y -(h*5)
                listtrans.append(img[y:y+h, x:x+w])
    if len(listtrans)==0:
        listtranstring=[]
        for i in range(n_boxes):
            get =1
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if  w > img.shape[1]/2 and h > img.shape[1]/4 and h<img.shape[0]/2:
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if len(listtranstring)>0:
                    for box in listtranstring:
                        if box == str(x+y+w+h):
                            get=2
                if get==1:
                    listtrans.append(img[y:y+h, x:x+w])
                    listtranstring.append(str(x+y+w+h))
    listtransactions =[]
    for text in listtrans:
        try:
            currtrans= {
                        'accnum' : '',
                        'money' :'',
                        'time':'',
                        'remainder':'',
                        'transcontent':''
                        }
            res = pytesseract.image_to_string(text)
            if(len(re.findall('\d{13}\s',res))==1):
                currtrans['accnum']=re.findall('\d{13}\s',res)[0].strip()
            if(len(re.findall('(?<=VCB '+currtrans['accnum']+')(.*)(?=VND)',res))==1):
                currtrans['money']=re.findall('(?<=VCB '+currtrans['accnum']+')(.*)(?=VND)',res)[0].strip()
            if(len(re.findall('[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}',res))==1):
                currtrans['time']=re.findall('[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}',res)[0].strip()
            if(len(re.findall('(?<=du )(\d.*)(?=VND)',res))==1):
                currtrans['remainder']=re.findall('(?<=du )(\d.*)(?=VND)',res)[0].strip()
            if(len(res.split('Ref'))==2):
                currtrans['transcontent']=res.split('Ref')[1].strip().replace("\n", " ")
            listtransactions.append(currtrans)
        except:
            continue
    return listtransactions
#****************************************TECHCOM**********************************
def getresTECH(img):
    listtransactions =[]
    h, w, c = img.shape
    img = img[0:h,0:round(w*0.85)]
    res = pytesseract.image_to_string(img,lang='vie')
    listtext = []
    if len(re.findall('\d{14}',res))>0 :
        listtext = res.split(re.findall('\d{14}',res)[0])
        for i in range(1,len(listtext)):
            transcontent=listtext[i]
            trans = {
                'accnum' : '',
                'money' :'',
                'time':'',
                'remainder':'',
                'transcontent':''
                    }
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
            if transcontent!=listtext[i]:
                trans['transcontent']=transcontent.replace("\n", " ")   
            listtransactions.append(trans)
    return listtransactions 
#****************************************BIDV**********************************   
def getlisttransimage(image):
	d = pytesseract.image_to_data(image, output_type=Output.DICT)
	date_pattern = '[0-9]{1,2}:[0-9]{1,2}'
	cou=0
	listtransimage=[]
	n_boxes = len(d['text'])
	listbox=[]
	for i in range(n_boxes):
		
		if np.double(d['conf'][i]) > 60 and np.double(d['left'][i])<image.shape[1]/6 and np.double(d['top'][i])>image.shape[0]/6 and image.shape[0]-np.double(d['top'][i])>image.shape[0]/6:
			if re.match(date_pattern, d['text'][i]):listbox.append((d['left'][i], d['top'][i], d['width'][i], d['height'][i]))
	for (x,y,w,h) in listbox:
		if cou<len(listbox)-1:
			listtransimage.append(image[y:listbox[cou+1][1],0:image.shape[1]])
		else:
			listtransimage.append(image[y:image.shape[0],0:image.shape[1]])
		cou+=1
	return listtransimage

def gettrans(image):
	trans = {
                'accnum' : '',
                'money' :'',
                'time':'',
                'transcontent':''
                    }
	res =  pytesseract.image_to_string(image,lang='vie')
	money = re.findall('(?<=D:)(.*)(?=VND)',res)

	if len(money)>0:
		trans['money']=money[0].strip()
	accnum = re.findall('(?<=n:)(.*)',res)
	time = re.findall('[0-9]{1,2}:[0-9]{1,2} [0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}',res)
	if len(time)>0:
		trans['time']=time[0].strip()
	accnum = re.findall('(?<=n:)(.*)',res)
	if len(accnum)>0:
		trans['accnum']=accnum[0].strip()
	res = res.replace("\n", " ")  
	transcontent = re.findall('(?<=h:)(.*)',res)
	if len(transcontent)>0:
		trans['transcontent']=transcontent[0].strip() 													
	return trans
def getresBIDV(img):  
    LISTTRANS = getlisttransimage(img)
    LISTTRANSACTION =[]
    if len(LISTTRANS)>0:
        for image in LISTTRANS:
            LISTTRANSACTION.append(gettrans(image))
    return LISTTRANSACTION
#****************************************MOMO********************************** 
def getresMOMO(image):
    trans = {
        'money' :'',
        'time':'',
        'phonenumber':'',
        'transID':''
    }
    d = pytesseract.image_to_data(image, output_type=Output.DICT,lang='vie')
    pattern1 = '-\S+'
    pattern2 = '+\S+'
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > image.shape[1]/6 and np.double(d['top'][i]) < image.shape[0]/6 and np.double(d['left'][i]) < image.shape[1]/4 and re.match(pattern1, d['text'][i]) or  re.match(pattern2, d['text'][i]) :
                trans['money'] = str(d['text'][i]).replace('đ','')     
        except:
            continue                                                                                                                
    pattern1 = '[0-9]{1,2}:[0-9]{1,2}'
    pattern2 = '[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}'
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > image.shape[1]/2 and np.double(d['top'][i]) < image.shape[0]/2.5 and re.match(pattern1, d['text'][i])  : trans['time'] = str(d['text'][i]).replace('-','')
            if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > image.shape[1]/2 and np.double(d['top'][i]) < image.shape[0]/2.5 and re.match(pattern2, d['text'][i])  : trans['time'] +='-'+str(d['text'][i]).replace('-','')        
        except:
            continue   
    pattern1 = '[0-9]{9,13}'
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > image.shape[1]/3 and np.double(d['top'][i]) < image.shape[0]/4 and re.match(pattern1, d['text'][i])  : 
                trans['transID'] = d['text'][i]    
        except:
            continue    
    pattern1 = '[0-9]{9,12}'
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 60 and np.double(d['left'][i]) > image.shape[1]/2 and np.double(d['top'][i]) > image.shape[0]*0.6 and re.match(pattern1, d['text'][i])  : 
                trans['phonenumber'] = d['text'][i]    
        except:
            continue   
    MOMO_LOCATE = []
    for i in range(len(d['text'])):
        try:
            if np.double(d['conf'][i]) > 50 and re.search('MoMo', d['text'][i] ) and np.double(d['left'][i]) < image.shape[1]/2 and np.double(d['top'][i]) > image.shape[0]*0.6: 
                MOMO_LOCATE.append((d['left'][i], d['top'][i], d['width'][i], d['height'][i]))
        except:
            continue   
    if len(MOMO_LOCATE)==1:
        (x,y,w,h) = MOMO_LOCATE[0]
        for i in range(len(d['text'])):
            try:
                if np.double(d['conf'][i]) > 50  and np.double(d['left'][i]) > image.shape[1]/2 and np.double(d['top'][i]) > y-10 and np.double(d['top'][i]) < y+10: 
                    trans['wallet'] +=' '+ d['text'][i]      
                    trans['wallet'].strip()
            except:
                continue  
    return [trans]
#########################################################################MB##################################################################################################

def getlisttransimageMB(image):
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    keys = list(d.keys())
    listtransimage=[]
    listbox=[]
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if np.double(d['conf'][i]) > 60 and str(d['text'][i])=='TK':
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i]) ;listbox.append((d['left'][i], d['top'][i], d['width'][i], d['height'][i]))
    if len(listbox)>0 :
        cou=0
        for (x,y,w,h) in listbox:
            y-=10
            if cou<len(listbox)-1:
                listtransimage.append(image[y:listbox[cou+1][1],0:image.shape[1]])
            else:
                listtransimage.append(image[y:image.shape[0],0:image.shape[1]])
            cou+=1   
    return listtransimage         


                                 
def gettransMB(image):
    trans = {
                'accnum' : '',
                'money' :'',
                'time':'',
                'transcontent':'',
                'remainder':''
                    }
    res =  pytesseract.image_to_string(image,lang='vie')
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    for i in range(len(d['text'])):
        if re.findall('\d{9,15}',d['text'][i]) and  d['top'][i]<20 :
            trans['accnum']=re.findall('\d{9,15}',d['text'][i])[0].strip();break
    for i in range(len(d['text'])):
        if str(d['text'][i]).count('VND') and str(d['text'][i]).count('+') or str(d['text'][i]).count('-') :
            trans['money']=d['text'][i].strip();break
    remainder = re.findall('(?<=SD)(.*)(?=VND)[0-9]{0,15}',res)
    if len(remainder)>0:
            trans['remainder']=remainder[0].replace(':','').replace(',','').strip()
    if(len(re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}',res))==1):
            trans['time']=re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}',res)[0].strip()
    transcontent = re.findall('(?<=ND:)(.*)',res)
    if(len(res.split('ND:'))==2):
            trans['transcontent']=res.split('ND:')[1].strip().replace("\n", " ").replace(':','').replace(',','').strip()
 
    return trans
def getresMB(img):  
    LISTTRANS = getlisttransimageMB(img)
    LISTTRANSACTION =[]
    if len(LISTTRANS)>0:
        for image in LISTTRANS:
            LISTTRANSACTION.append(gettransMB(image))
            print(gettransMB(image))
    return LISTTRANSACTION  



if __name__ == "__main__":

    data =  ''
    CV2_IMG = readb64(data)
    BANK_TYPE = BANK_LIST[np.argmax(getbankname(CV2_IMG))]
    RES_STRING = []
    try:
        if BANK_TYPE == 'VIETCOM':
            RES_STRING =getresVIETCOM(CV2_IMG)
        if BANK_TYPE == 'TECH':
            RES_STRING =getresTECH(CV2_IMG)
        if BANK_TYPE == 'BIDV':
            RES_STRING =getresBIDV(CV2_IMG)
        if BANK_TYPE == 'MOMO':
            RES_STRING =getresMOMO(CV2_IMG)
        if BANK_TYPE == 'MB':
            RES_STRING =getresMB(CV2_IMG)
        json_string = json.dumps(RES_STRING,indent=2)
        print(BANK_TYPE)
        print(json_string)
    except:
        print(BANK_TYPE)
   
    

    
    