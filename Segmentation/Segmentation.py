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
    
    # The function Performs the segmentation
    def perform_segmentation():
        # Open the image as numpy array
        img = plt.imread(path)

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
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111)
        ax.imshow(segmentation.mark_boundaries(img, slic), interpolation='nearest')
        ax.contour(mask, colors='red', linewidths=0.5)
        plt.axis('off')
        #plt.savefig('Preview.jpg', bbox_inches='tight')
        
        # Save the result as temporary image in the memory
        io_buf = io.BytesIO()
        plt.savefig(io_buf, bbox_inches='tight')
        io_buf.seek(0)
        #img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
        #                     newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        img_arr = Image.open(io_buf)
        rgb = img_arr.convert('RGB')
        
        io_buf.close()
        return img_arr
    return perform_segmentation

#images = [imageConfigSegment("crop2.jpg"),imageConfigSegment("crop3.jpg"),imageConfigSegment("crop4.jpg",0.7)]
#for image in images:
#    image()
    
#images = [imageConfigSegment("crop2.jpg"),imageConfigSegment("crop3.jpg", 0.6, 1000),imageConfigSegment("crop6.jpg",0.57,1000,1500)]
#for image in images:
#    image()
#plt.imshow()
#imageConfigSegment("crop3.jpg")()
#plt.imshow(imageConfigSegment("crop2.jpg"))

#Black and white pen
#images = [imageConfigSegment("crop2.jpg"),imageConfigSegment("crop3.jpg", 0.6, 1000),imageConfigSegment("crop7c.jpg",0.57,1500,1500)]
#for image in images:
#    image()