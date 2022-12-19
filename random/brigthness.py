import cv2
import numpy as np

img  = cv2.imread("../output/halogena.png")
original = img.copy()
original = original[:,37:1538]
img = img[1220:1229:,37:1538]
print(original.shape)
#  img = img[1150:1159:,:]
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.blur(img, (9,9))
img = cv2.blur(img, (9,9))

higher = np.max(img)
brightnesCorrecction = higher/img
brightnesCorrecction = np.mean(brightnesCorrecction,axis=0)
print(brightnesCorrecction.shape)

corr = np.zeros(original.shape[:2])
print(corr.shape)
for i in range(original.shape[0]):
    corr[i,:]=brightnesCorrecction

print(original.shape)
original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
original = original.astype(np.float32)
original[:,:,2] *=corr
original = original.astype(np.uint8)
original = cv2.cvtColor(original, cv2.COLOR_HSV2BGR)


cv2.imwrite("../input2/halogenas/a.png",original)
#  cv2.imshow("hola",original)
#  while True:
#      k = cv2.waitKey(100) & 0xFF
#      if k == 27:
#          break

