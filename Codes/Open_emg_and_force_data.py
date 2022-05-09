# -*- coding: utf-8 -*-
"""
Created on Tue April 20 22:09:25 2022
@author: bruno
"""


# Open libraries 
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt 
#import functions as func
import scipy.io
import seaborn as ns;
#import Ident as id
from sklearn.model_selection import cross_val_score

# read the datalog that is in " .m " file 
mat = scipy.io.loadmat('EMG_force_datalog/recording_force_v1.mat')     
emg = mat['emg'];
force=  mat['Force'];
Ts= mat['Ts'];

# define th Signal EMG with the imput signal 
u1=emg[:,0];
u2=emg[:,1];
u3=emg[:,2];
u4=emg[:,3];
u5=emg[:,4];
u6=emg[:,5];
u7=emg[:,6];
u8=emg[:,7];

#Define the grasping force with the output signal 
y=force;
y.shape=(-1,1)
nit=y.shape[0]


#%%
# sample time 
Ts=0.005
# datalog recording time 
t  =np.linspace(1, Ts*nit-Ts, nit)

# plot the EMG and Force  signals    
fig, axs = plt.subplots(8, 1)
fig.suptitle('Dados MYO')
axs[0].plot(t, u1, 'y')
axs[1].plot(t, u2, 'b')
axs[2].plot(t, u3, 'g')
axs[3].plot(t, u4, 'r')
axs[4].plot(t, u5, 'y')
axs[5].plot(t, u6, 'b')
axs[6].plot(t, u7, 'g')
axs[7].plot(t, y, 'r')
plt.show()