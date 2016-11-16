import math;
from PartialAnalysis import PartialAnalysis
__author__ = Kim Nguyen, kbnguyen@ncsu.edu
class CircSegAnalysis(PartialAnalysis):
    '''
    Circle segment section analysis.
    dim1 - Radius of outter circle
    dim2 - Radius of inner circle
    orient - angle from x axis to line along height
    x - x coordinate of the bottom left corner of rectangle
    y - y coordinate of the bottom left corner of rectangle
    '''
    def __init__(self, name, x, y, dim1, dim2, orient, alpha):
        super(CircSegAnalysis, self).__init__(name, x, y, dim1, dim2, orient);
        self._alpha = None;
        self._alphaD = None;
        self.alpha = alpha;
        self._areaOut = 0;
        self._areaIn = 0;
        self.calculateSection();

    @property
    def alpha(self):
        ''' orientation of the object '''
        return self._alpha;

    @alpha.setter
    def alpha(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');
        self._alphaD = value;
        self._alpha = value * math.pi / 180;

    def calculateArea(self):
        self._areaOut = self.alpha / 2 * self.dim1**2;
        self._areaIn = self.alpha / 2 * self.dim2**2;
        self._area = self._areaOut - self._areaIn;

    def _calculateCircCG(self, r):
        xccg = self.x + (2 * r * math.sin(self.alpha / 2) * math.cos(self.orient) / (3 * self.alpha / 2));
        yccg = self.y + (2 * r * math.sin(self.alpha / 2) * math.sin(self.orient) / (3 * self.alpha / 2));
        return xccg, yccg;

    def calculateCG(self):
        xocg, yocg = self._calculateCircCG(self.dim1);
        xicg, yicg = self._calculateCircCG(self.dim2);
        try:
            self._xcg = (xocg * self._areaOut - xicg * self._areaIn) / self._area;
            self._ycg = (yocg * self._areaOut - yicg * self._areaIn) / self._area;
        except ZeroDivisionError:
            self._xcg = 0;
            self._ycg = 0;
            
    def calculateI(self):
        try:
            self._Ix = ((self.dim1**4 - (self.dim2)**4) / 4
           * (self.alpha / 2 - math.sin(self.alpha / 2)
           * math.cos(self.alpha / 2)));
        except ZeroDivisionError:
            self._Ix = 0;
        try:
            self._Iy = ((self.dim1**4 - (self.dim2)**4) / 4
            * (self.alpha / 2 + math.sin(self.alpha / 2)
            * math.cos(self.alpha / 2))
            - self._area * (2 / 3 * math.sin(self.alpha / 2)
            * (self.dim1**3 - (self.dim2)**3)
            / ((self.alpha / 2) * (self.dim1**2 - (self.dim2)**2)))**2);
        except ZeroDivisionError:
            self._Iy = 0;
            
    def getArr(self):
        return (self.name, self._x, self._y,
                self._dim1, self._dim2, self._orientD, self._alphaD);


    def getMinMax(self):
        return ((max(self.x, self.y) + self.dim1),
                (min(self.x, self.y) - self.dim1));

    def corners(self):
        x, y, d1, d2, o, a = self.x, self.y, self.dim1, self.dim2, self.orient, self.alpha;
        c = [[0 for j in range(2)] for i in range(4)];
        c[0] = [x + d1 * math.cos(o - a / 2), y + d1 * math.sin(o - a / 2)];
        c[1] = [x + d1 * math.cos(o + a / 2), y + d1 * math.sin(o + a / 2)];
        c[2] = [x + d2 * math.cos(o + a / 2), y + d2 * math.sin(o + a / 2)];
        c[3] = [x + d2 * math.cos(o - a / 2), y + d2 * math.sin(o - a / 2)];
        return c;

    def perimeter(self):
        x, y, d1, d2, o, a = self.x, self.y, self.dim1, self.dim2, self.orient, self.alpha;
        c = self.corners();
        pps = self.pps;
        p = [[0 for j in range(2)] for i in range(pps * 4)];
        for i in [1, 3]:
            for j in range (pps):
                ip = (i + 1) % 4;
                blend = (j + 1) / (pps + 1);
                p[i * pps + j][0] = c[i][0] + blend * (c[ip][0] - c[i][0]);
                p[i * pps + j][1] = c[i][1] + blend * (c[ip][1] - c[i][1]);

        for i in [0]:
            for j in range (pps):
                angle = (o - a / 2) + a * (j + 1) / (pps + 1)
                p[i * pps + j] = [x + d1 * math.cos(angle), y + d1 * math.sin(angle)];

        for i in [2]:
            for j in range (pps):
                angle = (o + a / 2) - a * (j + 1) / (pps + 1)
                p[i * pps + j] = [x + d2 * math.cos(angle), y + d2 * math.sin(angle)];

        return p;