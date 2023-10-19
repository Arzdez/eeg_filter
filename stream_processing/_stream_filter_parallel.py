import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing as mp

from functools import partial

from filters import EegFilter

def _processing(
    path: str, *,
    ploting: bool = True,
    chanels: tuple = None,
    window: int = 1501,
    sample_rate = 1000,
    low_pass_filter = 99,
    notch_filter = (49,51)) -> None:
    
    if chanels is None:
        chanels = (
            "time", 
            "Cd_R", 
            "Cd_L", 
            "Cx_occip_R", 
            "Cx_occip_L"
        )
         
    print("Обрабатывается файл: " , path)
    #Грузим текст по пути
    input_data = np.loadtxt(path, comments="#")
    
    #Выделяем для удобства
    #times = input_data[:, 0]
    
    #устанвока нужных аргументов и филтрация
    ready_data = EegFilter(input_data, w = window)
    #ready_data.del_pick()
    ready_data.frequency_filter(sample_rate, notch_filter =notch_filter, low_pass_filter = low_pass_filter)
    trend = ready_data.trend
    clear_data= ready_data.clear_data

    times = clear_data[:,0]
    #Если заданно то рисуем для каждого канала его чистую версию и тренд
    if ploting:
        for i in range(1, np.shape(input_data)[1]):
            plt.subplot(2, 1, 1)
            plt.title(f"Тренд  {chanels[i]}")
            plt.plot(times, trend[:, i])
            plt.subplot(2, 1, 2)
            plt.title(f"Отфильтрованный сигнал {chanels[i]} ")
            plt.plot(times, clear_data[:, i])
            plt.tight_layout()
            plt.savefig(os.path.join(path.replace(".txt", f"_{chanels[i]}.png")),   dpi=1000)
            plt.close()
                    
    #Сохраняем ряды
    print("Сохраняю: ", path)
    np.savetxt(os.path.join(path.replace(".txt", "_trend.txt")), trend)
    np.savetxt(os.path.join(path.replace(".txt", "_clear.txt")), clear_data.real)


def stream_filter_parallel(
    path: str, *,
    ploting: bool = False,
    chanels: tuple = None,
    window: int = 1501,
    sample_rate = 1000 ) -> None:
    """
    Обрабатывает все .txt файлы по указанному пути.
    Если файлы лежат в поддиректориях то структура останется. 
    Сохраняет копию тренда и копии детрендированного ряда в той же папке где лежит исходный ряд
    
    Обязательный аргумент:
    Path - путь к дирректории хранящей файлы;
    
    Именованные аргументы:
    ploting - если True - по указанному пути вместе с обработанными копиями будут сохраняться изображения графиков;
    chanels - подаётся картеж с именами каналов;
    window - ширина окна;
    sample_rate - частота дискретизации.
    
    """
    #Имена отведений
    if chanels is None:
        chanels = (
            "time", 
            "Cd_R", 
            "Cd_L", 
            "Cx_occip_R", 
            "Cx_occip_L"
        )
        
    os.chdir(path)
    
    #Массив для путей
    path_tuple = []
    
    #Устанвка параметров чтобы с map не возиться
    part_processing = partial(_processing, ploting = ploting, chanels = chanels, window = window, sample_rate = sample_rate)

    #Собираем все пути к файлам
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if ".txt" in name:
                path_tuple.append(os.path.join(root, name))

    #ограничение на число процессов
    if len(path_tuple) > 8:
        thread = 8
    else:
        thread = len(path_tuple)
    
    #Создаём пул с процессами для оработки
    with mp.Pool(processes = thread ) as work:
        work.map(part_processing, path_tuple)



