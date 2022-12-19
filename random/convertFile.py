import numpy as np
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color

filename = "../referenceLab"
filename_out = "../referenceSRGB"
colores = np.loadtxt(filename,dtype=np.float32)
sRGBs =  []
for c in colores:
    lab = LabColor(*c,illuminant="d65",observer="2")
    srgb = convert_color(lab, sRGBColor,target_illuminant="d65")
    srgb = np.array((srgb.rgb_r,srgb.rgb_g,srgb.rgb_b))
    sRGBs.append(srgb)
sRGBs = np.array(sRGBs)
np.savetxt(filename_out,sRGBs,fmt='%1.3f')
