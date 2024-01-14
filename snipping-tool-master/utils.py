import numpy as np
# from sympy import Point, Segment
from os import path as PATH
import cv2, pathlib, os, time, re
dstH = 300 if 1==1 else 900
drawFlag = True if 1==11 else False

def scaledShow(img, name='image', h=dstH, pos=(None,None)):
    resized = cv2.resize(img, (int(h/img.shape[0]*img.shape[1]), h), 
                            interpolation=cv2.INTER_LANCZOS4)
    cv2.imshow(name, resized)
    if pos[0] is not None and pos[1] is not None:
        cv2.moveWindow(name, pos[0],pos[1])
    cv2.waitKey(0)
def absGetBooknumdir(path): # Absolute path
    split = path.split(os.sep)
    for i in range(len(split),0,-1):
        if re.search(r'\d{7}', split[i-1]): break
    if i>=2: return split[i-1] # Folder containing digits was found
    else: return '000000000'
def getFirstFileLikeWindows(files):
    if len(files)==0: return None
    ref = PATH.basename(files[0])
    if len(files) >= 2:
        stem0 = PATH.splitext(ref)[0]
        if stem0.endswith('-1'):
            name1 = PATH.basename(files[1])
            stem1 = PATH.splitext(name1)[0]
            try:
                stem0 = int(stem0.lstrip('a').rstrip('-1'))
                stem1 = int(stem1.lstrip('a').rstrip('-1'))
                # if stem0<stem1: ref=PATH.basename(files[0])
                if stem0==stem1: ref=name1
            except: pass
    return ref
def rstripBooknumdir(folderstr):
    split = folderstr.split('-')
    for i in range(len(split)):
        if re.search(r'\d{7}',split[i]): break
    else:
        # print('Booknum not found')
        return folderstr
    return '-'.join(split[:i+1])

def logError(path, funcName, 
             rootLogdir='\\\\Nascsncl\\tifhp\\BU3-QC&RD\\csv_logs'):
    errLogdir = f'{rootLogdir}{os.sep}error_logs'
    pathlib.Path(errLogdir).mkdir(parents=True, exist_ok=True)
    with open(f'{errLogdir}{os.sep}{absGetBooknumdir(path)}__\
{int(time.time()%10000):04}.csv', 'w+') as errLogfile:
        errLogfile.write(f'path,{path.rstrip(os.sep)}\n')
        errLogfile.write(f'func,{funcName}\n')


def largeCropQuick(image):  # largeCrop2.1.2
    bord = 50
    image = cv2.copyMakeBorder(image, bord,bord,bord,bord,
                                cv2.BORDER_CONSTANT, value=[0, 0, 0])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thres = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[0]
    binIm = cv2.threshold(gray, thres*1, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(binIm, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < image.shape[0]**2/5: continue
        if area>maxArea:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*perimeter, True)
            maxArea = area
    pad = 0
    sortIdx = np.argsort(approx[:,0,0])
    left = round(approx[sortIdx[1]][0][0]  + pad)
    right = round(approx[sortIdx[-2]][0][0] -pad)
    sortIdx = np.argsort(approx[:,0,1])
    top = round(approx[sortIdx[1]][0][1]   + pad)
    bottom = round(approx[sortIdx[-2]][0][1]-pad)
    return image[top:bottom, left:right]


def getSepErase(image):
    newImage = image.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thres = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[0]
    thresImage = cv2.threshold(blur, thres*0.9, 255, cv2.THRESH_BINARY_INV)[1] # Greater thres for thicker text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,2))
    dilate = cv2.dilate(thresImage, kernel, iterations=5)
    contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    expand = 0
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        if rect[0][1] < newImage.shape[0]*0.023: continue
        if rect[0][1] > newImage.shape[0]*0.8: continue
        if rect[2] < 45:
            if rect[1][0] > 0.3*newImage.shape[1] and rect[1][0]/rect[1][1] > 7:
                rect = [list(rect[0]), list(rect[1]), rect[2]]
                expand = 2*rect[1][1]
                rect[1][0] += expand
                break
        else:
            if rect[1][1] > 0.3*newImage.shape[1] and rect[1][1]/rect[1][0] > 7:
                rect = [list(rect[0]), list(rect[1]), rect[2]]
                expand = 2*rect[1][0]
                rect[1][1] += expand
                break
    else: return None
    if rect[0][1] > image.shape[0]*0.3: return None
    box = np.intp(np.round(cv2.boxPoints(rect)))
    cv2.drawContours(newImage, [box], 0, (0,255,0), 2)

    expand *= 2
    sortedIX = np.argsort(box[:,0])
    if box[sortedIX[0]][1] < box[sortedIX[1]][1]:
        box[sortedIX[0]][1] -= expand
        roll = sortedIX[0]
    else:
        box[sortedIX[1]][1] -= expand
        roll = sortedIX[1]

    if box[sortedIX[2]][1] < box[sortedIX[3]][1]:
        box[sortedIX[2]][1] -= expand
    else:
        box[sortedIX[3]][1] -= expand
    if roll>0: box = np.roll(box, shift=-roll, axis=0)
    # scaledShow('erase', newImage)
    # print('↑ Separator detected')
    return box