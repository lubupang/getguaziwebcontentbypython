from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import  SVGPathPen
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from ddddocr import DdddOcr
from PIL import Image
import os
import shutil
import time
import requests
import hashlib
import re


def getDict(yourwofffile):
    pathname=str(int(time.time()*(10**7)))
    res_d={}
    if not os.path.exists(pathname):
        os.mkdir(pathname)
    font=TTFont(yourwofffile)
    charsdict=font.getBestCmap()
    print(charsdict)
    for char1,x in charsdict.items():
        print(x)
        pen=SVGPathPen(font.getGlyphSet())
        font.getGlyphSet()[x].draw(pen)
        xMin, xMax, yMin, yMax = font['head'].xMin, font['head'].xMax, font['head'].yMin, font['head'].yMax
        height1 = (yMax - yMin)
        width1 = (xMax - xMin)
        r=width1/100
        svg1=f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="{xMin} {yMin} {width1} {height1}"><g transform="matrix(0.6 0 0 -0.6 {xMin+width1*0.2} {yMin+yMax-height1*0.2})"><path stroke = "black" fill = "black" d="{pen.getCommands()}"/></g></svg>'
        with open(rf'{pathname}\{x}.svg','w') as f:
            f.write(svg1)
        drawing=svg2rlg(rf'{pathname}\{x}.svg')
        renderPM.drawToFile(drawing,rf'{pathname}\{x}.png',fmt='PNG')
        img=Image.open(rf'{pathname}\{x}.png')      
        img.thumbnail((100,int(height1/r)))
        img.save(rf'{pathname}\{x}.png','png')        
        with open(rf'{pathname}\{x}.png','rb') as f:
            ocr=DdddOcr()
            text1=ocr.classification(f.read())            
            if text1!=None and text1!='':            
                res_d[x.lower()]={'unicode_hex':hex(int(char1)),'char':text1[:1].replace('o','0')}
    shutil.rmtree(pathname)
    return res_d


