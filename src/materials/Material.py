'''
Created on Nov 23, 2016

@author: Kim Nguyen
'''

class Material:
    '''
    parent class, contains basic information such as E, F
    '''
    alloy=spec=form=condition=thickness=basis=""
    FtuL=FtuLT=FtyL=FtyLT=FcyL=FcyLT=FsuL=FsuLT=FbruL=FbruLT=0
    eL=eLT=eST=E=Ec=G=mu=w=0
        
    def getMaterialDB(self, matfile):
        inp = open(matfile,"r")
    
        matArray = []
    
        for line in inp:
            m = Material()
            buff = line.strip().split("|")
            m.alloy = buff[0]
            m.spec = buff[1]
            m.form = buff[2]
            m.condition = buff[3]
            m.thickness = buff[4]
            m.basis = buff[5]
            m.FtuL = buff[6]
            m.FtuLT = buff[7]
            m.FtyL = buff[8]
            m.FtyLT = buff[9]
            m.FcyL = buff[10]
            m.FcyLT = buff[11]
            m.FsuL = buff[12]
            m.FsuLT = buff[13]
            m.FbruL = buff[14]
            m.FbruLT = buff[15]
            m.eL = buff[16]
            m.eLT = buff[17]
            m.eST = buff[18]
            m.E = buff[19]
            m.Ec = buff[20]
            m.G = buff[21]
            m.mu = buff[22]
            m.w = buff[23]
            matArray.append(m)
        inp.close
        return matArray