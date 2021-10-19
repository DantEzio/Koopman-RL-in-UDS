# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 16:40:00 2021

@author: chong
"""

import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import pandas as pd

import mmd

#MSE and NSE
def MSE(x,y):
    return np.sqrt(np.mean(np.square(x-y)))

def NSE(pre,tar):
    a=np.sum(np.square(pre-tar))/np.sum(np.square(tar-np.mean(tar)))
    return 1-a


    
def test_ver2():
    #去掉降雨数据，因为降雨数据和inflow相关性太强
    #Prepare training data
    df_s0 = pd.read_excel(r'./save_data/excelfile/rain0_set0_state_data.xlsx')
    df_a0= pd.read_excel(r'./save_data/excelfile/rain0_set0_action_data.xlsx')
    df_r0= pd.read_excel(r'./save_data/excelfile/rain0_set0_rain_data.xlsx')
    dt_s0=df_s0.values[:,1:]
    dt_a0=df_a0.values[:,1:]
    dt_r0=df_r0.values[:,1:]
    data=np.concatenate((dt_s0,dt_a0,dt_r0),axis=1)
        
    for it in range(10):
        for jt in range(1):   
            df_s0 = pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_state_data.xlsx')
            df_a0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_action_data.xlsx')
            df_r0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_rain_data.xlsx')
            dt_s0=df_s0.values[:,1:]
            dt_a0=df_a0.values[:,1:]
            dt_r0=df_r0.values[:,1:]
            tem=np.concatenate((dt_s0,dt_a0,dt_r0),axis=1)
            data=np.concatenate((data,tem),axis=0)
        
    data=np.array(data)
    
    '''
    #8 rainfall's data
    rainlog=0
    alog=0
    
    df_s0 = pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_state_data.xlsx')
    df_a0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_action_data.xlsx')
    df_r0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_rain_data.xlsx')
    dt_s0=df_s0.values[:,1:]
    dt_a0=df_a0.values[:,1:]
    dt_r0=df_r0.values[:,1:]
    data8=np.concatenate((dt_s0,dt_a0,dt_r0),axis=1)
    
    for it in range(1):
        for jt in range(10):   
            df_s0 = pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(it)+'_set'+str(jt)+'_state_data.xlsx')
            df_a0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(it)+'_set'+str(jt)+'_action_data.xlsx')
            df_r0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(it)+'_set'+str(jt)+'_rain_data.xlsx')
            dt_s0=df_s0.values[:,1:]
            dt_a0=df_a0.values[:,1:]
            dt_r0=df_r0.values[:,1:]
            tem=np.concatenate((dt_s0,dt_a0,dt_r0),axis=1)
            data8=np.concatenate((data8,tem),axis=0)
    '''
    
    X_train, Y_train=data[:210,:],data[1:211,:]
    
    #Train models: KVAD, KEDMD
    feature_dim = 1000
    feature_W = np.random.rand(X_train.shape[1], feature_dim) * 2 -1
    feature_b = np.random.rand(feature_dim)
    def feature_mapping(X):
        return np.exp(-(X.dot(feature_W) + feature_b) ** 2 / 2)
        
    model_mmd_dmd = mmd.linear_mmd_dmd(input_dim=X_train.shape[1], feature_mapping=feature_mapping)
    model_mmd_dmd.train(X_train, Y_train)
       
    model_kernel_edmd = mmd.kernel_edmd(input_dim=X_train.shape[1])
    model_kernel_edmd.train(X_train, Y_train)
    
    #Prediction
    rainlog=0
    X_test, Y_test=data[:(rainlog+1)*47,:],data[1+rainlog*47:(rainlog+1)*47+1,:]
    m1,m2=100,100
    
    test_mode=0
    if test_mode==0:
        Y_out1,Y_out2=[],[]
        for t in range(Y_test.shape[0]):
            tem1=model_mmd_dmd.prediction(X_test[t,:],m1,1)
            tem2,_=model_kernel_edmd.prediction(X_test[t,:],m2,1)
            Y_out1.append(tem1[0])
            Y_out2.append(tem2[0])
        Y_out1,Y_out2=np.array(Y_out1),np.array(Y_out2)
    else:
        Y_out1=model_mmd_dmd.prediction(X_test[0,:],m1,Y_test.shape[0])
        Y_out2,_=model_kernel_edmd.prediction(X_test[0,:],m2,Y_test.shape[0])
        
        
    print('Rain'+str(rainlog)+':')
    print('KEDMD:')
    print('MSE:',MSE(Y_out2[:,:4],Y_test[:,:4]),'  NSE:',NSE(Y_out2[:,:4],Y_test[:,:4]))
    
    print('KVAD:')
    print('MSE:',MSE(Y_out1[:,:4],Y_test[:,:4]),'  NSE:',NSE(Y_out1[:,:4],Y_test[:,:4]))
    
    i=0
    plt.plot(Y_out1[:,i],'r:',label='KVAD')
    plt.plot(Y_out2[:,i],'b:',label='KEDMD')
    plt.plot(Y_test[:,i],'k',label='SWMM')
    
if __name__=='__main__':
    test_ver2()