import cv2

def colorChckerDetection (img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    mask = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 1)
    cv2.imshow("",mask)

    while True:
        k = cv2.waitKey(100) & 0xFF
        if k == 27:
            break
if __name__ == "__main__":
    img = cv2.imread("./input6/halogenas/halogena.png")
    colorChckerDetection(img)
