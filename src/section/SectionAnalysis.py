from partial.PartialAnalysis import PartialAnalysis
from partial.RectangleAnalysis import RectangleAnalysis as RA
from partial.PolygonAnalysis import PolygonAnalysis as PA
from partial.CircSegAnalysis import CircSegAnalysis as CSA

import math
__author__ = 'Kim Nguyen'
class SectionAnalysis:
    ''' analyzes the cumulative list of sections '''
    def __init__(self, Pz, Mx, My, xP, yP, isSuppress):
        self._Pz = None
        self._Mx = None
        self._My = None
        self._xP = None
        self._yP = None
        self._isSuppress = False
        self._sectionArr = None
        self.Pz = Pz
        self.Mx = Mx
        self.My = My
        self.xP = xP
        self.yP = yP
        self.isSuppress = isSuppress
        self._sections = []
        self._xcg = 0
        self._ycg = 0
        self._areaTot = 0
        self._theta = 0
        self._thetaD = 0
        self._E = 0
        self._AE = 0

    @property
    def Pz(self):
        ''' Load in z direction '''
        return self._Pz

    @Pz.setter
    def Pz(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError('dimension must be a number')

        self._Pz = value

    @property
    def Mx(self):
        ''' Moment in x direction '''
        return self._Mx

    @Mx.setter
    def Mx(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError('dimension must be a number')

        self._Mx = value

    @property
    def My(self):
        ''' Moment in x direction '''
        return self._Mx

    @My.setter
    def My(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError('dimension must be a number')

        self._My = value

    @property
    def xP(self):
        ''' load point in x direction '''
        return self._xP

    @xP.setter
    def xP(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError('dimension must be a number')

        self._xP = value

    @property
    def yP(self):
        ''' load point in y direction '''
        return self._yP

    @yP.setter
    def yP(self, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError('dimension must be a number')

        self._yP = value
        
    @property
    def isSuppress(self):
        ''' load point in y direction '''
        return self._isSuppress

    @isSuppress.setter
    def isSuppress(self, value):
        try:
            value = bool(value)
        except ValueError:
            raise ValueError('suppression must be boolean')

        self._isSuppress = value

    @property
    def sectionArr(self):
        ''' section parts as array '''
        arr = [[] for i in range(len(self._sections))]
        for i in range(0, len(self._sections)):
            arr[i] = self._sections[i].getArr()
        self._sectionArr = arr
        return self._sectionArr

    @property
    def sections(self):
        return self._sections

    @property
    def xcg(self):
        self.calculateCG()
        return self._xcg

    @property
    def ycg(self):
        self.calculateCG()
        return self._ycg

    @property
    def areaTot(self):
        self.calculateCG()
        return self._areaTot

    @property
    def theta(self):
        ''' angle between the x axis and the principal axis in radians '''
        self.getIcg()
        return self._theta

    @property
    def thetaD(self):
        ''' angle between the x axis and the principal axis in degrees '''
        self.getIcg()
        return self._theta * 180 / math.pi
        
    @property
    def E(self):
        ''' Modulus of entire section '''
        return self._E
        
    @property
    def AE(self):
        ''' Modulus of entire section times entire section area '''
        return self._AE

    def calculateCG(self):
        ''' calculates the CG '''
        areaX = 0
        areaY = 0
        areaTot = 0
        self._E = 0
        self._AE = 0
        for section in self._sections:
            areaX += section.E * section.area * section.xcg
            areaY += section.E * section.area * section.ycg
            areaTot += section.area
            self._AE += section.E * section.area
        try:
            self._xcg = areaX / self._AE
            self._ycg = areaY / self._AE
            self._areaTot = areaTot
            self._E = self._AE / self._areaTot
        except ZeroDivisionError:
            self._xcg = 0
            self._ycg = 0
            self._areaTot = 0

    def addSection(self, pa):
        ''' adds a section pa to the list '''
        if isinstance(pa, PartialAnalysis):
            self._sections.append(pa)

    def removeSection(self, idx):
        ''' remvoes the section from the idx index '''
        if (idx >= 0 or idx < len(self._sections)):
            del self._sections[idx]

    def editSection(self, idx, e):
        ''' edits the section with the edit info '''
        if (idx < 0 or idx >= len(self._sections)):
            return

        if (e[0][0] is 'R' or e[0][0] is 'r'):
            self._sections[idx] = RA(e[1], e[2], e[3], e[4], e[5], e[6], e[7])
        elif (e[0][0] is 'C' or e[0][0] is 'c'):
            self._sections[idx] = CSA(e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
        else:
            self._sections[idx] = PA(e[1], e[2], e[3:])

    def getIcg(self):
        ''' gets the I about the CG un roated '''
        self.calculateCG()
        Ix = 0
        Iy = 0
        Ixy = 0
        
        for section in self._sections:
            Ixo, Iyo, Ixyo = section.getIo()
            Ix += section.E / self._E * Ixo
            Iy += section.E / self._E * Iyo
            Ixy += section.E / self._E * Ixyo
            
        Ixcg = Ix - self._areaTot * self._ycg ** 2
        Iycg = Iy - self._areaTot * self._xcg ** 2
        if self._isSuppress:
            Ixycg = 0
            self._theta = 0
        else:
            Ixycg = Ixy - self._areaTot * self._xcg * self._ycg
            try:
                self._theta = math.atan(2 * Ixycg / (Iycg - Ixcg)) / 2
            except ZeroDivisionError:
                self._theta = 45 * math.pi / 180
                if (Ixycg == 0):
                    self._theta = 0
        return Ixcg, Iycg, Ixycg

    def getIp(self):
        ''' gets the I about the principal axis (rotated) '''
        Ixcg, Iycg, Ixycg = self.getIcg()
        Ixp = (Ixcg * math.cos(self._theta) ** 2
               + Iycg * math.sin(self._theta) ** 2
               - 2 * Ixycg * math.sin(self.theta) * math.cos(self._theta))
        Iyp = (Ixcg * math.sin(self._theta) ** 2
               + Iycg * math.cos(self._theta) ** 2
               + 2 * Ixycg * math.sin(self._theta) * math.cos(self._theta))
        return Ixp, Iyp

    def getStress(self, index, x, y):
        ''' the stress at x , y '''
        try:
            index = int(index)
            x = float(x)
            y = float(y)
        except ValueError:
            raise ValueError('dimension must be a number')
        Ixp, Iyp = self.getIp()
        Pz = self._Pz
        Mx = (self._Mx - self._Pz * (self._ycg - self._yP))
        My = (self._My + self._Pz * (self._xcg - self._xP))
        Mxp = Mx * math.cos(self._theta) - My * math.sin(self._theta)
        Myp = Mx * math.sin(self._theta) + My * math.cos(self._theta)
        x = x - self._xcg
        y = y - self._ycg
        xp = x * math.cos(self._theta) + y * math.sin(self._theta)
        yp = -x * math.sin(self._theta) + y * math.cos(self._theta)
        EIx = self._E * Ixp
        EIy = self._E * Iyp
        try:
            if len(self._sections) != 0:
                sigma = self._sections[index].E * (Pz / self._AE - Mxp * yp / EIx - Myp * xp / EIy)
                return sigma
            else:
                raise ValueError('Nothing to analyze')
        except ZeroDivisionError:
            raise ValueError('Error during calculating stress, check section validity')
        
    def stressField(self):
        ''' entire stress field of part '''
        stressField = []
        maxS = float('-inf')
        minS = float('inf')
        maxI = 0
        minI = 0
        index = 0
        i = 0
        for section in self._sections:
            for c in section.corners():
                stress = self.getStress(i, c[0], c[1])
                stressField.append([c[0], c[1], stress])
                if (maxS < stress):
                    maxS = stress
                    maxI = index
                if (stress < minS):
                    minS = stress
                    minI = index
                index += 1
            for p in section.perimeter():
                stress = self.getStress(i, p[0], p[1])
                stressField.append([p[0], p[1], stress])
                if (maxS < stress):
                    maxS = stress
                    maxI = index
                if (stress < minS):
                    minS = stress
                    minI = index
                index += 1
            i += 1
        if minS == float('inf') or maxS == float('-inf'):
            minS = 0
            maxS = 1
        return stressField, minS, maxS, minI, maxI

    def clear(self):
        ''' clears all the sections'''
        del self._sections[:]
        
    def getMinMax(self):
        minX = float('inf')
        maxX = float('-inf')
        minY = float('inf')
        maxY = float('-inf')
        if len(self._sections) > 0:
            for section in self._sections:
                for c in section.corners():
                    minX = min(minX, c[0])
                    minY = min(minY, c[1])
                    maxX = max(maxX, c[0])
                    maxY = max(maxY, c[1])
                for p in section.perimeter():
                    minX = min(minX, p[0])
                    minY = min(minY, p[1])
                    maxX = max(maxX, p[0])
                    maxY = max(maxY, p[1])
                        
            return minX, minY, maxX, maxY
        else:
            return 0, 0, 0, 0
