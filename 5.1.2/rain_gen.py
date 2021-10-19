# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 09:26:52 2020

@author: chong
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class rain_gen:
    def __init__(self,t,deltt,T):#生成降雨，t是每场降雨时间步数，deltt是时间间隔，T是降雨总场数
        self.Rains=[]
        self.As,self.Cs,self.Ps,self.ns,self.bs,self.Ks=[],[],[],[],[],[]
        #T=[1,3,5,10]
        for i in T:
            A=30#np.random.randint(21,35)
            C=1#np.random.randint(939,1200)/1000.00
            P=i#np.random.randint(1,100)
            n=0.90#np.random.randint(86,96)/100.00
            b=18#np.random.randint(16,22)
            K=0.5#np.random.randint(3,8)/10.00
            rain=self.gen_rain(t,A,C,P,b,n,K,deltt)
            self.Rains.append(rain)
            self.As.append(A)
            self.Cs.append(C)
            self.Ps.append(P)
            self.ns.append(n)
            self.bs.append(b)
            self.Ks.append(K)
        
    def gen_rain(self,t,A,C,P,b,n,K,deltt):
        '''
        t是生成雨量时间序列步数上限
        delt是时间间隔，取1
        '''
        rain=[]
        for i in range(t):
            if i <int(t*K):
                rain.append(A*(1+C*np.log(P))/np.power(((t*K-i)+b),n))
            else:
                rain.append(A*(1+C*np.log(P))/np.power(((i-t*K)+b),n))
        
        plt.plot(rain)
        return rain
    
    def fig_parameters(self):
        data={'A':np.array(self.As)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of A')
        
        data={'C':np.array(self.Cs)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of C')
        
        data={'P':np.array(self.Ps)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of P')
        
        data={'n':np.array(self.ns)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of n')
        
        data={'b':np.array(self.bs)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of b')
        
        data={'K':np.array(self.Ks)}
        pddata=pd.DataFrame(data)
        pddata.plot.box(title='Box plot of K')
        
    def save_rainfall_data(self):
        np.savetxt('./source data/5.1.2.2_rainfall data.txt',np.array(self.Rains))
    
    def get_rainfall_data(self):
        return self.Rains
    
    def fig_rainfall_data(self):
        plt.plot(self.Rains)

if __name__=='__main__':
    P=[1,3,5,10]
    rg=rain_gen(121,1,P)
    rg.save_rainfall_data()
    #rg.fig_rainfall_data()
    