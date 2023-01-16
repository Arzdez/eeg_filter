import numpy as np
import matplotlib.pyplot as plt
import os
import shutil




#@deco_time
def png_ploting(path: str) -> None:
    """Создаёт график 4ёх каналов файла PGC и схораняет в PNG"""
    chanels = ["time", "Cd R", "Cd L", "Cx occip R", "Cx occip L"]
    os.chdir(path)

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if "trend" in name and "baseline" not in name:
                input_data = np.loadtxt(os.path.join(root, name))
                print(os.path.join(root, name))
                # Сохранение графиков
                plt.suptitle(root + name)
                plt.subplot(4, 1, 1)
                plt.title(f"{chanels[1]}")
                plt.plot(input_data[:, 0], input_data[:, 1])

                plt.subplot(4, 1, 2)
                plt.title(f"{chanels[2]} ")
                plt.plot(input_data[:, 0], input_data[:, 2])

                plt.subplot(4, 1, 3)
                plt.title(f"{chanels[3]} ")
                plt.plot(input_data[:, 0], input_data[:, 3])

                plt.subplot(4, 1, 4)
                plt.title(f"{chanels[4]} ")
                plt.plot(input_data[:, 0], input_data[:, 4])

                plt.tight_layout()
                plt.savefig(
                    os.path.join(root, name.replace(".txt", ""))
                    + root.replace("\\", "_")
                    + f"_sum.png",
                    dpi=1000,
                )
                plt.close()
    return None


def copy_sum_gruph(path_data: str, path_copy: str) -> None:
    """Копирует общий график по указанному пути для удобства"""
    os.chdir(path_data)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if "sum" in name and "detrend" not in name:
                shutil.copy(os.path.join(root, name), path_copy)
                

def copy_detrend_gruph(path_data: str, path_copy: str) -> None:
    """ Копирует детрендированные копии сигналов по указанному пути для удобства анализа"""
    os.chdir(path_data)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if "detrend.txt" in name:
                shutil.copy(os.path.join(root, name), path_copy)
    


def ploter(X: list) -> None:
    """
    Рисует 4 канала данных из PGC
    """
    chanels = ["time", "Cd R", "Cd L", "Cx occip R", "Cx occip L"]
    #X = np.loadtxt(path)
    plt.subplot(4, 1, 1)
    plt.title(f"{chanels[1]}")
    plt.plot(X[:, 0], X[:, 1])
    
    plt.subplot(4, 1, 2)
    plt.title(f"{chanels[2]} ")
    plt.plot(X[:, 0], X[:, 2])
    
    plt.subplot(4, 1, 3)
    plt.title(f"{chanels[3]} ")
    plt.plot(X[:, 0], X[:, 3])
    
    plt.subplot(4, 1, 4)
    plt.title(f"{chanels[4]} ")
    plt.plot(X[:, 0], X[:, 4])
    
    plt.tight_layout()
    plt.savefig("graph.png",dpi=1000)
    plt.show()