import pytesseract
from pytesseract import Output
import re
import numpy as np

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
    return LISTTRANSACTION