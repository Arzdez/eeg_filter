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

    frequency_filter - фильтр частот - self.clear_data. Принимает несколько именнованных и один обязательный аргумент:
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

        self.del_pick_data = None

        self.clear_data = np.zeros(
            (np.shape(self.eeg_data)[0] - self.W + 1, np.shape(self.eeg_data)[1]),
            dtype=np.complex128,
        )

    # Скользящее среднее
    def _moving_avg(self, x, w):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[w:] - cumsum[:-w]) / float(w)

    # вычитание тренда X - исходный ряд, Y - скользящее среднее, W - окно
    def _detrending(self, x, y, w):
        w2 = w // 2
        x_detred = np.subtract(x[w2 : len(x) - w2], y)

        return x_detred

    # фурье преобразование
    def _fourier(self, x, sample_rate, *, target_hz_1, target_hz_2):
        time_step = 1 / sample_rate
        N = len(x)
        # Фурье образ
        yf = rfft(x)
        # Часты
        xf = rfftfreq(N, time_step)[: N // 2]
        # Зануляем ненужные частоты
        points_per_gz = len(xf) / (sample_rate / 2)
        # Убираем 50+-1 герц
        target_gz_1 = int(points_per_gz * target_hz_1[0])
        target_gz_2 = int(points_per_gz * target_hz_1[1])

        yf[target_gz_1:target_gz_2] = 0

        if target_hz_2 is not None:
            target_gz_3 = int(points_per_gz * 99)
            yf[target_gz_3:] = 0

        s = irfft(yf)
        return s

    # Расчёт скользящего среднего для указанного ряда
    def moving_avg(self) -> list:
        # Заполняем таймлайн
        self.trend[:, 0] = self.eeg_data[
            self._half : len(self.eeg_data) - self._half, 0
        ]

        for i in range(1, np.shape(self.eeg_data)[1]):
            self.trend[:, i] = self._moving_avg(self.eeg_data[:, i], self.W)

        return self.trend

    # Вычитание тренда
    def detrend(self) -> list:
        # инициализируем значение тренда
        if self.trend.any() == 0:
            self.moving_avg()
        # Заполняем таймлайн
        self.detrend_data[:, 0] = self.eeg_data[
            self._half : len(self.eeg_data) - self._half, 0
        ]

        for i in range(1, np.shape(self.eeg_data)[1]):
            self.detrend_data[:, i] = self._detrending(
                self.eeg_data[:, i], self.trend[:, i], self.W
            )

        return self.detrend_data

    # Удаление пиков
    def del_pick(self) -> list:
        self.del_pick_data = self.detrend()
        shape = np.shape(self.del_pick_data)
        w_pick_find = 60  # Окно поиска пиков
        print(shape)
        for i in range(1, shape[1]):
            for j in range(w_pick_find, shape[0] - w_pick_find):
                chek_sum = 0  # накопление суммы вокруг точки
                for k in range(j - (w_pick_find // 2), j + (w_pick_find // 2)):
                    if k == j:
                        continue
                    chek_sum += abs(self.del_pick_data[k, i])
                # print(chek_sum/w_pick_find)
                if abs(self.del_pick_data[j, i]) > chek_sum:
                    print(f"удаляю пик {j}")
                    self.del_pick_data[j, i] = (
                        self.del_pick_data[j - 1, i] + self.del_pick_data[j + 1, i]
                    ) / 2

        return self.del_pick_data

    def frequency_filter(
        self,
        sample_rate: int,
        *,
        notch_filter: tuple = (49, 51),
        low_pass_filter: int = 99,
    ):
        self.clear_data[:, 0] = self.eeg_data[
            self._half : len(self.eeg_data) - self._half, 0
        ]

        if self.del_pick_data is None:
            if self.detrend_data.any() == 0:
                self.detrend()
            for i in range(1, np.shape(self.detrend_data)[1]):
                self.clear_data[:, i] = self._fourier(
                    self.detrend_data[:, i],
                    sample_rate,
                    target_hz_1=notch_filter,
                    target_hz_2=low_pass_filter,
                )

        else:
            if self.del_pick_data is None:
                self.del_pick()
            for i in range(1, np.shape(self.del_pick_data)[1]):
                self.clear_data[:, i] = self._fourier(
                    self.del_pick_data[:, i],
                    sample_rate,
                    target_hz_1=notch_filter,
                    target_hz_2=low_pass_filter,
                )

        return self.clear_data
