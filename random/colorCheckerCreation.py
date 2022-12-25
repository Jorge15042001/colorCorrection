import cv2
import numpy as np
from os import path

def createColorChecker(name:str):
    filePath = path.join("../output",name)
    if name== "reference": filePath = "../referenceSRGB"
    #  path = f'/home/jorge1504/projects/colorCorrection/output/{name}'
    colors = (np.loadtxt(filePath).astype(np.float32)*255)
    colors = np.clip(colors,0,255)
    colors = colors.astype(np.uint8)[:,::-1]

    width = 200

    shape = np.array([6,3])*width
    shape = shape[::-1]

    colorChecker = np.zeros((*shape,3),np.uint8)

    for i in range(len(colors)):
        c = (i%6)*width 
        r = (i//6)*width

        colorChecker[r:r+width,c:c+width,:]= colors[i]

    cv2.imwrite(path.join("./test",name+".png"),colorChecker)


createColorChecker("halogenas")
createColorChecker("leds")
createColorChecker("haloleds")
createColorChecker("reference")

#  while True:
#      k = cv2.waitKey(100) & 0xFF
#      if k == 27:
#          break
