import numpy as np
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

illuminant = "d65"

def convert_lab_srgb(colores):
    sRGBs =  []
    for c in colores:
        lab = LabColor(*c,illuminant=illuminant,observer="2")
        srgb = convert_color(lab, sRGBColor,target_illuminant=illuminant)
        srgb = np.array((srgb.rgb_r,srgb.rgb_g,srgb.rgb_b))
        sRGBs.append(srgb)
    sRGBs = np.array(sRGBs)
    return sRGBs
def convert_srgb_to_lab(srgbs):
    labs = []
    for srgb in srgbs:
        color_srgb = sRGBColor(*srgb)
        color_lab = convert_color(color_srgb,LabColor,target_illuminant=illuminant)
        labs.append(np.array([color_lab.lab_l,color_lab.lab_a,color_lab.lab_b]))
    return np.array(labs)




def measure_final_error(predicted_lab, expected_lab):
    deltas = [] 

    for i in range(len(predicted_lab)):
        lab1 = LabColor(*predicted_lab[i],illuminant=illuminant,observer="2")
        lab2 = LabColor(*expected_lab[i],illuminant=illuminant,observer="2")
        delta = delta_e_cie2000(lab1,lab2)
        deltas.append(delta)
    return np.array(deltas)


if __name__ == "__main__":
    filename = "../referenceLab"
    coloresLab = np.loadtxt(filename,dtype=np.float32)

    initialLab = coloresLab.copy()



    passes = 10
    for i in range(passes):
        #  sum = np.average((coloresLab-initialLab)**2)
        print(np.mean(measure_final_error(initialLab, coloresLab)))
        #  print(initialLab[6],coloresLab[6])
        #  print(initialLab[7],coloresLab[7])
        #  print()
        coloresLab = convert_srgb_to_lab(convert_lab_srgb(coloresLab))
    
    #  diffSqr = (coloresLab - initialLab)**2
    #  big_err = diffSqr>.5
    #  for i in range(len(coloresLab)):
    #      if any(big_err[i]):
    #          lab1 = initialLab[i]
    #          lab2 = coloresLab[i]
    #          print(i)
    #          print(lab1,lab2)
    #          print(i,np.sum((lab1-lab2)**2))
    #          print()


