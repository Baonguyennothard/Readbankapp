import pytesseract
from pytesseract import Output
import re
import numpy as np

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