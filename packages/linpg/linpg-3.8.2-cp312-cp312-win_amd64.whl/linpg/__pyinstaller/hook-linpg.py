import os, linpg

_PATH: str = linpg.__path__[0]
_NAME: str = "linpg"

hiddenimports = ['PIL.Image', 'PIL.ImageColor', 'PIL.ImageFilter', 'av', 'numpy', 'pygame', 'pygame.gfxdraw', 'pyvns', 'tkinter', 'tkinter.messagebox']

datas: list[tuple[str, str]] = []
ignores: tuple[str, ...] = ("__pyinstaller", "__pycache__", ".git")

# append all files/folders into datas
for file_name in os.listdir(_PATH):
    abs_path: str = os.path.join(_PATH, file_name)
    # append all folders into datas
    if os.path.isdir(abs_path):
        # if no ignore key appear in the given file name
        if not any(folder_name_t in file_name for folder_name_t in ignores):
            # then add it to list
            datas.append((abs_path, os.path.join(_NAME, file_name)))
    # append all file (except gitignore) into datas
    elif "gitignore" not in file_name:
        datas.append((abs_path, _NAME))
