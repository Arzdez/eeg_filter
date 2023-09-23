import os
import time
from shutil import copytree
import bz2


def comma_to_dot(
    path_data: str, *,
    comment_line = 4
    ):
    """
    Заменяет все запятые на точки в файле прербразованном из PGC
    Если параметр comment_line- колличество строк к которым унжно добавить знак комментария
    в PGC занимает 4 строки
    """

    if not os.path.exists(path_data):
        raise FileExistsError("invalid path")

    os.chdir(path_data)

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print("Обрабатывается файл:" , os.path.join(root, name))
            files = open(os.path.join(root, name), "r")
            text = files.readlines()

            for i in range(len(text)):
                text[i] = text[i].replace(",", ".")
            
            for i in range(comment_line):
               text[i] = '#'+text[i]
                
            files.close()

            files = open(os.path.join(root, name), "w")
            files.writelines(text)
            files.close()


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
            print("Обрабатывается файл:" , os.path.join(root, name))
            # Открываем файлы
            file_in = open(os.path.join(root, name), "rb")
            file_out = bz2.open(
                os.path.join(root, name) + ".bz2", "wb"
            )

            file_out.write(file_in.read())
            file_in.close()
            file_out.close()

            # Удаляем запакованный файл
            os.remove(os.path.join(root, name))
