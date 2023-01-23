import numpy as np
from statistics import mean


class EegFilter:
    """
    Класс предобработки ЭЭГ
    На вход подаётся файл ЭЭГ для которого создаётся экземпляр класса и при желании размер окна w - !!именованный аргумент!!, значение по умолчанию 1501.

    После можно вызывать нужные методы
    _moving_avg и _detrending - вспомагательные методы, считают скользящую среднюю и вычитают тренд соответсвенно



    S_moving_avg- метод считает и возвращает скользящуюю среднюю - self.trend
    detrend - метод вычитает тренд и взворащает детрендированный ряд но единичные пики не удаляются - self.detrend_data
    del_pick - метод удаляет резкие пики -  self.del_pick_data
    get_data - метод возвращает кортеж  1 эллемент - тренд , 2 детрендированные данные без еденичных пиков
    -------------------------------------------------------------------------------------------------------------------------------------------
    All_processing - вызывает  S_moving_avg, detrend, del_pick
    и позволяет обращаться ко всем вышеописанным атрибутам для дальнейшей работы:
    EEGProcess.trend;
    EEGProcess.detrend_data,;
    EEGProcess.del_pick_data;
    Атрибуты можно присвоить любой переменной для дальнейшей работы.

    Сам метод All_processing  вызывает метод del_pick - поскольку обрабокта последовательная - каждый  метод вызывает метод находящийся над ним.
    Метод создан для удобства и ничего не возвращает.
    --------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, EEG_data: list, *, w: int = 1501):

        self.W = w
        self._Half = int(self.W / 2)
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

    # Скользящее среднее
    def _moving_avg(self, x, w=1501):

        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[w:] - cumsum[:-w]) / float(w)

    # вычитание тренда X - исходный ряд, Y - скользящее среднее, W - окно
    def _detrending(self, x, y, w):

        w2 = int(w / 2)
        X_detred = np.subtract(x[w2:len(x)-w2],y)

        return X_detred

    # Расчтё скользящего среднего для указанного ряда
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
        # инициализируем значение тренда
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
            # Если пик в 100000 раз больше среднего - удаляем
            means = 100000 * mean(self.del_pick_data[:, i])
            #print(means)

            for j in range(shape[0] - 1):
                if self.del_pick_data[j, i] > means:
                    # print("удаляю пик")
                    self.del_pick_data[j, i] = (
                        self.del_pick_data[j - 1, i] + self.del_pick_data[j + 1, i]
                    ) / 2

        return self.del_pick_data

    def get_data(self) -> tuple:
        if self.del_pick_data == None:
            self.del_pick()
        return (self.trend, self.del_pick_data)

    def all_processing(self) -> None:
        self.del_pick()
