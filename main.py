import numpy as np 
import matplotlib.pyplot as plt

import eeg_filter.filters as filters

import eeg_filter.stream_processing as sp 

import eeg_filter.pgc as pgc

if __name__ == "__main__":
    
    X = np.loadtxt(r"C:\Users\insec\Desktop\Mous\RD\РД-амигдала-М1\281-19.07.18\RD_Am_R.txt")
    path = r"C:\Users\insec\Desktop\Mous\RD\РД-амигдала-М1"
    
    pgc.txt_edit()
    #Фильтрация одиночного файла
    filters.EegFilter(X)
    
    #Фильтрация нескольких файлов по указанному пути
    sp.stream_filter(path)
    
    
    plt.plot(X[:,0], X[:,1])
    plt.show()

