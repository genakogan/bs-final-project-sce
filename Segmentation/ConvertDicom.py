# -*- coding: utf-8 -*-

import pydicom as dicom
import os
import cv2
import pandas as pd
import csv
import numpy as np
from PIL import Image

# Constant definition
DICOM_DESCRIPTION_FILE_PATH = "./DicomDescription/dicom_image_description.csv"  # The path to dicom attributes file
DICOM_FILENAME_EXTENSION    = '.dcm'                                            # The extension of dicom file
RESULT_FILE_EXTENSION       = '.png'                                            # The extension of the result file
PATIENT_DETAILS_FILENAME    = 'Patient_Detail.csv'                              # The name of the result file with patient data

# The function gets folder path with dicom files and converts them to PNG
def convertDCM(folder_path):

    # Set path to the dicom images directory
    dicom_files_in_dir = os.listdir(folder_path)
    
    # Get only dicom files from the file list
    dicom_files_in_dir = list(filter(lambda file: file.endswith(DICOM_FILENAME_EXTENSION), dicom_files_in_dir))
    
    # Read all dicom data disription
    dicom_image_description = pd.read_csv(DICOM_DESCRIPTION_FILE_PATH)
    
    # Open the result csv file to write
    with open(os.path.join(folder_path, PATIENT_DETAILS_FILENAME), 'w', newline ='') as csvPatient:
        
        # Create a list of all descriptions in dicom images
        fieldnames = list(dicom_image_description["Description"])
        
        # Write the description to csv file with patient data
        writerPatient = csv.writer(csvPatient, delimiter=',')
        writerPatient.writerow(fieldnames)
        
        # Run over the dicom images
        for n, curImage in enumerate(dicom_files_in_dir):
            
            # Open dicom image
            dicomImg = dicom.dcmread(os.path.join(folder_path, curImage))
    
            # Initialize row data of the current image for patient data
            rows = []
            
            # Get the slope and interept from the dicom image
            slope = float(dicomImg.RescaleSlope)
            intercept = float(dicomImg.RescaleIntercept)
            
            # Rescale the pixels according to slope and intercept
            df_data = intercept + dicomImg.pixel_array.astype(float) * slope
            
            # Convert the image to tiff
            curImage = curImage.replace(DICOM_FILENAME_EXTENSION, RESULT_FILE_EXTENSION)
            
            # Convert the image from grayscale back to RGB
            stacked_img = np.stack((df_data,) * 3, axis=-1)
            
            # Wrtite the result image to file
            cv2.imwrite(os.path.join(folder_path, curImage), stacked_img)
                
            # Run over the fields
            for field in fieldnames:
                try:
                    # If the element is empty inside the current image
                    if dicomImg.data_element(field) is None:
                        rows.append('')
                    # The element exists in the dicom image - append it to the row of csv file
                    else:
                        x = str(dicomImg.data_element(field)).replace("'", "")
                        y = x.find(":")
                        x = x[y+2:]
                        rows.append(x)
                except KeyError as ke:
                    continue
            
            # Write patient data of the current image to the csv file
            writerPatient.writerow(rows)
            
#convertDCM("C:\\Users\\Aviel-PC\\Documents\\Final-Project\\Not in Git\\Dicom")