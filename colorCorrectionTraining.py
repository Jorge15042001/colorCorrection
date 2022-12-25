import numpy as np
import cv2
import CA as ca

    
if __name__  == "__main__":

    x_Holagena = np.loadtxt("./output/halogenas",dtype=np.float32)
    x_Led = np.loadtxt("./output/leds",dtype=np.float32)
    x_HaloLed = np.loadtxt("./output/haloleds",dtype=np.float32)
    expected = np.loadtxt("./referenceSRGB",dtype=np.float32)

    lccHalogena = ca.LCC(x_Holagena, expected, "Halogena")
    lccLed = ca.LCC(x_Led, expected, "Led")
    lccHaloled = ca.LCC(x_HaloLed, expected, "Haloled")

    lccHalogena.showError(x_Holagena,expected)
    lccLed.showError(x_Led,expected)
    lccHaloled.showError(x_HaloLed, expected)
    print()

    pcc_halogena = ca.PCC(x_Holagena,expected,"Halogena")
    pcc_led = ca.PCC(x_Led,expected,"Led")
    pcc_haloled = ca.PCC(x_HaloLed,expected,"Haloleds")

    pcc_halogena.showError(x_Holagena,expected)
    pcc_led.showError(x_Led,expected)
    pcc_haloled.showError(x_HaloLed, expected)
    print()

    rpcc_halogena = ca.RPCC(x_Holagena,expected,"Halogena")
    rpcc_led = ca.RPCC(x_Led,expected,"Led")
    rpcc_haloled = ca.RPCC(x_HaloLed,expected,"Haloleds")
    
    rpcc_halogena.showError(x_Holagena, expected)
    rpcc_led.showError(x_Led, expected)
    rpcc_haloled.showError(x_HaloLed, expected)
    print()

    svrcc_halogena = ca.SVRCC(x_Holagena,expected,"Halogena")
    svrcc_led = ca.SVRCC(x_Led,expected,"Led")
    svrcc_haloled = ca.SVRCC(x_HaloLed,expected,"Haloleds")

    svrcc_halogena.showError(x_Holagena, expected)
    svrcc_led.showError(x_Led, expected)
    svrcc_haloled.showError(x_HaloLed, expected)
    print()

    tarjetaCorr = cv2.imread("random/test/halogenas.png")
    tarjetareff = cv2.imread("random/test/reference.png")
    tarjetaCorr = cv2.imread("random/test/franjas2.png")
    #  tarjetaCorr = cv2.imread("./input6/leds/led.png")
    #  tarjetaCorr = cv2.blur(tarjetaCorr,(3,3))
    tarjeta = tarjetaCorr.copy()
    tarjetaCorr = cv2.cvtColor(tarjetaCorr, cv2.COLOR_BGR2RGB)
    #  tarjetaCorr = cv2.GaussianBlur(tarjetaCorr,(101,101),0,0)
    #  tarjetaCorr = cv2.blur(tarjetaCorr,(101,101))
    tarjetaCorr = tarjetaCorr/255
    tarjetaCorr = lccLed.correctImage(tarjetaCorr)
    tarjetaCorr = (tarjetaCorr * 255).astype(np.uint8)
    tarjetaCorr = cv2.cvtColor(tarjetaCorr, cv2.COLOR_RGB2BGR)

    cv2.imshow("corr",tarjetaCorr)
    cv2.imshow("origial",tarjeta)
    cv2.imshow("ref",tarjetareff)
    
    while True:
        k = cv2.waitKey(100) & 0xFF
        if k == 27:
            break
