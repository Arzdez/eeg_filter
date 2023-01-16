import numpy as np 
import matplotlib.pyplot as plt

#Модуль содержит класс с фильтрами 
import eeg_filter.filters as filters

#Модуль содержит функцию для обработки множества файлов в каталоге
import eeg_filter.stream_processing as sp 

#Модуль содержит функции обработки только что сконвертированных PGC файлов - указывать путь к каталогу с файлами
import eeg_filter.pgc as pgc

if __name__ == "__main__":
    
    #Пути к файлам 
    X = np.loadtxt(r"C:\Users\insec\Desktop\Mous\RD\РД-амигдала-М1\281-19.07.18\RD_Am_R.txt")
    path = r"C:\Users\insec\Desktop\Mous\RD\РД-амигдала-М1"
    path_archive = r"C:\Users\insec\Desktop\Mous\arch"
    
    #Изменение точек на запятые
    pgc.comma_to_dot(path)
    
    #Архивация данных
    pgc.txt_to_zip(path_data, path_archive)
    
    #Фильтрация одиночного файла
    filters.EegFilter(X)
    
    #Фильтрация нескольких файлов по указанному пути
    sp.stream_filter(path)
    
    
    plt.plot(X[:,0], X[:,1])
    plt.show()
    
