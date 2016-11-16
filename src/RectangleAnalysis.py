import math;
from PartialAnalysis import PartialAnalysis
__author__ = 'RA029440 - Kim_Nguyen@haci.honda.com'
class RectangleAnalysis(PartialAnalysis):
    '''
    Rectangle section analysis.
    dim1 - base of rectangle
    dim2 - height of rectangle
    orient - angle from x axis to line along height
    x - x coordinate of the bottom left corner of rectangle
    y - y coordinate of the bottom left corner of rectangle
    '''
    def __init__(self, name, x, y, dim1, dim2, orient):
        super(RectangleAnalysis, self).__init__(name, x, y, dim1, dim2, orient);
        self.calculateSection();

    def calculateArea(self):
        self._area = self.dim1 * self.dim2;

    def calculateCG(self):
        self._xcg = (self.x
                    + self.dim1 / 2 * math.cos(self.orient)
                    - self.dim2 / 2 * math.sin(self.orient));
        self._ycg = (self.y
                    + self.dim1 / 2 * math.sin(self.orient)
                    + self.dim2 / 2 * math.cos(self.orient));

    def calculateI(self):
        self._Ix = 1 / 12 * self.dim1 * self.dim2**3;
        self._Iy = 1 / 12 * self.dim1**3 * self.dim2;

    def getArr(self):
        return (self.name, self._x, self._y,
                self._dim1, self._dim2, self._orient, '');

    def getMinMax(self):
        return (max(self.x, self.y) + max(self.dim1, self.dim2),
                min(self.x, self.y));

    def corners(self):
        x, y, d1, d2, o = self.x, self.y, self.dim1, self.dim2, self.orient;
        c = [[0 for j in range(2)] for i in range(4)];
        c[0] = [x, y];
        c[1] = [x + d1 * math.cos(o), y + d1 * math.sin(o)];
        c[2] = [c[1][0] - d2 * math.sin(o), c[1][1] + d2 * math.cos(o)];
        c[3] = [x - d2 * math.sin(o), y + d2 * math.cos(o)];
        return c;

    def perimeter(self):
        c = self.corners();
        pps = self.pps;
        p = [[0 for j in range(2)] for i in range(pps * 4)];
        for i in range (4):
            for j in range (pps):
                ip = (i + 1) % 4;
                blend = (j + 1) / (pps + 1);
                p[i * pps + j][0] = c[i][0] + blend * (c[ip][0] - c[i][0]);
                p[i * pps + j][1] = c[i][1] + blend * (c[ip][1] - c[i][1]);

        return p;