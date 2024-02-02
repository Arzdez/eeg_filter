import numpy as np 
import matplotlib.pyplot as plt


#Модуль содержит класс с фильтрами 
import filters as filters

#Модуль содержит функцию для обработки множества файлов в каталоге
import stream_processing as sp 

#Модуль содержит функции обработки только что сконвертированных PGC файлов - указывать путь к каталогу с файлами
import pgc as pgc

#Модуль содержит функция построения и схоранения графиков
import ploting as ploting

if __name__ == "__main__":
    
    #X = r"C:\Users\insec\Desktop\RD_CX_L+_trend.txt"
    #Пути к файлам 
    X = np.loadtxt(r"C:\Users\insec\Desktop\25txt\2020_2_25_9_50.dat_R12.txt")
    #path = r"C:\Users\insec\Desktop\25txt"
    #path_archive = r"C:\Users\insec\Desktop\RD_txt\New data\rat 10 - test 1 - 7.11.22_zip"
    #path_copy = r"C:\Users\insec\Desktop\Тесты обработки\РД-амигдала-М1_copy"
    #sample_rate = 1000
    #Hz_1 = (49,51)
    #Hz_2 = 99
    
    #Изменение запятых на точки - не акутально в связи с возможностью конвертирования через matlab и python, но оставляю на всякий случай
    #pgc.comma_to_dot_parallel(path, comment_line = 0)
    
    #Архивация данных
    #pgc.txt_to_zip(path, path_archive)
   
   
#------------------------------------------------------------------------------------------------------------- 
    #Фильтрация одиночного файла - создаётся экземпляр класс и после вызываются интресующие вас фильтры
    #подробная инструкция к классу указана в файле класса
    #f_data = filters.EegFilter(X,w=3000)
    
    #Расчёт  скользящего среднего
    #f_data.moving_avg()

    #Вычитание скользящего среднего
    #f_data.detrend()
    #Удаление пиков
    #f_data.del_pick()
    #Частотный фильтр
    #f_data.frequency_filter(sample_rate, notch_filter = Hz_1, low_pass_filter = Hz_2 )
    


    
    #Обращенние к атрибутам класса
    #Обращение к детрендированному ряду
    #X1 = f_data.detrend_data
    #Обращение к полностью обработанной копии
    #clear_data = f_data.clear_data
    
    #print(X2)
    #Обращение к атрибуту который содержит тренд
    #trend = f_data.trend

    #обращение к ряду без пиков
    #X4 = f_data.del_pick_data
        
    #Обращение к атрибуту содержащему детрендированный сигнал 
    #X4 = f_data.detrend_data
#--------------------------------------------------------------------------------------------------------------------
    #Потоковая обработка
    #sp.stream_filter(path, ploting=True)
    
   # sp.stream_filter_parallel(path, ploting = True)
# Вывод графика
    ploting.ploter(X,figsize=(23,15),time_in_data=True,save=True,theme=False)
    #f_data.plot_ft("clear_data", sample_rate,show_all=True)
    #pass
    
    
    
    