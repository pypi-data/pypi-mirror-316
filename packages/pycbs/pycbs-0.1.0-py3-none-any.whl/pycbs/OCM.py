'''
OCM [Object-Command Mapping] - объектно-коммандное отображение
'''

import os
from enum import Enum
from rich import print as rprint


def CheckFile(file):
    if not os.path.exists(file):
        rprint(f'[red bold]Ошибка: указанный путь [green]"{file}"[/] [red bold]- не существует![/]')
        exit(1)

    if not os.path.isfile(file):
        rprint(f'[red bold]Ошибка: указанный путь [green]"{file}"[/] [red bold]- не существует![/]')
        exit(1)


def ToAsm(file: str):
    CheckFile(file)
    os.system(f'clang -S {file}')


def ToObj(file: str, endFile: str):
    CheckFile(file)
    os.system(f'clang {file} -o {endFile}')
