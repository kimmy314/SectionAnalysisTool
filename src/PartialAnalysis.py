import math;
__author__ = 'Kim Nguyen'
class PartialAnalysis:
    '''
    Parent class for all section analysis
    '''
    pps = 7; # number of points per segment
    def __init__(self, name, E, x, y, dim1, dim2, orient):
        '''
        name - name/id of the section
        x - x coordinate position of section
        y - y coordinate position of section
        dim1 - dimension 1 of the section
        dim2 - dimension 2 of the section
        orient - orientation of the section
        '''
        self.name = name;
        self._dim1 = None;
        self._dim2 = None;
        self._orient = None;
        self._orientD = None;
        self._x = None;
        self._y = None;
        self._E = None;
        self.dim1 = dim1;
        self.dim2 = dim2;
        self.orient = orient;
        self.x = x;
        self.y = y;
        self.E = E;
        self._area = 0;
        self._xcg = 0;
        self._ycg = 0;
        self._Ix = 0;
        self._Iy = 0;
        self._Ixc = 0;
        self._Iyc = 0;
        self._Ixyc = 0;

    @property
    def dim1(self):
        ''' dimension 1 '''
        return self._dim1;

    @dim1.setter
    def dim1(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');

        if (value < 0):
            raise ValueError('dimension must be greater than or equal to 0');

        self._dim1 = value;

    @property
    def dim2(self):
        ''' dimension 2 '''
        return self._dim2;

    @dim2.setter
    def dim2(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');
        if (value < 0):
            raise ValueError('dimension must be greater than or equal to 0')

        self._dim2 = value;

    @property
    def orient(self):
        ''' orientation of the object '''
        return self._orient;

    @orient.setter
    def orient(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');
        self._orientD = value;
        self._orient = value * math.pi / 180;

    @property
    def x(self):
        ''' x coordinate'''
        return self._x;

    @x.setter
    def x(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');

        self._x = value;

    @property
    def y(self):
        ''' y coordinate'''
        return self._y;

    @y.setter
    def y(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');

        self._y = value;

    @property
    def area(self):
        self.calculateArea();
        return self._area;

    @property
    def xcg(self):
        self.calculateCG();
        return self._xcg;

    @property
    def ycg(self):
        self.calculateCG();
        return self._ycg;

    @property
    def Ix(self):
        self.calculateI();
        return self._Ix;

    @property
    def Iy(self):
        self.calculateI();
        return self._Iy;

    @property
    def Ixc(self):
        self.calculateIc();
        return self._Ixc;

    @property
    def Iyc(self):
        self.calculateIc();
        return self._Iyc;

    @property
    def Ixyc(self):
        self.calculateIc();
        return self._Ixyc;
        
    @property
    def E(self):
        ''' dimension 1 '''
        return self._E;

    @E.setter
    def E(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('dimension must be a number');

        if (value < 0):
            raise ValueError('dimension must be greater than or equal to 0');

        self._E = value;

    def calculateArea(self):
        '''
        calculates the area of the section
        '''
        raise NotImplementedError( "Should have implemented this" );

    def calculateCG(self):
        '''
        calculates the cg of section
        '''
        raise NotImplementedError( "Should have implemented this" );

    def calculateI(self):
        '''
        calculates the segment inertias (not inclined)
        '''
        raise NotImplementedError( "Should have implemented this" );

    def getArr(self):
        '''
        gets the array for gui display
        '''
        raise NotImplementedError( "Should have implemented this" );

    def getMinMax(self):
        '''
        gets the min max of the x/y values
        '''
        raise NotImplementedError( "Should have implemented this" );

    def corners(self):
        '''
        gets the corners of the shape
        '''
        raise NotImplementedError( "Should have implemented this" );

    def perimeter(self):
        '''
        gets the perimeter of the shape
        '''
        raise NotImplementedError( "Should have implemented this" );

    def calculateIc(self):
        '''
        calculates the segment inertias (inclined axis)
        '''
        self._Ixc = self._Ix * math.cos(self._orient)**2 + self._Iy * math.sin(self._orient)**2;
        self._Iyc = self._Ix * math.sin(self._orient)**2 + self._Iy * math.cos(self._orient)**2;
        self._Ixyc = - (self._Ix - self._Iy) * math.sin(2 * self._orient) / 2;

    def calculateSection(self):
        self.calculateArea();
        self.calculateCG();
        self.calculateI();
        self.calculateIc();

    def getIo(self):
        '''
        calculates and returns the MOI about the origin
        '''
        self.calculateSection();
        Ixo = self._Ixc + self._area * self._ycg**2;
        Iyo = self._Iyc + self._area * self._xcg**2;
        Ixyo = self._Ixyc + self._area * self._xcg * self._ycg;
        return Ixo, Iyo, Ixyo;
