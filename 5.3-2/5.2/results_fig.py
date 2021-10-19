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
dfDLEDMD_DQN=pd.read_csv('./dqn_DLEDMD_test_result/dqn_DLEDMDflooding_vs_t.csv').values
dfKEDMD_DQN=pd.read_csv('./dqn_KEDMD_test_result/dqn_KEDMDflooding_vs_t.csv').values
dfDLEDMD_PPO=pd.read_csv('./ppo_DLEDMD_test_result/ppo_DLEDMDflooding_vs_t.csv').values
dfKEDMD_PPO=pd.read_csv('./ppo_KEDMD_test_result/ppo_KEDMDflooding_vs_t.csv').values
dfSWMM_DQN=pd.read_csv('./dqn_SWMM_test_result/dqn_SWMMflooding_vs_t.csv').values
dfSWMM_PPO=pd.read_csv('./ppo_SWMM_test_result/ppo_SWMMflooding_vs_t.csv').values

dfhc=pd.read_csv('./hc_flooding_vs_t.csv').values

#datas=[dfdqn,dfddqn,dfppo1,dfppo2,dfa2c,dfvt]

font1 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 20,}

font2 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 15,}

font3 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 15,}


def draw(data,dfhc):
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
    plt.plot(dfhc,'k:',label='Water level system',alpha=0.5)
    #plt.legend(prop=font1)
    

#data=dfa2c[:,0:10]
#draw(data,dfop[0],dfhc[0])


fig = plt.figure(figsize=(26,20))
N_lines=6
line=0
im=1
while im < 25:
    
    if line ==0:
        data=dfDLEDMD_PPO
    elif line==1:
        data=dfKEDMD_PPO
    else:
        data=dfSWMM_PPO
    
    print(data.shape)
    
    plts=fig.add_subplot(N_lines,4,im)
    
    draw(data[:,0:49],dfhc[:,0])
    
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    plt.ylabel('CSO volume (10$^{3}$ m$^{3}$)',font2)
    
    im+=1
    
    plts=fig.add_subplot(N_lines,4,im)
    draw(data[:,50:99],dfhc[:,1])
    
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    
    im+=1
    
    plts=fig.add_subplot(N_lines,4,im)
    draw(data[:,100:149],dfhc[:,2])
    
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    
    im+=1
    
    plts=fig.add_subplot(N_lines,4,im)
    draw(data[:,150:199],dfhc[:,3])
    
    if im<5:
        plt.title('Rain'+str(im),fontdict=font3)
    if im>20:
        plt.xlabel('time (minute)',font2)
    
    im+=1
    
    line=line+1
  


plt.text(-217, 275, r'DLEDME-DQN', fontdict=font1)
plt.text(-217, 225, r'KEDMD-DQN', fontdict=font1)
plt.text(-217, 175, r'SWMM-DQN', fontdict=font1)
plt.text(-217, 125, r'DLEDMD-PPO', fontdict=font1)
plt.text(-217, 75, r'KEDMD-PPO', fontdict=font1)
plt.text(-217, 25, r'SWMM-PPO', fontdict=font1)

fig.savefig('5.3.2.png', bbox_inches='tight', dpi=200)