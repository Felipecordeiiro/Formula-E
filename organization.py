import os
import cv2 as cv
import numpy as np
from skimage import exposure
from PIL import Image

def pre_processing_images(url_dataset, path_save):
    imagens  = url_dataset

    #between -50% and +50%
    adjust_factor = np.random.uniform(*(0.5, 1.5))

    for image in imagens:
        
        #Auto-orientation with EXIF-autorientation
        image = Image.open(image)

        if "exif" in image.info:
            exif_data = image.info["exif"]
            orientation = None
            for tag, value  in exif_data.items():
               if tag == 0x0112:  # EXIF tag for orientation
                orientation = value
                break
        # Apply auto-orientation if orientation information is found
        if orientation is not None:
            if orientation == 1:
                # Normal (no rotation needed)
                pass
            elif orientation == 3:
                # Rotate 180 degrees
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                # Rotate 270 degrees
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                # Rotate 90 degrees
                image = image.rotate(90, expand=True)
        #applied the AHE
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        equalize_image = exposure.equalize.adapthist(gray_img)
        equalize_image_rgb = cv.cvtColor(equalize_image, cv.COLOR_GRAY2RGB)
        #applied the enhancement random exposure 
        np.clip(equalize_image_rgb * adjust_factor, 0, 255).astype(np.uint8)
        #resize the image for standard dataset
        cv.resize(equalize_image_rgb, (650,650))
        #Saving image
        cv.imwrite('imaage')

        