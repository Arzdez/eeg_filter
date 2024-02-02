import numpy as np
import mplcatppuccin
from mplcatppuccin.palette import load_color
import matplotlib as mpl
import matplotlib.pyplot as plt


def ploter(
    data: list,
    *,
    time_in_data: bool = True,
    sample_rate: int = 1000,
    figsize: tuple = (18, 9),
    save: bool =False,
    filename: str ="Figure",
    title: list = None,
    theme: bool = False,
    color: str = "black",
):
    """
    Принимает на вход n-мерный массив data и строит визуализацию;
    time - Положение True говорит о том что временную шкалу нужно брать из переданного массива
    False - Тогда вызовется генератор временной шкалы с помощью linspace;
    figsize - Размер фигуры;
    filename- Имя фигуры для сохранения;
    title - принимает значения с именами каналов, по умолчанию - None, зназвание каналов по умолчанию channel+num_chanel
    
    """
    num_of_rows = min(np.shape(data))
    print(np.shape(data))

    #Проверка флага наличия врменной лоинии в отправленном масиве
    if not time_in_data:
        time_line = np.linspace(0, len(data) / sample_rate, len(data)) #TODO заменить на np.arange()
        start_index = 0
        num_of_rows_sub = num_of_rows

    else:
        time_line = data[:, 0]
        num_of_rows_sub = num_of_rows - 1
        start_index = 1
        
    if theme:
        mpl.style.use("mocha")
        color = load_color("mocha", "green")

    num_changer = 0
    plt.figure(figsize=figsize)
    for i in range(start_index, num_of_rows):
        plt.subplot(num_of_rows_sub, 1, num_changer + 1)

        if title is not None:
            print(title[num_changer])
            plt.title(title[num_changer])



        plt.grid()
        plt.xlabel("time,c")
        plt.ylabel("U, мВ")
        plt.plot(time_line, data[:, i],color=color)
        num_changer += 1

    plt.tight_layout()
    if save:
        plt.savefig(filename + ".pdf")
    plt.show()