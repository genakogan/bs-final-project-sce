# -*- coding: utf-8 -*-

import SimpleITK as sitk

img = sitk.ReadImage("C:\\Users\\Aviel-PC\\Documents\\Final-Project\\Not in Git\\Dicom\\IMG-0001-00001.dcm")
# rescale intensity range from [-1000,1000] to [0,255]
img = sitk.IntensityWindowing(img, -1000, 1000, 0, 255)
# convert 16-bit pixels to 8-bit
img = sitk.Cast(img, sitk.sitkUInt8)

sitk.WriteImage(img, "C:\\Users\\Aviel-PC\\Documents\\Final-Project\\Not in Git\\Dicom\\IMG-0001-00001.png")