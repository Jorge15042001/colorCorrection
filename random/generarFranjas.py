
import cv2
import numpy as np
from os import path

def createFranjas():
    width = 400

    shape = np.array([3,1])*width
    shape = shape[::-1]

    colorChecker = np.zeros((*shape,3),np.uint8)

    gradiente = np.round(np.linspace(0., 1.,shape[1])*255).astype(np.uint8)
    
    colorChecker[0:width//3,:,0]=gradiente
    colorChecker[width//3:2*width//3,:,1]=gradiente
    colorChecker[2*width//3:,:,2]=gradiente

    #  cv2.imshow("",colorChecker)


    cv2.imwrite(path.join("./test/franjas.png"),colorChecker)
def createFranjasAnidadas():
    width = 400

    shape = np.array([3,1])*width
    shape = shape[::-1]

    colorChecker = np.zeros((*shape,3),np.uint8)

    gradiente = np.round(np.linspace(0., 1.,shape[1])*255).astype(np.uint8)
    for i in range(3):
        step = width//3
        colorChecker[i*step:(i+1)*step,:,i]=gradiente
        for j in range(3):
            step2 = step//3
            colorChecker[i*step+j*step2:i*step+(j+1)*step2,:,j]=gradiente
            for k in range(3):
                step3 = step2//3
                colorChecker[i*step+j*step2+k*step3:i*step+j*step2+(k+1)*step3,:,k]=gradiente

    
    colorChecker[0:width//3,:,0]=gradiente
    colorChecker[width//3:2*width//3,:,1]=gradiente
    colorChecker[2*width//3:,:,2]=gradiente

    #  cv2.imshow("",colorChecker)


    cv2.imwrite(path.join("./test/franjas2.png"),colorChecker)


#  createFranjas()
createFranjasAnidadas()

#  while True:
#      k = cv2.waitKey(100) & 0xFF
#      if k == 27:
#          break
