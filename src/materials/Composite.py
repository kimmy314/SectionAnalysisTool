'''
Created on Nov 23, 2016

@author: ra029440
'''
from materials.Material import Material

class Composite(Material):
    '''
    creates a composite material
    '''

    def __init__(self, ply):
        '''
        constructors a composite material with ply number of plies
        '''
        self._ply = 0
        self._plies = []
        self.ply = ply
        
    @property
    def ply(self):
        ''' number of plies '''
        return self._ply

    @ply.setter
    def ply(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError('ply must be an integer')

        if (value < 0):
            raise ValueError('ply must be greater than or equal to 0')

        self._ply = value;
        if len(self._plies) == 0:
            self._plies = [Ply() for i in range(value)]
        else:
            if (value < len(self._plies)):
                self._plies = self._plies[:value]
            else:
                for i in range(len(self._plies), value):
                    self._plies.append(Ply())
        
    def setPlyAngle(self, index, angle):
        self.plies[index].angle = angle
        
    def setPlyE(self, index, E):
        self.plies[index].E = E
        
    def rotateMatrix(self, angle):
        for ply in self.plies:
            ply.angle = ply.angle + angle
            
    def calculateA(self):
        
        return 0
        
class Ply:
    def __init__(self):
        '''
        constructors a ply with modulus E with angle
        '''
        self._E1 = 0
        self._E2 = 0
        self._G = 0
        self._nu = .33
        self._angle = 0
        
    @property
    def angle(self):
        ''' dimension 1 '''
        return self._angle;

    @angle.setter
    def angle(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('angle must be an number');

        self._angle = value;
        
    @property
    def E1(self):
        ''' modulus '''
        return self._E1;

    @E1.setter
    def E1(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('modulus must be an number');

        if (value < 0):
            raise ValueError('modulus must be greater than or equal to 0');

        self._E1 = value;
            
    @property
    def E2(self):
        ''' modulus '''
        return self._E2;

    @E2.setter
    def E2(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('modulus must be an number');

        if (value < 0):
            raise ValueError('modulus must be greater than or equal to 0');

        self._E2 = value;
        
    @property
    def nu(self):
        ''' poisson's ratio '''
        return self._nu;

    @nu.setter
    def nu(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('modulus must be an number');

        if (value < 0):
            raise ValueError('modulus must be greater than or equal to 0');

        self._nu = value;
        
    @property
    def G(self):
        ''' shear modulus '''
        return self._G;

    @G.setter
    def G(self, value):
        try:
            value = float(value);
        except ValueError:
            raise ValueError('modulus must be an number');

        if (value < 0):
            raise ValueError('modulus must be greater than or equal to 0');

        self._G = value;
        
        