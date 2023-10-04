import numpy as np 
import matplotlib.pyplot as plt


#Модуль содержит класс с фильтрами 
import filters as filters

#Модуль содержит функцию для обработки множества файлов в каталоге
import stream_processing as sp 

#Модуль содержит функции обработки только что сконвертированных PGC файлов - указывать путь к каталогу с файлами
#import pgc as pgc

#Модуль содержит функция построения и схоранения графиков
import ploting as ploting

if __name__ == "__main__":
    

    #Пути к файлам 
    X = np.loadtxt(r"C:\Users\arzdez\Desktop\РД_крысы_текст\РД-амигдала-М1\281-10.07.18\RD_Am_R+.txt", comments='#')
    #path = r"C:\Users\insec\Desktop\РД - кора S1-M1_txt"
    #path_archive = r"C:\Users\insec\Desktop\RD_txt\New data\rat 10 - test 1 - 7.11.22_zip"
    #path_copy = r"C:\Users\insec\Desktop\Тесты обработки\РД-амигдала-М1_copy"
   # sample_rate = 1000
    #Hz_1 = (49,51)
   # Hz_2 = 99
    
    #Изменение запятых на точки - не акутально в связи с возможностью конвертирования через matlab и python, но оставляю на всякий случай
    #pgc.comma_to_dot(r"C:\Users\arzdez\Desktop\РД_крысы_текст", comment_line = 4)
    
    #Архивация данных
    #pgc.txt_to_zip(path, path_archive)
   
   
#------------------------------------------------------------------------------------------------------------- 
    #Фильтрация одиночного файла - создаётся экземпляр класс и после вызываются интресующие вас фильтры
    #подробная инструкция к классу указана в файле класса
    #f_data = filters.EegFilter(X)
    #Расчёт  скользящего среднего
    #mavg = f_data.moving_avg()

    #Вычитание скользящего среднего
    #detrend_data = f_data.detrend()

    #Частотный фильтр
    #f_data.frequency_filter(sample_rate, notch_filter = Hz_1, low_pass_filter = Hz_2 )
    


    
    #Обращенние к атрибутам класса
    #детрендированный ряд
    #X1 = f_data.detrend_data

    #отфильтрованный ряд
    #clear_data = f_data.clear_data
    
    #print(X2)
    #Тренд
    #trend = f_data.trend
    #Сигнал без тренда
    #X4 = f_data.detrend_data
#--------------------------------------------------------------------------------------------------------------------
    #Потоковая обработка - обрабатывает все файлы в указанной папке  и подпапках
    #sp.stream_filter(path, ploting=True)
    #Многоядерный вариант
    #sp.stream_filter_parallel(r"C:\Users\arzdez\Desktop\РД_крысы_текст", ploting = False)
# Графики
    #ploting.ploter(trend)
    #ploting.ploter(detrend)
    #ploting.ploter(clear)
    #ploting.ploter(clear_data)
    #f_data.plot_ft("clear_data", sample_rate,show_all=True)