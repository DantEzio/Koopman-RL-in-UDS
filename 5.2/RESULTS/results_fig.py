#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 22:23:07 2020

@author: chong
"""

import pandas as pd
import matplotlib.pyplot as plt


dfdqn_KEDMD=pd.read_excel('./Final_results.xlsx',sheet_name='dqn_KEDMD')
dfdqn_DLEDMD=pd.read_excel('./Final_results.xlsx',sheet_name='dqn_DLEDMD')
dfdqn_SWMM=pd.read_excel('./Final_results.xlsx',sheet_name='dqn_SWMM')
dfppo_KEDMD=pd.read_excel('./Final_results.xlsx',sheet_name='ppo_KEDMD')
dfppo_DLEDMD=pd.read_excel('./Final_results.xlsx',sheet_name='ppo_DLEDMD')
dfppo_SWMM=pd.read_excel('./Final_results.xlsx',sheet_name='ppo_SWMM')
dfhc=pd.read_excel('./Final_results.xlsx',sheet_name='hc')

font1 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 12,}

font2 = {'family' : 'Times New Roman',
         'weight' : 'normal',
         'size'   : 12,}

time_point=['8:00','16:00']
x=[0,dfhc[0].shape[0]]

fig = plt.figure(figsize=(15,15))
for im in range(1,9):
    plts=fig.add_subplot(4,2,im)
    plt.plot(dfdqn_KEDMD[im-1],'r:',label='KEDMD-DQN')
    plt.plot(dfdqn_DLEDMD[im-1],'b:',label='DLEDMD-DQN')
    plt.plot(dfdqn_SWMM[im-1],'k:',label='SWMM-DQN')
    plt.plot(dfhc[im-1],'k.-',label='Water level system')
    plt.title('Rain'+str(im),font2)
    
    if im in [7,8]:
        plt.xlabel('time (minute)',font2)
    plt.ylabel('CSO and flooding volume (10$^{3}$ m$^{3}$)',font2)
    
    # 增加刻度
    plt.xticks(x, time_point)

    plt.legend(prop=font1)

fig.savefig('5.2.1.png', bbox_inches='tight', dpi=500)

fig = plt.figure(figsize=(15,15))
for im in range(1,9):
    plts=fig.add_subplot(4,2,im)
    plt.plot(dfppo_KEDMD[im-1],'r:',label='KEDMD-PPO')
    plt.plot(dfppo_DLEDMD[im-1],'b:',label='DLEDMD-PPO')
    plt.plot(dfppo_SWMM[im-1],'k:',label='SWMM-PPO')
    plt.plot(dfhc[im-1],'k.-',label='Water level system')
    
    plt.title('Rain'+str(im),font2)
    if im in [7,8]:
        plt.xlabel('time (minute)',font2)
    plt.ylabel('CSO volume (10$^{3}$ m$^{3}$)',font2)

    # 增加刻度
    plt.xticks(x, time_point)
    plt.legend(prop=font1)

fig.savefig('5.2.2.png', bbox_inches='tight', dpi=500)