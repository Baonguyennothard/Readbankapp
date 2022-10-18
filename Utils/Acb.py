import pytesseract
from pytesseract import Output
import re
import numpy as np
import cv2


def get_list_x_y(cv2image):
    width = cv2image.shape[1]
    List_locate = []
    d = pytesseract.image_to_data(cv2image, output_type=Output.DICT)
    for i in range(len(d['text'])):
        if np.double(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if x < round(width/3) and re.findall('[0-9]{2}:[0-9]{2}',d['text'][i]):
                List_locate.append((x,y,d['text'][i]))
    return List_locate
def getmoney(string):
    s = ''
    for char in string:
        if str(char).isnumeric() or char=='-' or char == '+' or char == ',':
            s+=char
    return s
def gettransACB(image,List_locate):
    list_trans = []
    
    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    for ind,(x,_MIN_Y,time) in enumerate(List_locate):
        trans = {
                'accnum' : '',
                'money' :'',
                'time':str(time),
                'transcontent':'',
                'remainder':''
                    }
        if ind < len(List_locate)-1:
            _MAX_Y = List_locate[ind+1][1]
            res =  pytesseract.image_to_string(image[_MIN_Y:_MAX_Y,5:image.shape[1]],lang='vie')
            for i in range(len(d['text'])):
                pattern = re.findall('\d{7,13}',d['text'][i])
                if pattern  and  d['top'][i]>_MIN_Y and d['top'][i]<_MAX_Y :
                    trans['accnum']=pattern[0].strip();break
            pattern = re.findall('(?<=VND)(.*)(?=l)[0-9]{0,15}',res)
            if pattern :
                trans['money']=getmoney(pattern[0])
            pattern = re.findall('(?<=u)(.*)(?=G)[0-9]{0,15}',res)
            if pattern  :
                trans['remainder']=getmoney(pattern[0])
                cont = str(res).split(trans['remainder'])
                if len(cont)==2:
                    trans['transcontent']= cont[1]
            
        else:
            res =  pytesseract.image_to_string(image[_MIN_Y:image.shape[0],5:image.shape[1]],lang='vie')
            for i in range(len(d['text'])):
                pattern = re.findall('\d{7,13}',d['text'][i])
                if pattern  and  d['top'][i]>_MIN_Y  :
                    trans['accnum']=pattern[0].strip();break
            pattern = re.findall('(?<=VND)(.*)(?=l)[0-9]{0,15}',res)
            if pattern :
                trans['money']=getmoney(pattern[0])
            pattern = re.findall('(?<=u)(.*)(?=G)[0-9]{0,15}',res)
            if pattern  :
                trans['remainder']=getmoney(pattern[0])
                cont = str(res).split(trans['remainder'])
                if len(cont)==2:
                    trans['transcontent']= cont[1]
        list_trans.append(trans)
    return list_trans
def getresAcb(image):     
    List_locate = get_list_x_y(image)     
    return gettransACB(image,List_locate)
            


# if __name__ == "__main__":
#     img = cv2.imread('D:\Working\Octa\Readbankapp\Acb\Acb\z3810160959955_72f472121a15396716ddb165f687308f.jpg')
#     List_locate = get_list_x_y(img)
#     print(gettransACB(img,List_locate))