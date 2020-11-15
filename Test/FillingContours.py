# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:40:21 2020

@author: Aviel-PC
"""
import numpy as np
import imutils
import cv2
from skimage import color
from PIL import Image
from datetime import datetime

def is_contour_bad(c):
	# the contour is 'bad' if it is greater than max size
    if (cv2.contourArea(c) > 10000):
        return True
    return False

mask = cv2.imread("test.jpg")
mask_inv = cv2.bitwise_not(mask)

se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se2)


#edged = cv2.Canny(mask_inv, 50, 100)
test = mask.copy()

cnts = cv2.findContours(cv2.cvtColor(test, cv2.COLOR_RGB2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    if is_contour_bad(c):
        cv2.drawContours(test, [c], 0, (0, 0, 0), thickness = cv2.FILLED)
  
i1 = Image.fromarray(test, 'RGB')
i1.show()

print(datetime.now())