#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:51:09 2020

@author: chong
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SW:
    def __init__(self):
        self.Nx,self.Ny=51,51
        #self.X,self.Y=10,10
        
        self.N=1500
        
        self.deltx,self.delty=10,10#self.X/self.Nx,self.Y/self.Ny
        
        self.u=np.zeros((self.N,self.Nx,self.Ny))
        self.v=np.zeros((self.N,self.Nx,self.Ny))
        self.h_star=np.zeros((self.Nx,self.Ny))
        self.h=np.ones((self.N,self.Nx,self.Ny))
        
        #self.h[0,int(self.Nx/2),int(self.Ny/2)]=1
        
        self.he=1
        self.hw=1
        self.hn=1
        self.hs=1
        
        self.deltt=0.05#np.min(self.deltx,self.delty)/np.sqrt(2*10*hmax)
        
        #create initial displacement
        Z=np.zeros((10,10))
        a=np.linspace(-3,3,10)
        for i in range(10):
            for j in range(10):
                R=np.sqrt(a[i]**2+a[j]**2)+0.01
                Z[i,j]=np.sin(R)/R
                if Z[i,j]<0:
                    Z[i,j]=0
        
        
        #draw_v2(Z,10,10)
        #add displacement to the height matrix 
        w = Z.shape[1] 
        self.h[0,10:w+10,20:w+20] += Z
        self.draw_v2(self.h[0],self.Nx,self.Ny)
    
    
    def draw_v2(self,data,t,x):
        figure = plt.figure()
        plt.clf()
        X = np.arange(0,(data.shape[1]))         
        Y = np.arange(0,(data.shape[0]))
        #网格化数据
        X, Y = np.meshgrid(X, Y)
        #plt.contourf(X, Y, data, levels=100)
        #plt.show()
        
        ax = Axes3D(figure)
        #ax.contourf(X, Y, data)
        ax.plot_surface(X, Y, data)
        plt.show()        
        
        
    def sim(self):
        
        eplison=0.005
        
        for n in range(self.N-1):
            for j in range(1,self.Nx-1):
                for k in range(1,self.Ny-1):
                    self.u[n+1,j,k]=self.u[n,j,k]-(self.deltt/self.deltx)*10*(self.h[n,j+1,k]-self.h[n,j,k])
                    self.v[n+1,j,k]=self.v[n,j,k]-(self.deltt/self.delty)*10*(self.h[n,j+1,k]-self.h[n,j,k])
            for j in range(1,self.Nx-1):
                for k in range(1,self.Ny-1):
                    self.h_star[j,k]=self.h[n,j,k]-self.deltt*((self.u[n+1,j,k]*self.he-self.u[n+1,j,k-1]*self.hw)/self.deltx-
                                                               (self.v[n+1,j,k]*self.hn-self.v[n+1,j-1,k]*self.hs)/self.delty)
            
            for j in range(1,self.Nx-1):
                for k in range(1,self.Ny-1):
                    self.h[n+1,j,k]=(1-eplison)*self.h_star[j,k]+(eplison/4)*(self.h_star[j,k-1]+
                                                                              self.h_star[j,k+1]+
                                                                              self.h_star[j-1,k]+
                                                                              self.h_star[j+1,k])
    
    def output(self):
        self.draw_v2(self.h[90],self.Nx,self.Ny)

if __name__=='__main__':
    
    eg=SW()
    eg.sim()
    eg.output()
        