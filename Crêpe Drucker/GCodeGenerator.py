import math
import numpy as np

class GCodeGenerator:
    def __init__(self):
        pass
        
    def generateGCode(self, contour):
        numpyArray = self.contourToNumpy(contour)
        return self.numpyToGCode(numpyArray)

    def generateGCodeVectorized(self, contour):
        numpyArray = self.contourToNumpy(contour)
        if len(numpyArray) > 2:
            numpyArray = self.vectorFilter(numpyArray, 5)
        if len(numpyArray) > 2:
            numpyArray = self.angleFilter(numpyArray, 170)
        return self.numpyToGCode(numpyArray)

    def contourToNumpy(self, contour):
        array = []
        for point in contour:
            #print(point[0][0], ",",point[0][1], ";")
            array.append(np.array([point[0][0], point[0][1]]))
        return array
    
    def vectorFilter(self, numpyArray, minLength):
        new_numpy_array = []
        length = len(numpyArray)
        p0 = numpyArray[length - 1]
        for i in range(0, length):
            p1 = numpyArray[i]
            v = p1 - p0
            v_abs = np.linalg.norm(v)
            #print(p0)
            if v_abs >= minLength:
                new_numpy_array.append(p0)
                #print(p0)
                p0 = p1
        return new_numpy_array
            

    def angleFilter(self, numpyArray, angle):
        new_numpy_array = []
        length = len(numpyArray)
        p0 = numpyArray[length - 1]
        numpyArray.append(numpyArray[0])
        for i in range(0, length):
            p1 = numpyArray[i]
            p2 = numpyArray[i+1]
            u = p0 - p1
            v = p2 - p1
            skalar_prod = np.dot(u, v)
            u_abs = np.linalg.norm(u)
            v_abs = np.linalg.norm(v)
            eps = skalar_prod / (u_abs * v_abs)
            eps = round(eps, 7)
            alpha = math.degrees(math.acos(eps))
            #print("u ", u, "v ", v, "skalar ", skalar_prod, "uabs ", u_abs, "vabs ", v_abs, "Points: ", [p0, p1, p2], "eps ", eps, "alpha ", alpha)
            if alpha <= angle:
                new_numpy_array.append(p0)
                #print("u ", u, "v ", v, "skalar ", skalar_prod, "uabs ", u_abs, "vabs ", v_abs, "Points: ", [p0, p1, p2], "eps ", eps, "alpha ", alpha)
                #print(p0)
                p0 = p1
        return new_numpy_array

    def numpyToGCode(self, numpyArray):
        gcodes = []
        length = len(numpyArray)
        numpyArray.append(numpyArray[0])
        gcodes.append(f"G1 {numpyArray[0][0]} {numpyArray[0][1]}")
        gcodes.append("G2 1")
        gcodes.append("G3 500")
        for i in range(1, length+1):
            x = numpyArray[i][0]
            y = numpyArray[i][1]
            gcodes.append(f"G1 {x} {y}")
        gcodes.append("G2 0")
        gcodes.append("G3 500")
        return gcodes

