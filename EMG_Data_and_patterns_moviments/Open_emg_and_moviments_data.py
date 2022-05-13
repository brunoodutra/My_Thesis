# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 21:27:15 2020

@author: bruno
"""

import numpy as np
from sklearn import svm, metrics
from sklearn.metrics import confusion_matrix
from numpy.linalg import inv
import matplotlib.pyplot as plt 
import scipy.optimize as opt
from sklearn.model_selection import train_test_split
from yellowbrick.classifier import ConfusionMatrix
import scipy.io
import seaborn as ns;
from sklearn.model_selection import cross_val_score

mat = scipy.io.loadmat('EMG_patterns_datalog/recording_mov_bruno.mat')     

emg = mat['emg'];
stimulus= mat['stimulus'];
t= mat['temp'];
   
u1=emg[:,0];
u2=emg[:,1];
u3=emg[:,2];
u4=emg[:,3];
u5=emg[:,4];
u6=emg[:,5];
u7=emg[:,6];
u8=emg[:,7];
y=stimulus;


fig1, axs = plt.subplots(8, 1)
fig1.suptitle('Dados MYO')
axs[0].plot(u1, 'y')
axs[1].plot(u2, 'b')
axs[2].plot(u3, 'g')
axs[3].plot(u4, 'r')
axs[4].plot(u5, 'y')
axs[5].plot(u6, 'b')
axs[6].plot(u7, 'g')
axs[7].plot(y, 'r')
plt.show()