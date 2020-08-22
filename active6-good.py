import matplotlib.pyplot as plt
from skimage import data
from skimage import color
from skimage import morphology
from skimage import segmentation
# Input data
img = plt.imread('crop.jpg')
img[10][10] = 0

# Compute a mask for the bone
lum = color.rgb2gray(img) # Convert the image to graycicle
mask = morphology.remove_small_holes(
    morphology.remove_small_objects(
        lum < 0.5156, 500),
    500) # Compute the mask by deletion of small holes

# Different version
"""
mask = morphology.remove_small_holes(
    morphology.remove_small_objects(
        lum < 0.7, 500),
    500)
"""


mask = morphology.opening(mask, morphology.disk(1)) # Remove some of foreground - Erosion

# SLIC result
slic = segmentation.slic(img, n_segments=1, start_label=1)

# maskSLIC result
m_slic = segmentation.slic(img, n_segments=1, mask=mask, start_label=1)

# Display result
fig, ax_arr = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10, 10))
ax1, ax2, ax3, ax4 = ax_arr.ravel()

ax1.imshow(img)
ax1.set_title("Original image")

ax2.imshow(mask, cmap="gray")
ax2.set_title("Mask of the image")

ax3.imshow(segmentation.mark_boundaries(img, slic))
ax3.contour(mask, colors='red', linewidths=1)
ax3.set_title("SLIC Algorithm")

ax4.imshow(segmentation.mark_boundaries(img, m_slic))
ax4.contour(mask, colors='red', linewidths=1)
ax4.set_title("maskSLIC Algorithm")

# Don't show the axis for images - turn them off
for ax in ax_arr.ravel():
    ax.set_axis_off()

# Set output to be tight in order to show larger images
plt.tight_layout()
plt.show()