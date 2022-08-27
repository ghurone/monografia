import os


def criar_pasta(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        print(f'A pasta "{os.path.basename(dir_path)}" já existe!')