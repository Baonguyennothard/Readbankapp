import pytesseract
from pytesseract import Output
import re
import numpy as np

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