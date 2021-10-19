#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 22:23:07 2020

@author: chong
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#每个df包含所有降雨结果
dfa2c=pd.read_excel('./Final_results.xlsx',sheet_name='a2c').values
dfddqn=pd.read_excel('./Final_results.xlsx',sheet_name='ddqn').values
dfdqn=pd.read_excel('./Final_results.xlsx',sheet_name='dqn').values
dfppo1=pd.read_excel('./Final_results.xlsx',sheet_name='ppo1').values
dfppo2=pd.read_excel('./Final_results.xlsx',sheet_name='ppo2').values
dfvt=pd.read_excel('./Final_results.xlsx',sheet_name='voting').values
dfhc=pd.read_excel('./Final_results.xlsx',sheet_name='hc').values
dfop=pd.read_excel('./Final_results.xlsx',sheet_name='opt').values

#datas=[dfdqn,dfddqn,dfppo1,dfppo2,dfa2c,dfvt]

font1 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 25,}

font2 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 20,}

font3 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 25,}


def draw(data,dfop,dfhc):
    a=np.max(data,axis=1)
    b=np.min(data,axis=1)
    
    #plt.plot(a,'b',label='Upper bound')
    #plt.plot(b,'b',label='Lower bound')
    
    def func(x):
        return a[x]#+np.random.rand(1)[0]+np.random.rand(1)[0]
    #定义另一个函数
    def func1(x):
        return b[x]#+np.random.rand(1)[0]
    
    xf = [i for i in range(a.shape[0])]

    plt.fill_between(xf,func1(xf),func(xf),color='b',alpha=0.75)
    plt.plot(dfop,'k',label='Optimization model',alpha=0.5)
    plt.plot(dfhc,'k:',label='Water level system',alpha=0.5)
    #plt.legend(prop=font1)
    

#data=dfa2c[:,0:10]
#draw(data,dfop[0],dfhc[0])


fig = plt.figure(figsize=(20,24))
line=0
im=1
while im < 25:
    
    if line ==0:
        data=dfdqn
    elif line==1:
        data=dfddqn
    elif line==2:
        data=dfppo1
    elif line==3:
        data==dfppo2
    elif line==4:
        data=dfa2c
    else:
        data=dfvt
    
    print(data.shape)
    
    plts=fig.add_subplot(6,4,im)
    
    draw(data[:,0:9],dfop[:,0],dfhc[:,0])
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    plt.ylabel('CSO volume (10$^{3}$ m$^{3}$)',font2)
    im+=1
    
    plts=fig.add_subplot(6,4,im)
    draw(data[:,10:19],dfop[:,1],dfhc[:,1])
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    im+=1
    
    plts=fig.add_subplot(6,4,im)
    draw(data[:,30:39],dfop[:,3],dfhc[:,3])
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    im+=1
    
    plts=fig.add_subplot(6,4,im)
    draw(data[:,20:29],dfop[:,2],dfhc[:,2])
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    im+=1
    
    line=line+1
  


plt.text(-215, 475, r'DQN', fontdict=font1)
plt.text(-215, 375, r'DDQN', fontdict=font1)
plt.text(-215, 290, r'PPO1', fontdict=font1)
plt.text(-215, 205, r'PPO2', fontdict=font1)
plt.text(-215, 115, r'A2C', fontdict=font1)
plt.text(-215, 25, r'Voting', fontdict=font1)

fig.savefig('5.5.2.png', bbox_inches='tight', dpi=500)