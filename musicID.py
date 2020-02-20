# -*- coding: utf-8 -*-
"""
Christian Teeples
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import soundfile as sf
from scipy.signal import spectrogram
import glob

###############################################################################
def classifyMusic() :
    signature, dataBaseSignature, norm, tempNorm = [], [], [], []
    dataBase = glob.glob('song-*.wav')
    x, fs = readWaveFile("test-beatles.wav")
    f, t, Sxx = spectrogram(x, fs=fs, nperseg=fs//2)
    
    signature = getSignature(Sxx, f)
    
    for item in dataBase:
        xTemp, fsTemp =readWaveFile(item)
        fTemp, tTemp, SxxTemp = spectrogram(xTemp, fs=fsTemp, nperseg=fs//2)
        dataBaseSignature.append(getSignature(SxxTemp, fTemp))
         
    norm = getNorms(dataBaseSignature, signature)
    tempNorm = norm.copy()
    tempNorm.sort()  #sorting copy of norm in order to find index of least values

    for item in tempNorm[0:5]:
        index = norm.index(item)
        print(norm[index], "   ", dataBase[index])
      
    plt.specgram(x, Fs=fs)
    plt.show()
    plotTwoBestFits(tempNorm, norm, dataBase)    
###############################################################################  
def getNorms(array, sig):
    n = []
    for item in array:
        npItem = np.asarray(item)
        npSignature = np.asarray(sig)
        n.append(np.linalg.norm((npItem - npSignature), 1))
    return n
###############################################################################
def plotTwoBestFits(array, norm, dataBase):
    for item in array[0:2]:
        index = norm.index(item)
        bestDataBaseName = dataBase[index]
        xTemp, fsTemp =readWaveFile(bestDataBaseName)
        plt.specgram(xTemp, Fs=fsTemp)
        plt.show()           
###############################################################################
def getSignature(Sxx, f):
    n = 0
    sig = []
    while n < len(Sxx[n]):
        temp = Sxx[:, n].tolist()
        index = temp.index(max(temp))
        sig.append(f[index])
        n = n + 1
    return sig
###############################################################################
def readWaveFile(fileName):
    data, samplerate = sf.read(fileName)
    return data, samplerate
###################  main  ####################################################
if __name__ == "__main__" :
    classifyMusic()
