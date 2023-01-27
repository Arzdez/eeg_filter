import numpy as np 
import matplotlib.pyplot as plt
import time
import shutil

#Модуль содержит класс с фильтрами 
import eeg_filter.filters as filters

#Модуль содержит функцию для обработки множества файлов в каталоге
import eeg_filter.stream_processing as sp 

#Модуль содержит функции обработки только что сконвертированных PGC файлов - указывать путь к каталогу с файлами
from eeg_filter.pgc import pgc

#Модуль содержит функция построения и схоранения графиков описания лежат в файле
from eeg_filter.ploting import ploting

if __name__ == "__main__":

    #Пути к файлам 
    X = np.loadtxt(r"C:\Users\insec\Desktop\Тесты обработки\РД-амигдала-М1\281-10.07.18\RD_Am_R+.txt")
    path = r"C:\Users\insec\Desktop\Тесты обработки\РД-амигдала-М1"
    #path_copy = r"C:\Users\insec\Desktop\Тесты обработки\РД-амигдала-М1_copy"
    sample_rate = 1000
    Hz_1 = (49,51)
    Hz_2 = 99
    
    #Изменение запятых на точки
    #pgc.comma_to_dot(path, flag_reduce = True)
    
    #Архивация данных
    #pgc.txt_to_zip(path_data, path_archive)
   
   
#------------------------------------------------------------------------------------------------------------- 
    #Фильтрация одиночного файла - создаётся экземпляр класс и после вызываются интресующие вас фильтры
    #подробная инструкция к классу указана в файле класса
    #f_data = filters.EegFilter(X)
    
    #Расчёт  скользящего среднего
    #f_data.moving_avg()

    #Вычитание скользящего среднего
    #f_data.detrend()
    #f_data.frequency_filter(sample_rate, notch_filter = Hz_1, low_pass_filter = Hz_2 )
    
    #Удаление пиков
    #f_data.del_pick()

    #Возвращает кортеж содержащий скользщее среднее и обработанный сигнал
    #X,Y = f_data.get_data()
    
    #Обращенние к атрибутам класса
    #Обращение к детрендированному ряду
    #X1 = f_data.detrend_data
    #Обращение к полностью обработанной копии
    #X2 = f_data.clear_data
    
    #print(X2)
    #Обращение к атрибуту который содержит тренд
    #X3 =f_data.trend
    #обращение к ряду без пиков
    #X4 = f_data.del_pick_data
        
    #Обращение к атрибуту содержащему детрендированный сигнал 
    #X4 = f_data.detrend_data
#--------------------------------------------------------------------------------------------------------------------
    #Потоковая обработка
    #sp.stream_filter(path)
    
# Вывод графика
    ploting.ploter(X)
    #ploting.ploter(X2)
    #f_data.plot_ft("clear_data", sample_rate)
    
