from keras.models import load_model
import numpy as np
import base64
import json
import os
from Utils.helper import *
from Utils.Vietcom import getresVIETCOM
from Utils.Tech import getresTECH
from Utils.Bidv import getresBIDV
from Utils.Momo import getresMOMO
from Utils.Mb import getresMB
from Utils.Acb import getresAcb
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
#Định nghĩa
model = load_model('keras_model.h5')
BANK_LIST =['VIETCOM','TECH','BIDV','MOMO','MB','ACB','AGRI']

if __name__ == "__main__":

    data = base64.b64encode(open(r'Acb\Acb\z3810160886946_00f1d575646cc871ddb17fd9b6666d82.jpg', "rb").read()).decode('utf8') # image to base64
    CV2_IMG = readb64(data)
    BANK_TYPE = BANK_LIST[np.argmax(getbankname(model,CV2_IMG))]
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
        if BANK_TYPE == 'ACB':
            RES_STRING =getresAcb(CV2_IMG)
        json_string = json.dumps(RES_STRING,indent=2)
        print(BANK_TYPE)
        print(json_string)
    except:
        print(BANK_TYPE)            