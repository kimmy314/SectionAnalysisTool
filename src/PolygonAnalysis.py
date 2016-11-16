from PartialAnalysis import PartialAnalysis
__author__ = 'Kim Nguyen'
class PolygonAnalysis(PartialAnalysis):
    '''
    Rectangle section analysis.
    dim1 - base of rectangle
    dim2 - height of rectangle
    orient - angle from x axis to line along height
    x - x coordinate of the bottom left corner of rectangle
    y - y coordinate of the bottom left corner of rectangle
    '''
    def __init__(self, name, coords):
        super(PolygonAnalysis, self).__init__(name, 0, 0, 0, 0, 0);
        self._coords = None;
        self._size = None;
        self.coords = coords;
        self.calculateSection();

    @property
    def coords(self):
        ''' orientation of the object '''
        return self._coords;

    @coords.setter
    def coords(self, value):
        if (len(value) % 2 != 0 or len(value) < 6):
            raise ValueError('must be an even number of inputs');
        try:
            for i in range(len(value)):
                value[i] = float(value[i]);
        except ValueError:
            raise ValueError('coords must be a number: {}'.format(value));

        self._size = int(len(value) / 2);
        self._coords = value;

    @property
    def size(self):
        ''' returns the number of points in the polygon '''
        return self._size;

    def getXY(self, idx):
        ''' gets the x and y position at the ith place '''
        coords = self.coords;
        idx = idx % self.size;
        x = coords[idx * 2];
        y = coords[idx * 2 + 1];
        return x, y
    def calculateArea(self):
        area = 0;
        for i in range(self.size):
            x,y = self.getXY(i);
            xp, yp = self.getXY(i + 1);
            area += (x * yp - xp * y);
        self._area = area / 2;

    def calculateCG(self):
        self.calculateArea();
        if self._area == 0:
            raise ValueError('polygon has a 0 area');
            return;

        xcg = 0;
        ycg = 0;
        for i in range(self.size):
            x,y = self.getXY(i);
            xp, yp = self.getXY(i + 1);
            xcg += ((x + xp) * (x * yp - xp * y));
            ycg += ((y + yp) * (x * yp - xp * y));
        self._xcg = xcg / 6 / self._area;
        self._ycg = ycg / 6 / self._area;

    def calculateI(self):
        self._Ix = 0;
        self._Iy = 0;

    def calculateIc(self):
        self._Ixc = 0;
        self._Iyc = 0;
        self._Ixyc = 0;

    def getIo(self):
        Ix = 0;
        Iy = 0;
        Ixy = 0;
        for i in range(self.size + 1):
            x,y = self.getXY(i);
            xp, yp = self.getXY((i + 1));
            Ix += ((y**2 + y * yp + yp**2) * (x * yp - xp * y));
            Iy += ((x**2 + x * xp + xp**2) * (x * yp - xp * y));
            Ixy += ((x * yp + 2 * x * y + 2 * xp * yp + xp * y)
                    * (x * yp - xp * y));
        return Ix / 12, Iy / 12, Ixy / 24;

    def getArr(self):
        return (self.name, 'P', 'O',
                'L', 'Y', '', '');

    def getMinMax(self):
        maxC = 0;
        minC = 0;
        for i in range(self.size):
            x,y = self.getXY(i);
            maxC = max(maxC, max(x, y));
            minC = min(minC, min(x, y))
        return maxC, minC;

    def corners(self):
        c = [[0 for j in range(2)] for i in range(self.size)];
        for i in range(self.size):
            c[i][0] = self.coords[i * 2];
            c[i][1] = self.coords[i * 2 + 1];
        return c;

    def perimeter(self):
        c = self.corners();
        pps = self.pps;
        p = [[0 for j in range(2)] for i in range(pps * self.size)];
        for i in range (self.size):
            for j in range (pps):
                ip = (i + 1) % self.size;
                blend = (j + 1) / (pps + 1);
                p[i * pps + j][0] = c[i][0] + blend * (c[ip][0] - c[i][0]);
                p[i * pps + j][1] = c[i][1] + blend * (c[ip][1] - c[i][1]);

        return p;