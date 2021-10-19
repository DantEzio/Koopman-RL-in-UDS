# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:02:42 2019

@author: chong
"""

import PPO
import env_SWMM
import env_DLEDMD
import numpy as np
import time


if __name__=='__main__':
    '''
    date_time=['08:00','08:10','08:20','08:30','08:40','08:50',\
               '09:00','09:10','09:20','09:30','09:40','09:50',\
               '10:00','10:10','10:20','10:30','10:40','10:50',\
               '11:00','11:10','11:20','11:30','11:40','11:50','12:00']
    date_t=[0,10,20,30,40,50,\
            60,70,80,90,100,110,\
            120,130,140,150,160,170,\
            180,190,200,210,220,230,240]
    '''
    
    date_time=['08:00','08:10','08:20','08:30','08:40','08:50',\
               '09:00','09:10','09:20','09:30','09:40','09:50',\
               '10:00','10:10','10:20','10:30','10:40','10:50',\
               '11:00','11:10','11:20','11:30','11:40','11:50',\
               '12:00','12:10','12:20','12:30','12:40','12:50',\
               '13:00','13:10','13:20','13:30','13:40','13:50',\
               '14:00','14:10','14:20','14:30','14:40','14:50',\
               '15:00','15:10','15:20','15:30','15:40','15:50',\
               '16:00']
    
    date_t=[]
    for i in range(len(date_time)):
        date_t.append(int(i*10))
    
    #observation=env.reset()
    #print(env.action_space)
    num_rain=1
    # Superparameters
    
    batch_size=240
    step=2
    rain_num=1
    
    #test_num=8
    test_num=[i for i in range(4)]
    
    rainData1=np.loadtxt('./sim/testRainFile.txt',delimiter=',')#读取测试降雨数据
    rainData2=np.loadtxt('./sim/real_rain_data.txt',delimiter=' ')*10#读取真实降雨数据
    rainData=np.vstack((rainData1[:,:120],rainData2[:4,:]))#共8场降雨
    
    envK=env_DLEDMD.env_DLEDMD(rainData)
    K_PPO = PPO.PPO(envK,step, 24, num_rain, 'ppo_DLEDMD')
    t1=time.time()
    K_PPO.train()
    t2=time.time()
    print(t2-t1)
    
    envS=env_SWMM.env_SWMM(date_time, date_t)
    K_PPO.change_env(envS)
    r2=K_PPO.test(test_num,50)