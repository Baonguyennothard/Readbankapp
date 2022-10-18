import pytesseract
from pytesseract import Output
import re
import numpy as np

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