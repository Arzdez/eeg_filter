import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from scipy.fft import rfft, irfft, rfftfreq, fft, fftfreq

class EegFilter:
    """
    Класс предобработки ЭЭГ
    На вход подаётся файл ЭЭГ для которого создаётся экземпляр класса и при желании размер окна w - !!именованный аргумент!!, значение по умолчанию 1501.

    После можно вызывать нужные методы
    _moving_avg ,_fourier  и _detrending - вспомагательные методы, считают скользящую среднюю, фурье образ и вычитают тренд, соответсвенно



    moving_avg- метод считает и возвращает скользящуюю среднюю - self.trend
    detrend - метод вычитает тренд и взворащает детрендированный ряд но единичные пики не удаляются - self.detrend_data
    del_pick - метод удаляет резкие пики -  self.del_pick_data
    
    frequency_filter - фильтр частот прини - self.clear_data. Принимает несколько именнованных и один обязательный аргумент:
    sample_rate - частота дискретезации - целочисленное значение - обязательный параметр
    notch_filter - режекторный фильтр - подаётся кортеж содержащий интервал который будет отфильтрован - по умолчанию обрезает 50+-1 Гц
    low_pass_filter - фильтр пропускающий всё ниже указанной частоты по умолчанию задан значенеим None и неактивен
    
    -------------------------------------------------------------------------------------------------------------------------------------------
    Атрибуты:
    EEGProcess.trend;
    EEGProcess.detrend_data,;
    EEGProcess.del_pick_data;
    Атрибуты можно присвоить любой переменной для дальнейшей работы.

    --------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, EEG_data: list, *, w: int = 1501):

        self.W = w
        self._Half = self.W // 2
        if self.W % 2 == 0:
            self._Half -= 1

        self.EEG_data = EEG_data
        
        self.trend = np.zeros(
            (np.shape(self.EEG_data)[0] - self.W + 1, np.shape(self.EEG_data)[1])
        )
        
        self.detrend_data = np.zeros(
            (np.shape(self.EEG_data)[0] - self.W + 1, np.shape(self.EEG_data)[1])
        )
        
        self.del_pick_data = None
        
        self.clear_data = np.zeros(
            (np.shape(self.EEG_data)[0] - self.W + 1, np.shape(self.EEG_data)[1]), dtype = np.complex128
        )

    # Скользящее среднее
    def _moving_avg(self, x, w):

        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[w:] - cumsum[:-w]) / float(w)

    # вычитание тренда X - исходный ряд, Y - скользящее среднее, W - окно
    def _detrending(self, x, y, w):

        w2 = w // 2
        X_detred = np.subtract(x[w2:len(x)-w2],y)

        return X_detred
    
    #фурье преобразование
    def _fourier(self, x, sample_rate,*, target_hz_1, target_hz_2):
        time_step = 1/sample_rate
        N = len(x)
        #Фурье образ
        yf = rfft(x)
        #Часты
        xf = rfftfreq(N, time_step)[:N//2]
        #Зануляем ненужные частоты
        points_per_gZ = len(xf)/(sample_rate/2)
        #Убираем 50+-1 герц 
        target_GZ_1 = int(points_per_gZ  *  target_hz_1[0])
        target_GZ_2 = int(points_per_gZ  * target_hz_1[1])

        yf[target_GZ_1:target_GZ_2] = 0
        
        if not(target_hz_2 is None):
            target_GZ_3 = int(points_per_gZ  * 99)
            yf[target_GZ_3:] = 0
        
        s = irfft(yf)
        return s
    
    # Расчёт скользящего среднего для указанного ряда 
    def moving_avg(self) -> list:
        # Заполняем таймлайн
        self.trend[:, 0] = self.EEG_data[
            self._Half : len(self.EEG_data) - self._Half, 0
        ]

        for i in range(1, np.shape(self.EEG_data)[1]):
            self.trend[:, i] = self._moving_avg(self.EEG_data[:, i], self.W)

        return self.trend

    # Вычитание тренда
    def detrend(self) -> list:
        #инициализируем значение тренда
        if self.trend.any() == 0:
            self.moving_avg()
        # Заполняем таймлайн
        self.detrend_data[:, 0] = self.EEG_data[
            self._Half : len(self.EEG_data) - self._Half, 0
        ]

        for i in range(1, np.shape(self.EEG_data)[1]):
            self.detrend_data[:, i] = self._detrending(
                self.EEG_data[:, i], self.trend[:, i], self.W
            )

        return self.detrend_data

    # Удаление пиков
    def del_pick(self) -> list:
        self.del_pick_data = self.detrend()
        shape = np.shape(self.del_pick_data)

        for i in range(1, shape[1]):
            for j in range(shape[0] - 1):
                if abs(self.del_pick_data[j, i]) > 1:
                    print(f"удаляю пик{j}")
                    self.del_pick_data[j, i] = (
                        self.del_pick_data[j - 1, i] + self.del_pick_data[j + 1, i]
                    ) / 2

        return self.del_pick_data
    
    def frequency_filter(self, sample_rate: int ,* , notch_filter: tuple = (49,50), low_pass_filter: int = None):
        self.clear_data[:, 0] = self.EEG_data[
            self._Half : len(self.EEG_data) - self._Half, 0
        ]
        
        if self.del_pick_data is None:
            for i in range(1, np.shape(self.detrend_data)[1]):
                self.clear_data[:, i] = self._fourier(self.detrend_data[:, i], sample_rate, target_hz_1 = notch_filter, target_hz_2 = low_pass_filter)
        
        else:
            for i in range(1, np.shape(self.del_pick_data)[1]):
                self.clear_data[:, i] = self._fourier(self.del_pick_data[:, i], sample_rate, target_hz_1 = notch_filter, target_hz_2 = low_pass_filter)
            
        return self.clear_data
                
        

    def plot_ft(self, name_: str, sample_rate: int ,*, line_num = 1, show_all = False):
        """
        Рисует спектр сигналов
        name_ - какую версию сигнала отбразить
        sample_rate - частота дескритезации 
        line_num - если параметр show_all - False - выводит отведение под указанным номером
        show_all - если true - выводит все 4 отведения сигнала
        """
        if name_ == "EEG_data":
            time_step = 1/sample_rate
            
            plot_data = np.zeros(
            (np.shape(self.EEG_data)[0] , np.shape(self.EEG_data)[1])
        )   
            N = len(self.EEG_data[:,0])
            plot_data[:, 0] = fftfreq(N, time_step)#[:N//2]
            
            for i in range(1, np.shape(self.EEG_data)[1]):
                
                #Фурье образ
                plot_data[:, i] = fft(self.EEG_data[:,i])
                #Частоты
            
            

            if show_all:
                
                plt.subplot(4,1,1)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 1]))
                
                plt.subplot(4,1,2)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 2]))
                
                plt.subplot(4,1,3)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 3]))
                
                plt.subplot(4,1,4)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 4]))
                plt.show()
            
            else:
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, line_num]))
                plt.show()
                    
            
            
    
        elif name_ == "detrend_data":
            time_step = 1/sample_rate
            
            plot_data = np.zeros(
            (np.shape(self.detrend_data)[0], np.shape(self.detrend_data)[1]), dtype = np.complex128
        )
            N = len(self.detrend_data)
            plot_data[:, 0] = fftfreq(N, time_step)#[:N//2]
            
            for i in range(1, np.shape(self.detrend_data)[1]):
                #Фурье образ
                plot_data[:, i] = fft(self.detrend_data[:,i])
            
            

            if show_all:
                
                plt.subplot(4,1,1)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 1]))
                
                plt.subplot(4,1,2)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 2]))
                
                plt.subplot(4,1,3)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 3]))
                
                plt.subplot(4,1,4)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 4]))
                plt.show()
            
            else:
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, line_num]))
                plt.show()
                    
            
        elif name_ == "clear_data":
            time_step = 1/sample_rate
            
            plot_data = np.zeros(
            (np.shape(self.clear_data)[0], np.shape(self.clear_data)[1]), dtype = np.complex128
        )
            N = len(self.clear_data)
            plot_data[:, 0] = fftfreq(N, time_step)#[:N//2]
            for i in range(1, np.shape(self.clear_data)[1]):
                #Фурье образ
                plot_data[:, i] = fft(self.clear_data[:,i])

            
            

            if show_all:
                
                plt.subplot(4,1,1)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 1]))
                
                plt.subplot(4,1,2)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 2]))
                
                plt.subplot(4,1,3)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 3]))
                
                plt.subplot(4,1,4)
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, 4]))
                plt.show()
            
            else:
                plt.plot(plot_data[:N//2, 0], 2./N * np.abs(plot_data[0:N//2, line_num]))
                plt.show()
            
            
            
        
        

def furier(X, sample_rate):
    time_step = 1/sample_rate
    N = len(X)
    #Фурье образ
    yf = fft(X)
    #Часты
    xf = fftfreq(N, time_step)[:N//2]
    
    #Зануляем ненужные частоты
    points_per_gZ = len(xf)/(sample_rate/2)
    #Убираем 50+-1 герц 
    target_GZ_1 = int(points_per_gZ  * 49)
    target_GZ_2 = int(points_per_gZ  * 51)
    target_GZ_3 = int(points_per_gZ  * 99)
    yf[target_GZ_1:target_GZ_2] = 0
    yf[target_GZ_3:] = 0
    
    #убираем всё от 99 герц

    plt.plot(xf, 2./N * np.abs(yf[0:N//2]))
    plt.show()
    
    return ifft(yf)
        