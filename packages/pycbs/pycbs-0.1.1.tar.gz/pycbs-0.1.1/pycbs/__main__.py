import os
import sys

from rich import print as rprint


HELLO_TEST = '''
[green]Привет! Это CLI сборщик на Python - PyCBS 0.1.0[/]

[yellow bold]⚠ На данный момент достуна сборка только для clang![/]
[yellow bold]⚠ На данный момент поддержка ориентированна на Windows![/]

[violet]Параметры:[/]
[grey]*[/] [bold]init full[/] - [green]инициализарует полный файл сборки в вашей директории[/]
[grey]*[/] [bold]init[/] - [green]инициализарует минимальный файл сборки в вашей директории[/]

[green]Чтобы начать сборку проекта, просто запустите "pmake.py" файл![/]
'''[1:-1]


PMAKE_MIN_CODE = '''
from pycbs import *


ClangBuild()

'''[1:-1]

PMAKE_FULL_CODE = '''
from pycbs import *


ClangBuild (
    # Пути к папкам с библиотеками
    headerPaths = [],
    libsPaths = [],
    
    # Файлы для сборки
    libs = [],
    startFile = 'main.c',
    
    # Настройки компиляции
    linker = Linker.LLVM,
    target = ClangBuild,

    # Настройки языыка
    lang = Language.C,
    targetArch = TargetArch.M64,
    optimization = OptimizationMode.NONE
)

'''[1:-1]


if __name__ == '__main__':
    thisPath = os.getcwd()

    match sys.argv:
        case [_, 'init', 'full']:
            with open('pmake.py', 'w', encoding='utf-8') as file:
                file.write(PMAKE_FULL_CODE)

        case [_, 'init']:
            with open('pmake.py', 'w', encoding='utf-8') as file:
                file.write(PMAKE_MIN_CODE)

        case _:
            rprint(HELLO_TEST)
