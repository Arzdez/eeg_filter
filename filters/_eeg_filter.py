import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from scipy.fft import rfft, irfft, rfftfreq


class EegFilter:
    """
    Класс предобработки ЭЭГ
    На вход подаётся файл ЭЭГ для которого создаётся экземпляр класса и при желании размер окна w - !!именованный аргумент!!, значение по умолчанию 1501.

    После можно вызывать нужные методы
    _moving_avg ,_fourier  и _detrending - вспомагательные методы, считают скользящую среднюю, фурье образ и вычитают тренд, соответсвенно



    moving_avg- метод считает и возвращает скользящуюю среднюю - self.trend
    detrend - метод вычитает тренд и взворащает детрендированный ряд но единичные пики не удаляются - self.detrend_data

    frequency_filter - фильтр частот - self.clear_data. Принимает несколько именнованных и один обязательный аргумент:
        sample_rate - частота дискретезации - целочисленное значение - обязательный параметр
        notch_filter - режекторный фильтр - подаётся кортеж содержащий интервал который будет отфильтрован - по умолчанию обрезает 50+-1 Гц
        
    low_pass_filter - фильтр пропускающий всё ниже указанной частоты по умолчанию задан значенеим None и неактивен



    -------------------------------------------------------------------------------------------------------------------------------------------
    Атрибуты:
    EEGProcess.trend;
    EEGProcess.detrend_data,;

    --------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, eeg_data: list, *, w: int = 1501):
        self.W = w
        self._half = self.W // 2
        if self.W % 2 == 0:
            self._half -= 1

        self.eeg_data = eeg_data

        self.trend = np.zeros(
            (np.shape(self.eeg_data)[0] - self.W + 1, np.shape(self.eeg_data)[1])
        )

        self.detrend_data = np.zeros(
            (np.shape(self.eeg_data)[0] - self.W + 1, np.shape(self.eeg_data)[1])
        )

        self.clear_data = np.zeros(
            (np.shape(self.eeg_data)[0] - self.W + 1, np.shape(self.eeg_data)[1]),
            dtype=np.complex128,
        )

    # Скользящее среднее - ОПТИМАЛЬНО
    def _moving_avg(self, x: list, w: int) -> list:
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[w:] - cumsum[:-w]) / float(w)

    # Фурье преобразование
    def _fourier(self, x: list, sample_rate: int, *, notch_filter: tuple, low_pass_filter: int) -> np.array:
        time_step = 1 / sample_rate
        N = len(x)
        # Фурье образ
        yf = rfft(x)
        # Частоты
        xf = rfftfreq(N, time_step)[: N // 2]
        # Зануляем ненужные частоты
        points_per_gz = len(xf) / (sample_rate / 2)
        # Убираем 50+-1 герц
        notch_target_gz_1 = int(points_per_gz * notch_filter[0])
        notch_target_gz_2 = int(points_per_gz * notch_filter[1])

        yf[notch_target_gz_1:notch_target_gz_2] = 0

        if low_pass_filter is not None:
            target_gz_3 = int(points_per_gz * 99)
            yf[target_gz_3:] = 0

        final = irfft(yf)
        return final

    # Расчёт скользящего среднего для указанного ряда
    def moving_avg(self):
        for i in range(1, np.shape(self.eeg_data)[1]):
            self.trend[:, i] = self._moving_avg(self.eeg_data[:, i], self.W)

        return self.trend

    # Вычитание тренда
    def detrend(self):
        # Инициализируем расчёт тренда если не был вызван соответсвующий метод
        if self.trend.any() == 0:
            self.moving_avg()    
        self.detrend_data = np.subtract(self.eeg_data[self._half:-self._half], self.trend)
        
        return self.detrend_data


    def frequency_filter(
        self,
        sample_rate: int,
        *,
        notch_filter: tuple = (49, 51),
        low_pass_filter: int = 99,
    ):
        self.clear_data[:, 0] = self.eeg_data[self._half : len(self.eeg_data) - self._half, 0]

        
        if self.detrend_data.any() == 0:
            self.detrend()
            
        for i in range(1, np.shape(self.detrend_data)[1]):
            self.clear_data[:, i] = self._fourier(
                self.detrend_data[:, i],
                sample_rate,
                notch_filter=notch_filter,
                low_pass_filter=low_pass_filter,
                )


        return self.clear_data
