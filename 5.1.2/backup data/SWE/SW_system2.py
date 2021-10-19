# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:30:38 2020

@author: chong
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def draw_v2(data,t,x):
    plt.figure()
    X = np.arange(0, x, x/(data.shape[1]))         
    Y = np.arange(0, t, t/(data.shape[0]))
    #网格化数据
    X, Y = np.meshgrid(X, Y)
    plt.contourf(X, Y, data, levels=100)
    plt.show()
    
    figure = plt.figure()
    ax = Axes3D(figure)
    ax.plot_surface(X, Y, data, rstride=1, cstride=1, cmap='rainbow')
    plt.show() 

#define the grid size 
n = 50

dt = 0.01
dx = 1
dy = 1
g = 9.8

T=500

H = np.ones((n+2,n+2))# displacement matrix (this is what gets drawn) 
U = np.zeros((n+2,n+2))# x velocity 
V = np.zeros((n+2,n+2))# y velocity 

#create initial displacement
Z=np.zeros((10,10))
a=np.linspace(-3,3,10)
for i in range(10):
    for j in range(10):
        R=np.sqrt(a[i]**2+a[j]**2)+1e-16
        Z[i,j]=np.sin(R)/R
        if Z[i,j]<0:
            Z[i,j]=0

#add displacement to the height matrix 
w = Z.shape[1] 
H[10:w+10,20:w+20] += Z
draw_v2(H,n,n)

#empty matrix for half-step calculations 
Hx = np.zeros((n+1,n+1))
Hy = np.zeros((n+1,n+1))
Ux = np.zeros((n+1,n+1))
Uy = np.zeros((n+1,n+1))
Vx = np.zeros((n+1,n+1))
Vy = np.zeros((n+1,n+1))

#X = np.arange(0, n, n/(H.shape[1]))         
#Y = np.arange(0, n, n/(H.shape[0]))
#X, Y = np.meshgrid(X, Y)
#plt.figure()
for t in range(T):
    
    '''
    #blending the edges keeps the function stable 
    H[:,0] = H[:,1] 
    H[:,n+1] = H[:,n] 
    H[0,:] = H[1,:] 
    H[n+1,:] = H[n,:] 

    #reverse direction at the x edges 
    U[0,:] = -U[1,:] 
    U[n+1,:] = -U[n,:] 

    #reverse direction at the y edges 
    V[:,0] = -V[:,1]
    V[:,n+1] = -V[:,n]
    '''
    
    for i in range(n+1):
        for j in range(n+1):
            #height 
            Hx[i,j] = (H[i+1,j+1]+H[i,j+1])/2 - dt/(2*dx)*(U[i+1,j+1]-U[i,j+1])
            Hy[i,j] = (H[i+1,j+1]+H[i+1,j])/2 - dt/(2*dy)*(V[i+1,j+1]-V[i+1,j])

            #x momentum 
            Ux[i,j] = (U[i+1,j+1]+U[i,j+1])/2 \
                      - dt/(2*dx)*(U[i+1,j+1]*U[i+1,j+1]/H[i+1,j+1]-U[i,j+1]*U[i,j+1]/H[i,j+1] \
                      + (g/2)*H[i+1,j+1]*H[i+1,j+1]- (g/2)*H[i,j+1]*H[i,j+1]) 
            Uy[i,j] = (U[i+1,j+1]+U[i+1,j])/2 \
                      - dt/(2*dy)*(V[i+1,j+1]*U[i+1,j+1]/H[i+1,j+1] \
                      - V[i+1,j]*U[i+1,j]/H[i+1,j])

            #y momentum 
            Vx[i,j] = (V[i+1,j+1]+V[i,j+1])/2 \
                      - dt/(2*dx)*((U[i+1,j+1]*V[i+1,j+1]/H[i+1,j+1]) \
                      -(U[i,j+1]*V[i,j+1]/H[i,j+1]))
            Vy[i,j] = (V[i+1,j+1]+V[i+1,j])/2 \
                      - dt/(2*dy)*((V[i+1,j+1]*V[i+1,j+1]/H[i+1,j+1] \
                      + g/2*H[i+1,j+1]*H[i+1,j+1]) \
                      - (V[i+1,j]*V[i+1,j]/H[i+1,j] \
                      - g/2*H[i+1,j]*H[i+1,j]))
    
    #Second half step 
    for i in range(1,n+1):
        for j in range(1,n+1):

           #height 
           H[i,j] = H[i,j] - (dt/dx)*(Ux[i,j-1]-Ux[i-1,j-1]) \
                           - (dt/dy)*(Vy[i-1,j]-Vy[i-1,j-1])
           #x momentum 
           U[i,j] = U[i,j] - (dt/dx)*((Ux[i,j-1]*Ux[i,j-1]/Hx[i,j-1] \
                           + g/2*Hx[i,j-1]*Hx[i,j-1]) \
                           - (Ux[i-1,j-1]*Ux[i-1,j-1]/Hx[i-1,j-1] \
                           + g/2*Hx[i-1,j-1]*Hx[i-1,j-1])) \
                           - (dt/dy)*((Vy[i-1,j]*Uy[i-1,j]/Hy[i-1,j]) \
                           -(Vy[i-1,j-1]*Uy[i-1,j-1]/Hy[i-1,j-1]))
           #y momentum 
           V[i,j] = V[i,j] - (dt/dx)*((Ux[i,j-1]*Vx[i,j-1]/Hx[i,j-1]) \
                           - (Ux[i-1,j-1]*Vx[i-1,j-1]/Hx[i-1,j-1])) \
                           - (dt/dy)*((Vy[i-1,j]*Vy[i-1,j]/Hy[i-1,j] \
                           + g/2*Hy[i-1,j]*Hy[i-1,j]) \
                           -(Vy[i-1,j-1]*Vy[i-1,j-1]/Hy[i-1,j-1] \
                           + g/2*Hy[i-1,j-1]*Hy[i-1,j-1]))
          
    if np.mod(t,100)==0:
        draw_v2(H,n,n)
    #plt.contourf(X, Y, H, levels=100)
    #plt.colorbar()
    #plt.show()
    #plt.pause(0.02)
    #plt.clf()     