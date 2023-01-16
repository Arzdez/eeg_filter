import numpy as np
import matplotlib.pyplot as plt
import os

from eeg_filter.filters import EegFilter



def stream_filter(path: str, *, ploting: bool = False, chanels: tuple = None, window: int = 1501) -> None:
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
    """
    #Имена отведений
    if chanels is None:
        chanels = ("time", "Cd_R", "Cd_L", "Cx_occip_R", "Cx_occip_L")
        
    window = 1501
    os.chdir(path)

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if ".txt" in name:
                input_data = np.loadtxt(os.path.join(root, name))
                time = input_data[:, 0]
                
                ready_data = EegFilter(input_data, w = window)
                ready_data.All_processing()
                trend = ready_data.trend
                detrend_data = ready_data.detrend_data

                times = detrend_data[:,0]
                if ploting:
                    for i in range(1, np.shape(input_data)[1]):
                        plt.subplot(2, 1, 1)
                        plt.title(f"Тренд  {chanels[i]}")
                        plt.plot(times, trend[:, i])
                        plt.subplot(2, 1, 2)
                        plt.title(f"Детрендированный сигнал {chanels[i]} ")
                        plt.plot(times, detrend_data[:, i])
                        plt.tight_layout()
                        plt.savefig(os.path.join(root, name.replace(".txt", "")) + root.replace('\\', '_') + f"_{chanels[i]}.png", dpi=1000)
                        plt.close()
                    
                #Сохраняем ряд
                np.savetxt(os.path.join(root, name.replace(".txt", root.replace("\\", "")+"_trend.txt")), trend)
                np.savetxt(os.path.join(root, name.replace(".txt", "_detrend.txt")), detrend_data)



