# -*- coding: utf-8 -*-

# import the necessary packages
import numpy as np
import imutils
import cv2
from skimage import color

def is_contour_bad(c):

	# the contour is 'bad' if it is not a rectangle
	return cv2.contourArea(c) < 100

# load the shapes image, convert it to grayscale, and edge edges in
# the image
image = cv2.imread("test_uncrop.jpg")
mask = cv2.imread("test.jpg")

#mask = cv2.GaussianBlur(mask, (7, 7), 0)
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
mask_inv = cv2.bitwise_not(mask)
edged = cv2.Canny(mask_inv, 50, 100)
#edged = cv2.dilate(edged, None, iterations=1)
#edged = cv2.erode(edged, None, iterations=1)


#mask_inv = cv2.bitwise_not(mask)
#print(mask.shape)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#edged = cv2.Canny(mask, 50, 100)
#cv2.imshow("Original", image)
# find contours in the image and initialize the mask that will be
# used to remove the bad contours
#cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cnts = imutils.grab_contours(cnts)
#mask = np.ones(mask.shape[:2], dtype="uint8") * 255
#print(mask.shape)
# loop over the contours
#for c in cnts:
	# if the contour is bad, draw it on the mask
#	if is_contour_bad(c):
#		cv2.drawContours(mask, [c], -1, 0, -1)
        
# remove the contours from the image and show the resulting images
image = cv2.bitwise_and(image, mask_inv)
cv2.imshow("Mask", mask)
cv2.imshow("After", image)
cv2.imwrite("res.jpg",image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)