import os
import time
from shutil import copytree
import bz2


# @deco_time
def comma_to_dot(
    path_data: str, *,
    flag_reduce: bool = False
    ):
    """
    Заменяет все запятые на точки в файле прербразованном из PGC
    Если параметр flag_reduce = True - тогда обрезает шапку которая по умолчанию
    в PGC занимает 4 строки
    """
    # Костыль, обрезает шапку если флаг = 1
    reduce = 0
    if flag_reduce:
        reduce = 4

    if not os.path.exists(path_data):
        raise FileExistsError("invalid path")

    os.chdir(path_data)

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print("Обрабатывается файл:" , os.path.join(root, name))
            file = open(os.path.join(root, name), "r")
            text = file.readlines()

            for i in range(len(text)):
                text[i] = text[i].replace(",", ".")
            file.close()

            file = open(os.path.join(root, name), "w")
            file.writelines(text[reduce:])
            file.close()


# path_data,path_archive пути до данных и до папки где будут храниться архивные данные
def txt_to_zip(
    path_data: str,
    path_archive: str
    ):
    """
    Запаковывает  данные в формат Bz2 из пути path_data по пути Path_archive
    Если папка Path_archive существует  выполнение прекращается
    воизбежание повторной архивации данных
    """
    os.chdir(path_data)
    # проверяем создана ли папка с архивами т Копируем всё содержимое папки с данными в неё, и меняем директорию
    try:
        copytree(path_data, path_archive)
        os.chdir(path_archive)

    except FileExistsError:
        print("Папка уже существует, измените место либо удалите существющую папку")
        return 0

    # создаём архив и удалем текстовые
    for root, dirs, files in os.walk(".", topdown=False):

        for name in files:

            # Открываем файлы
            file_in = open(os.path.join(root, name), "rb")
            file_out = bz2.open(
                os.path.join(root, name.replace(".txt", "")) + ".bz2", "wb"
            )

            file_out.write(file_in.read())
            file_in.close()
            file_out.close()

            # Удаляем запакованный файл
            os.remove(os.path.join(root, name))
