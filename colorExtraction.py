import cv2
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
from time import sleep

import colour

from colour_checker_detection import (
    colour_checkers_coordinates_segmentation,
    detect_colour_checkers_segmentation)
from colour_checker_detection.detection.segmentation import (
    adjust_image)

settings = {
        "adaptive_threshold_kwargs": {
            "maxValue": 255,
            "adaptiveMethod": cv2.ADAPTIVE_THRESH_MEAN_C,
            "thresholdType": cv2.THRESH_BINARY,
            "blockSize": int(1440 * 0.015) - int(1440 * 0.015) % 2 + 1,
            "C": 10   ,
        }
    }

def findColors(images,settings=dict()):
    for image,path in images:
        print(np.max(image),np.min(image))
        #  imagecv = (image*255).astype(np.uint8)[:,:,::-1]
        #  imagecv = cv2.medianBlur(imagecv,1)
        #  cv2.imshow("",imagecv)
        #  cv2.imshow("blured",imagecv2)
        #
        #  while True:
        #      k = cv2.waitKey(100) & 0xFF
        #      if k == 27:
        #          break
        #  image=(imagecv/255).astype(np.float64)[:,:,::-1]
        result = colour_checkers_coordinates_segmentation(image,additional_data=True)
        print(len(result.swatches))
        #  colour.plotting.plot_image( colour.cctf_encoding(segmented))

        for colour_checker_swatches_data in detect_colour_checkers_segmentation( image, additional_data=True, samples=25,**settings):
            print(path)
            swatch_colours, colour_checker_image, swatch_masks = ( colour_checker_swatches_data.values)
            #  masks_i = np.zeros(colour_checker_image.shape)
            #  for i, mask in enumerate(swatch_masks):
            #      masks_i[mask[0]:mask[1], mask[2]:mask[3], ...] = 1
            #  colour.plotting.plot_image(
            #      colour.cctf_encoding(
            #          np.clip(colour_checker_image + masks_i * 0.25, 0, 1)))
            return np.array(swatch_colours[:18])


#  path_images_halogena = glob.glob( os.path.join('./input8', 'halogenas',"*"))
path_images_halogena = list(glob.glob( os.path.join('/home/jorge1504/Downloads', 'luzNormal.jpeg')))
path_images_led = glob.glob( os.path.join('./input8', 'leds',"*"))
path_images_haloled = glob.glob( os.path.join('./input8', 'haloleds',"*"))

imagenes_halogenas = [ (colour.io.read_image(path),path) for path in path_images_halogena ]
imagenes_leds = [ (colour.io.read_image(path),path) for path in path_images_led ]
imagenes_haloleds = [ (colour.io.read_image(path),path) for path in path_images_haloled ]


Lab_tarjeta_halogena = findColors(imagenes_halogenas,settings)
Lab_tarjeta_led = findColors(imagenes_leds)
Lab_tarjeta_haloled = findColors(imagenes_haloleds)

np.savetxt("output/halogenas", Lab_tarjeta_halogena,fmt='%1.7f')
np.savetxt("output/leds", Lab_tarjeta_led,fmt='%1.7f')
np.savetxt("output/haloleds", Lab_tarjeta_haloled,fmt='%1.7f')
