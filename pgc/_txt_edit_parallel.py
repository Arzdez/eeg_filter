import os
import time
from shutil import copytree
import bz2
import multiprocessing as mp 
from functools import partial

def _ctd(path,*, comment_line = 4):

    print("Обрабатывается файл:" , path)
    files = open(path, "r")
    text = files.readlines()

    for i in range(len(text)):
        text[i] = text[i].replace(",", ".")
            
    for i in range(comment_line):
        text[i] = '#'+text[i]
                
    files.close()

    files = open(path, "w")
    files.writelines(text)
    files.close()
    

def comma_to_dot_parallel(
    path_data: str, *,
    comment_line = 4
    ):
    """
    Заменяет все запятые на точки в файле прербразованном из PGC
    Если параметр comment_line- колличество строк к которым унжно добавить знак комментария
    в PGC занимает 4 строки
    вариант с параллельной обрботкой. Поумолчанию берётся значение 7 процессов, для 8 ядерных машин - оптимально
    """
    
    path_tuple = []
    thread = 16

    if not os.path.exists(path_data):
        raise FileExistsError("invalid path")

    os.chdir(path_data)

    part_ctd = partial(_ctd, comment_line = comment_line)
    
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            path_tuple.append(os.path.join(root, name))
    
    

    
    with mp.Pool(processes = thread ) as work:
        work.map(part_ctd, path_tuple)
        
        
        

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
                os.path.join(root, name.replace(".txt", "")) + ".bz2", "wb"
            )

            file_out.write(file_in.read())
            file_in.close()
            file_out.close()

            # Удаляем запакованный файл
            os.remove(os.path.join(root, name))
