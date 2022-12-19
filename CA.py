from abc import ABC,abstractmethod
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import numpy as np
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

#  import colour.difference.delta_e
#  from colour.difference import delta_E_CIE2000
import colour


illuminant = "d65"
observer = "2"


def convert_srgb_to_lab(srgbs):
    labs = []
    for srgb in srgbs:
        color_srgb = sRGBColor(*srgb)
        color_lab = convert_color(color_srgb,LabColor,target_illuminant=illuminant)
        labs.append(np.array([color_lab.lab_l,color_lab.lab_a,color_lab.lab_b]))
    return np.array(labs)


def measure_final_error(predicted, expected):
    predicted_lab = convert_srgb_to_lab(predicted)
    expected_lab = convert_srgb_to_lab(expected)
    #  expected_lab = np.loadtxt("referenceLab")
    deltas = []
    for i in range(len(predicted_lab)):
        lab1 = LabColor(*predicted_lab[i],illuminant=illuminant,observer="2")
        lab2 = LabColor(*expected_lab[i],illuminant=illuminant,observer="2")
        delta = delta_e_cie2000(lab1,lab2)
        deltas.append(delta)
    return np.mean(deltas)


class CorrectioAlgoritm(ABC):
    @abstractmethod
    def predict(self,x):pass
    def showError(self, x,expected):
        finalError = measure_final_error(self.predict(x),expected)
        print("{:10} {:10} {:10} {:6.3f}".format(self.id,type(self).__name__,"error:",finalError))
    def correctImage(self,img):

        corrected = np.zeros(img.shape)
        for i,r in enumerate(img):
            corrected [i]= self.predict(r)
        corrected = np.clip(corrected,0.,1.)
        #  corrected=(corrected-np.min(corrected))/(np.max(corrected)-np.min(corrected))
        return corrected


class LCC (CorrectioAlgoritm):
    def __init__(self,x,y,id):
        self.id = id

        model = LinearRegression()
        model.fit(x, y)
        self.model = model


    def predict(self,x):
        return self.model.predict(x)
            


class SVRCC(CorrectioAlgoritm):
    def __init__(self, x,y,id):
        self.id = id
        

        modelR = SVR(epsilon=0.001)
        modelG = SVR(epsilon=0.001)
        modelB = SVR(epsilon=0.001)

        modelR.fit(x, y[:,0])
        modelG.fit(x, y[:,1])
        modelB.fit(x, y[:,2])

        self.modelR = modelR
        self.modelB = modelB
        self.modelG = modelG

    def predict(self,x):

        predictedR = self.modelR.predict(x)
        predictedG = self.modelG.predict(x)
        predictedB = self.modelB.predict(x)

        predictions = []
        for i in range(len(predictedR)):
            predictions.append(np.array([predictedR[i],predictedG[i],predictedB[i]]))
        predictions = np.array(predictions)

        return predictions



class RPCC(CorrectioAlgoritm):
    def __init__(self,x,y,id):
        self.id = id
        self.y = y
        self.x = x
        
    def predict(self, x):
        predicted = colour.colour_correction(x,self.x,self.y, "Finlayson 2015",degree=2)
        return predicted

        
class PCC(CorrectioAlgoritm):
    def __init__(self,x,y,id):
        self.id = id
        x_ = PolynomialFeatures(degree=2, include_bias=True).fit_transform(x)
        self.model = LinearRegression().fit(x_, y)
    def predict(self, x):
        x_ = PolynomialFeatures(degree=2, include_bias=True).fit_transform(x)
        predicted = self.model.predict(x_)
        return predicted
        



