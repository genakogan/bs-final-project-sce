# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import io
import cv2
import imutils
from PIL import Image
from skimage import data
from skimage import color
from skimage import morphology
from skimage import segmentation
from os.path import splitext

# Constant variable definition
SAVE_OPTION_FALSE               = 0             # Save option was not selected
SAVE_OPTION_TRUE                = 1             # Save option was selected
SAVE_FILENAME_INDEX             = 0             # Save filename index in splited list of filename and extension
SAVE_FILE_EXTENSION_INDEX       = 1             # Save file extension index in splited list of filename and extension
SAVE_FAILED                     = 0             # Status for image that failed in save
SAVED_SUCCESSFULLY              = 1             # Status for image saved successfully
PIXEL_TO_MM_VAL                 = 0.352777778   # The value of One pixel converted to milimeters
XYZ_LAST_INDEX                  = 2             # The index of Z in the result list to check convert to milimeters
X_INDEX_IN_LINE                 = 0             # The index of the x coordinate in a line
Y_INDEX_IN_LINE                 = 1             # The index of the y coordinate in a line
CONTOUR_FILENAME_ADDITION       = "_contour"    # Save contour file additional word
GRAYSCALE_FILENAME_ADDITION     = "_grayscale"  # Save grayscale file additional word

# The function configures an image before segmentation
def imageConfigSegment(path, threshold = 0.6, min_size = 1000, area_threshold = 5000, max_size = 50000):
         
    # Create sizes matrix
    sizesMat = np.zeros(1)
    
    # The function returns string with result to write to file according to the array
    def buildResultString(lstInput):
        # Initialize the result string
        strResult = ""
        
        # Get the amount of items in each line
        nLineSize = len(lstInput[0])
        
        # Run over the list values
        for line in lstInput:
            # Initialize current line
            curLine = ""
            
            # Run over the values of the point
            for nIndx in range(nLineSize):
               
                # Check if the current cell is part of X,Y,Z to convert to milimeters
                if (nIndx <= XYZ_LAST_INDEX):
                    # Convert the value of coordinate to milimeters
                    curLine += '{0:.3f}'.format(int(line[nIndx]) * PIXEL_TO_MM_VAL)
                # The current cell is not x,y or z therefore save it as is
                else:
                    curLine += str(line[nIndx])     
                
                # Check if last column reached
                if (nIndx == (nLineSize - 1)):
                    # Add the shape index
                    curLine += ', ' + str(int(sizesMat[line[X_INDEX_IN_LINE]][line[Y_INDEX_IN_LINE]][0]))
                    
                    curLine += '\n'
                # Current column is not the last one
                else:
                    curLine += ', '
                    
                # Increment index column
                nIndx += 1
            
            # Append the current line to the result
            strResult += curLine
        
        return (strResult)
    
    # Convert image numpy array to grayscale
    def grayConversion(image):
        grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
        gray_img = grayValue.astype(np.uint8)
        return gray_img
    
    # The function gets numpy array for image and mask and returns the cropped objects in the image
    def convertMaskToMatrix(npImg, npMask):
        # Copy the image to new numpy array of pixels
        npCropImg = np.copy(npImg)

        # Initialize the indexes for loop
        nIndxRow = 0
        nIndxCol = 0

        # Run over the rows of the image
        for nIndxRow in range(0, npImg.shape[0]):
            # Run over the columns of the image
            for nIndxCol in range(0, npImg.shape[1]):
                # If the current pixel is set to False in the mask then the pixel is not part of the bone
                if npMask[nIndxRow][nIndxCol] == False:
                    # Reset the pixel if it is not part of the bone
                    npCropImg[nIndxRow][nIndxCol] = [0,0,0]
                # The pixel is part of the bone - set white
                else:
                    npCropImg[nIndxRow][nIndxCol] = [255,255,255]

        return (npCropImg)
    
    # The function convert matrix to boolean matrix
    def convertMatrixToBool(npMask, npNewMask):
        # Copy the image to new numpy array of pixels
        npBool = np.copy(npMask)
        #npBool = np.full((npNewMask.shape[0], npNewMask.shape[1]), False)
        #print(npBool)

        # Initialize the indexes for loop
        nIndxRow = 0
        nIndxCol = 0

        # Run over the rows of the image
        for nIndxRow in range(0, npNewMask.shape[0]):
            # Run over the columns of the image
            for nIndxCol in range(0, npNewMask.shape[1]):
                # If the current pixel is set to White in the mask then the pixel is part of the mask
                npBool[nIndxRow][nIndxCol] = (npNewMask[nIndxRow][nIndxCol][0] == 255)

        return (npBool)
    
    # The function removes from the mask objects that greater than maxSize
    def findMaskByMaxSize(npMask, npImage, maxSize):
        # Set the sizes matrix configurable within this function
        nonlocal sizesMat
        
        # Reset the sizes matrix to zero values
        sizesMat = np.zeros(npImage.shape)
        
        # Convert the boolean mask to numpy matrix
        mask = convertMaskToMatrix(npImage, npMask)
        
        # Conuter for shape
        nCounterShape = 1
        
        # Perform morphological operations on the mask
        se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se2)
        
        # Find the contours of the objects in the mask
        cnts = cv2.findContours(cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # Run over the contours and test them by area
        for currCont in cnts:
            # Check if current contour's area is greater than maxSize
            if (cv2.contourArea(currCont) > maxSize):
                # Remove the contour from the mask by filling it with black color
                cv2.drawContours(mask, [currCont], 0, (0, 0, 0), thickness = cv2.FILLED)
            # The contour is not greater than max
            else:
                # Fill the shape with color that incremented by One each contour
                cv2.drawContours(sizesMat, [currCont], 0, (nCounterShape, 0, 0), thickness = cv2.FILLED)
                
                # Fill the borders of the shape with the same color for contour
                cv2.drawContours(sizesMat, [currCont], 0, (nCounterShape, 0, 0), thickness = 2)
                
                # Increment contour shape by One
                nCounterShape += 1
        
        return (convertMatrixToBool(npMask,mask))
        
    
    # The function gets numpy array for image and mask and returns the cropped image by the mask
    def cropShape(npImg, npMask, nZValue):
        # Copy the image as grayscale
        npGrayImage = grayConversion(npImg)
        
        # list of grayscale values
        lstGrayscale = []

        # Initialize the indexes for loop
        nIndxRow = 0
        nIndxCol = 0

        # Run over the rows of the image
        for nIndxRow in range(0, npImg.shape[0]):
            # Run over the columns of the image
            for nIndxCol in range(0, npImg.shape[1]):
                # If the current pixel is part of the bone
                if npMask[nIndxRow][nIndxCol] == True:
                    # Add the point to grayscle array
                    lstGrayscale.append((nIndxRow, nIndxCol, nZValue, npGrayImage[nIndxRow][nIndxCol]))

        return (lstGrayscale)
    
    # The function prints the contour only
    def cropContour(qContourSet, nZValue):
        # Contour points list
        lstContourPoints = []
        
        # Get all contour pathes (if multiple shapes)
        pathes = qContourSet.collections[0].get_paths()  # grab the 1st path
        
        # Run over all the pathes in the contour
        for path in pathes:
            coordinates = path.vertices
            
            # Run over coordinates and insert them into the contour list
            for cord in coordinates:
                # Add the coordinates of the contour to the result list
                lstContourPoints.append((int(cord[1]), int(cord[0]), nZValue))
        
        return (lstContourPoints)
    
    # Test function to write the sizes matrix to file
    # Delete when end testing
    def testSizesMat():
        nonlocal sizesMat
        strT = ""
        for x in range(512):
            for y in range(512):
                strT += str(int(sizesMat[x][y][0])) + " "
            strT += "\n"
        with open("test.txt", "w") as t:
            t.write(strT)
        
    
    # The function Performs the segmentation
    def perform_segmentation(saveOption = SAVE_OPTION_FALSE, saveFilepath = "", saveFilename = "", nZValue = 0):
        # Open the image as basic image
        im = Image.open(path)
        
        # Convert the image to numpy array
        img = np.array(im)
        
        # Get the height and width of the image
        height, width, depth = img.shape
        
        # Set DPI value for the image as default DPI
        dpi = 72
        
        # Calculate the correct figure size in order to save dimensions of the image
        figsize = width / float(dpi), height / float(dpi)

        # Compute a mask for the bone
        lum = color.rgb2gray(img) # Convert the image to graycicle
        mask = morphology.remove_small_holes(
            morphology.remove_small_objects(
                lum > threshold, min_size),
            area_threshold) # Compute the mask by deletion of small holes

        # Remove some of foreground - Erosion
        mask = morphology.opening(mask, morphology.disk(1))

        # Remove some holes in the object - Dilation
        mask = morphology.closing(mask, morphology.disk(1))
        
        # Find the objects that not large than max size
        mask = findMaskByMaxSize(mask, img, max_size)

        # SLIC result
        #slic = segmentation.slic(img, n_segments=1, start_label=1)

        # Check if the mask is not empty
        if (mask.all()):
            # Use maskSLIC result
            m_slic = segmentation.slic(img, n_segments=1, mask=mask, start_label=1)
        else:
            # Use the slic algorithm instead of mask slic if mask empty
            #m_slic = slic
            m_slic = segmentation.slic(img, n_segments=1, start_label=1)
        
        # Display result
        # Set the figure size the same as the real image size
        fig = plt.figure(figsize = figsize)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(segmentation.mark_boundaries(img, m_slic), interpolation='nearest')
        
        # Create bone contour and save contour lines in contLines
        contLines = ax.contour(mask, colors='red', linewidths=0.5)
        
        # Get the image contour only
        #cropContour(contLines, (width, height))
        
        # Disable axises in the result image
        plt.axis('off')
        
        # Save the result as temporary image in the memory
        io_buf = io.BytesIO()
        plt.savefig(io_buf, bbox_inches='tight')
        io_buf.seek(0)
        img_arr = Image.open(io_buf)
        rgb = img_arr.convert('RGB')
        
        # Close the buffer channel
        io_buf.close()
        
        # Close figure after end of segmentation in order to save memory
        plt.close()
        
        # Check if save option was selected
        if (saveOption):
            # Calculate the contour points list
            lstContourPoints = cropContour(contLines, nZValue)
            
            # Prepare contour points filename - first split the filename and extension
            lstFileAndExtension = splitext(saveFilename)
            
            # Add the word _contour after filename and then add extension
            strContourFile = saveFilepath + "\\" + lstFileAndExtension[SAVE_FILENAME_INDEX] + CONTOUR_FILENAME_ADDITION + lstFileAndExtension[SAVE_FILE_EXTENSION_INDEX]
            
            # Add the word _grayscale after filename and then add extension
            strGrayscaleFile = saveFilepath + "\\" + lstFileAndExtension[SAVE_FILENAME_INDEX] + GRAYSCALE_FILENAME_ADDITION + lstFileAndExtension[SAVE_FILE_EXTENSION_INDEX]
            
            # Try save contour to file
            try:
                # Write contour points to file
                with open(strContourFile, "a") as outContour:
                   #outContour.write(str(lstContourPoints) + '\n\n')
                   outContour.write(buildResultString(lstContourPoints))
            except:
                print("Error in save contour")
                
                return (SAVE_FAILED)
            
            # Calculate the grayscale points list
            lstGrayscalePoints = cropShape(img, mask, nZValue)
            
            # Try save grayscale to file
            try:
                # Write grayscale points to file
                with open(strGrayscaleFile, "a") as outGrayscale:
                   #outGrayscale.write(str(lstGrayscalePoints) + '\n\n')
                   outGrayscale.write(buildResultString(lstGrayscalePoints))
            except:
                print("Error in save grayscale")
                
                return (SAVE_FAILED)
                
            return (SAVED_SUCCESSFULLY)
        
        return (img_arr)
    return perform_segmentation