# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image
from skimage import data
from skimage import color
from skimage import morphology
from skimage import segmentation

# The function configures an image before segmentation
def imageConfigSegment(path, threshold = 0.6, min_size = 1000, area_threshold = 1000):
    # The function gets numpy array for image and mask and returns the cropped image by the mask
    def cropShape(npImg, npMask):
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

        return (npCropImg)
    
    # The function prints the contour only
    # Remember to remove figsize after all test has been done!!!!!!!!!!!!!
    def cropContour(qContourSet, figsize):
        
        # Test image
        data = np.zeros( (figsize[0],figsize[1],3), dtype=np.uint8 )
        
        # Set white pixels
        for i in range(figsize[0]):
            for j in range(figsize[1]):
                data[i][j] = [255,255,255]
        
        # Get all contour pathes (if multiple shapes)
        pathes = qContourSet.collections[0].get_paths()  # grab the 1st path
        for path in pathes:
            coordinates = path.vertices
            
            # Run over coordinates and set red color pixel
            for cord in coordinates:
                data[int(cord[1])][int(cord[0])] = [254,0,0]
        
        # Show reuslt image
        image = Image.fromarray(data)
        image.show()
    
    # The function Performs the segmentation
    def perform_segmentation():
        # Open the image as basic image
        im = Image.open(path)
        
        # Open the image as numpy array
        #img = plt.imread(path)
        
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
        mask = morphology.closing(mask, morphology.disk(3))

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
        cropContour(contLines, (width, height))
        
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
        
        return (img_arr)
    return perform_segmentation