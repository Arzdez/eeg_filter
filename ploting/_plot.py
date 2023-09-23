import numpy as np
import matplotlib.pyplot as plt


def ploter(
    data,
    *,
    time_in_data=True,
    sample_rate=1000,
    figsize=(18, 9),
    save=False,
    filename="Figure",
    title=None,
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

    num_changer = 0
    plt.figure(figsize=figsize)
    for i in range(start_index, num_of_rows):
        plt.subplot(num_of_rows_sub, 1, num_changer + 1)

        if title is None:
            plt.title(f"Channel {num_changer+1}")
        else:
            print(title[num_changer])
            plt.title(title[num_changer])

        plt.grid()
        plt.plot(time_line, data[:, i])
        num_changer += 1

    plt.tight_layout()
    if save:
        plt.savefig(filename + ".pdf")
    plt.show()


if __name__ == "__main__":
    x = np.loadtxt(r"RD_Cx_L+.txt")
    title = ["a","b","c",'d','e']
    ploter(x, time_in_data=False, title=title, save=True)
