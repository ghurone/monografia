import os


def criar_pasta(dir_path:str, debug:bool=True) -> None:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        if debug:
            print(f'A pasta "{os.path.basename(dir_path)}" foi criada com sucesso!')
    else:
        if debug:
            print(f'A pasta "{os.path.basename(dir_path)}" já existe!')