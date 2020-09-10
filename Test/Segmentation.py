import matplotlib.pyplot as plt
import numpy as np

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
        fig, ax_arr = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
        ax1, ax2, ax3, ax4 = ax_arr.ravel()

        ax1.imshow(cropShape(img,mask))
        ax1.set_title("Original image")

        ax2.imshow(mask, cmap="gray")
        ax2.set_title("Mask of the image")

        ax3.imshow(segmentation.mark_boundaries(img, slic))
        ax3.contour(mask, colors='red', linewidths=0.5)
        ax3.set_title("SLIC Algorithm")

        ax4.imshow(segmentation.mark_boundaries(img, m_slic))
        ax4.contour(mask, colors='red', linewidths=0.5)
        ax4.set_title("maskSLIC Algorithm")

        # Don't show the axis for images - turn them off
        for ax in ax_arr.ravel():
            ax.set_axis_off()

        # Set output to be tight in order to show larger images
        plt.tight_layout()
        plt.show()
    return perform_segmentation

images = [imageConfigSegment("crop2.jpg"),imageConfigSegment("crop3.jpg"),imageConfigSegment("crop4.jpg",0.7)]
for image in images:
    image()