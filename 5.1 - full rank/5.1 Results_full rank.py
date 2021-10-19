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

#Prepare training data
df_s0 = pd.read_excel(r'./save_data/excelfile/rain0_set0_state_data.xlsx')
df_a0= pd.read_excel(r'./save_data/excelfile/rain0_set0_action_data.xlsx')
df_r0= pd.read_excel(r'./save_data/excelfile/rain0_set0_rain_data.xlsx')
df_node0= pd.read_excel(r'./save_data/excelfile/rain0_set0_node_data.xlsx')
df_sub0= pd.read_excel(r'./save_data/excelfile/rain0_set0_sub_data.xlsx')
dt_s0=df_s0.values[:,1:]
dt_a0=df_a0.values[:,1:]
dt_r0=df_r0.values[:,1:]
dt_node0=df_node0.values[:,1:]
dt_sub0=df_sub0.values[:,1:]
data=np.concatenate((dt_s0,dt_a0,dt_r0,dt_node0,dt_sub0),axis=1)
    
for it in range(3):
    for jt in range(3):   
        df_s0 = pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_state_data.xlsx')
        df_a0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_action_data.xlsx')
        df_r0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_rain_data.xlsx')
        df_node0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_node_data.xlsx')
        df_sub0= pd.read_excel(r'./save_data/excelfile/rain'+str(it)+'_set'+str(jt)+'_sub_data.xlsx')
        dt_s0=df_s0.values[:,1:]
        dt_a0=df_a0.values[:,1:]
        dt_r0=df_r0.values[:,1:]
        dt_node0=df_node0.values[:,1:]
        dt_sub0=df_sub0.values[:,1:]
        tem=np.concatenate((dt_s0,dt_a0,dt_r0,dt_node0,dt_sub0),axis=1)
        data=np.concatenate((data,tem),axis=0)
    
data=np.array(data)
print(data.shape)


#8 rainfall's data
rainlog=0
alog=0

df_s0 = pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_state_data.xlsx')
df_a0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_action_data.xlsx')
df_r0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_rain_data.xlsx')
df_node0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_node_data.xlsx')
df_sub0= pd.read_excel(r'./save_data/excelfile/TEST_rain'+str(rainlog)+'_set'+str(alog)+'_sub_data.xlsx')
dt_s0=df_s0.values[:,1:]
dt_a0=df_a0.values[:,1:]
dt_r0=df_r0.values[:,1:]
dt_node0=df_node0.values[:,1:]
dt_sub0=df_sub0.values[:,1:]
data8=np.concatenate((dt_s0,dt_a0,dt_r0,dt_node0,dt_sub0),axis=1)



X_train, Y_train=data[:50,:],data[1:51,:]
X_test, Y_test=data8[:46,:],data8[1:47,:]
print(X_train.shape,X_test.shape)

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
m1,m2=100,1000
Y_out1,Y_out2=[],[]
for t in range(Y_test.shape[0]):
    tem1=model_mmd_dmd.prediction(X_test[t,:],m1,1)
    tem2,_=model_kernel_edmd.prediction(X_test[t,:],m2,1)
    Y_out1.append(tem1[0])
    Y_out2.append(tem2[0])
    
Y_out1,Y_out2=np.array(Y_out1),np.array(Y_out2)

print('Rain'+str(rainlog)+':')
print('KEDMD:')
print('MSE:',MSE(Y_out2,Y_test),'  NSE:',NSE(Y_out2,Y_test))
print('KVAD:')
print('MSE:',MSE(Y_out1,Y_test),'  NSE:',NSE(Y_out1,Y_test))

i=0
#plt.plot(Y_out1[:,i],'r:',label='KVAD')
plt.plot(Y_out2[:,i],'b:',label='KEDMD')
plt.plot(Y_test[:,i],'k',label='SWMM')