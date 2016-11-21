'''
Created on Nov 21, 2016

@author: ra029440
'''
import unittest
from section.SectionAnalysis import SectionAnalysis as SA
from partial.RectangleAnalysis import RectangleAnalysis as RA
class Test(unittest.TestCase):
    
    def setUp(self):
        self.ra = [0 for i in range(4)]
        self.ra[0] = RA('R1',2,0,0,1,1,0);
        self.ra[1] = RA('R2',2,-1,0,1,1,0);
        self.ra[2] = RA('R3',2,-1,-1,1,1,0);
        self.ra[3] = RA('R4',1,0,-1,1,1,0);
        
        self.sa = SA(0, 300, 0, 0, 0)
        for i in range(4):
            self.sa.addSection(self.ra[i])
        
    def testRectIo(self):
        ixy = [.25, -.25, .25, -.25]
        for i in range(4):
            self.assertTrue(abs(self.ra[i].getIo()[0] - .33333) < .001, 'Actual: {}, Expected: {}'.format(self.ra[i].getIo()[0], .333))
            self.assertTrue(abs(self.ra[i].getIo()[1] - .33333) < .001, 'Actual: {}, Expected: {}'.format(self.ra[i].getIo()[1], .333))
            self.assertTrue(abs(self.ra[i].getIo()[2] - ixy[i]) < .001, 'Actual: {}, Expected: {}'.format(self.ra[i].getIo()[2], ixy[i]))

    def testSaCG(self):
        cg = .5 / 7
        self.assertTrue(abs(self.sa.xcg + cg) < .001, 'Actual: {}, Expected: {}'.format(self.sa.xcg, -cg))
        self.assertTrue(abs(self.sa.ycg - cg) < .001, 'Actual: {}, Expected: {}'.format(self.sa.ycg, cg))
        
    def testSaIcg(self):
        cg = .5/7
        Io = 4/3
        A = 4
        Icg = Io - A * cg**2
        Ixycg = .25 * 4 / 7 + A * cg**2
        self.assertTrue(abs(self.sa.getIcg()[0] - Icg) < .001, 'Actual: {}, Expected: {}'.format(self.sa.getIcg()[0], Icg))
        self.assertTrue(abs(self.sa.getIcg()[1] - Icg) < .001, 'Actual: {}, Expected: {}'.format(self.sa.getIcg()[1], Icg))
        self.assertTrue(abs(self.sa.getIcg()[2] - Ixycg) < .001, 'Actual: {}, Expected: {}'.format(self.sa.getIcg()[2], Ixycg))
        
    def testSaIp(self):
        self.assertTrue(abs(self.sa.getIp()[0] - 1.1497) < .001, 'Actual: {}, Expected: {}'.format(self.sa.getIp()[0], 1.1497))
        self.assertTrue(abs(self.sa.getIp()[1] - 1.4762) < .001, 'Actual: {}, Expected: {}'.format(self.sa.getIp()[1], 1.4762))
        
    def testSaStress(self):
        self.assertTrue(abs(self.sa.getStress(0, self.sa.xcg, self.sa.ycg)) < .001, 
                        'Actual: {}, Expected: {}'.format(self.sa.getStress(0, self.sa.xcg, self.sa.ycg), 0))
        self.assertTrue(abs(self.sa.getStress(0, -1, 1) + 276.7414) < 1, 
                        'Actual: {}, Expected: {}'.format(self.sa.getStress(0, -1, 1), -276.913))
        self.assertTrue(abs(self.sa.getStress(3, 1, -1) - 159.7577) < 1, 
                        'Actual: {}, Expected: {}'.format(self.sa.getStress(0, 1, -1), 159.7577))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()