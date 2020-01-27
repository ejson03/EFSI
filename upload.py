import cv2
import os
import numpy as np
import owncloud
from datetime import date, datetime

def setup(today):
    oc = owncloud.Client('http://localhost/owncloud')
    oc.login('wagner', 'qazwsxedcrfvt')
    folder = f'{today.day}-{today.month}'
    try:
        oc.mkdir(folder)
        os.mkdir(folder)
    except:
        raise Exception('Directory exists for today')
    return oc, folder

def capture(oc, folder):
    sec = 0
    cap = cv2.VideoCapture(0)
    if (cap.isOpened() == True):
        while(True):
            cap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = cap.read()
            if hasFrames:
                upload_file = f'{folder}/{datetime.now().strftime("%H-%M-%S")}.jpg'
                cv2.imwrite(upload_file, image)
                oc.put_file(upload_file, upload_file)
                sec+=1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    today = date.today()
    oc,folder = setup(today)
    capture(oc,folder)