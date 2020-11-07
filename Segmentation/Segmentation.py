# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import io
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
COLUMN_NAMES                    = ['X', 'Y',
                                   'Z', 'HU']   # Name of columns in result file
CONTOUR_FILENAME_ADDITION       = "_contour"    # Save contour file additional word
GRAYSCALE_FILENAME_ADDITION     = "_grayscale"  # Save grayscale file additional word

# The function configures an image before segmentation
def imageConfigSegment(path, threshold = 0.6, min_size = 1000, area_threshold = 1000):
    
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
                # Build result line
                curLine += COLUMN_NAMES[nIndx] + ":" + str(line[nIndx])
                
                # Check if last column reached
                if (nIndx == (nLineSize - 1)):
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
    
    # The function Performs the segmentation
    def perform_segmentation(saveOption = SAVE_OPTION_FALSE, saveFilepath = "", saveFilename = "", nZValue = 0):
        # Open the image as basic image
        im = Image.open(path)
        
        # Convert the image to numpy array
        img = np.array(im)
        
        # Get the height and width of the image
        height, width, depth = img.shape
        
        # Set DPI value for the image as default DPI
        #dpi = im.info['dpi'][0]
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

        # SLIC result
        slic = segmentation.slic(img, n_segments=1, start_label=1)

        # maskSLIC result
        m_slic = segmentation.slic(img, n_segments=1, mask=mask, start_label=1)

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