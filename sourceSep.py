# -*- coding: utf-8 -*-
"""
Christian Teeples
"""

import numpy as np
import soundfile as sf
from scipy import signal
from sklearn.decomposition import FastICA, PCA

def unmixAudio(leftName, rightName) :
    matrix = []
    n = 0
    leftNameList, leftSampleRate = readWaveFile(leftName)
    rightNameList, rightSampleRate = readWaveFile(rightName)
    maximum = max(len(leftNameList), len(rightNameList))

    while n < maximum:
        temp = [leftNameList[n], rightNameList[n]]
        matrix.append(temp)
        for item in temp:
            del item
        n = n + 1
        
    npMatrix = np.asarray(matrix)
    
    ica = FastICA(n_components=2)
    S_ = ica.fit_transform(npMatrix)  # Reconstruct signals
    A_ = ica.mixing_  # Get estimated mixing matrix
    S_ = S_ * 10
    writeWaveFile("unmixed0.wav", S_[:, 0], leftSampleRate)
    writeWaveFile("unmixed1.wav", S_[:, 1], rightSampleRate)
    
###############################################################################
def writeWaveFile(outName, fileNameList, samplerate):
    sf.write(outName, fileNameList, samplerate) 
###############################################################################
def readWaveFile(fileName):
    data, samplerate = sf.read(fileName)
    return data, samplerate
###################  main  ####################################################
if __name__ == "__main__" :
    leftName = "darinSiren0.wav"
    rightName = "darinSiren1.wav"
    unmixAudio(leftName, rightName)
