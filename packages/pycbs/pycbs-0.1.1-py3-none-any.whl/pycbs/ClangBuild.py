'''
Главный пакет с функциями для сборки проектов
'''

import os
import sys

from enum import Enum

from .Target import *
from .LangSTD import *

from rich import print as rprint


DEFAULT = None


class CompileModes(Enum):
    OBJECT = '-o'
    COMPILE = '-c'
    PREPROCESSING = '-E'
    ASM_CODE = '-S'


class Linker(Enum):
    LLVM = 'lld'


class Language(Enum):
    C = 'c'


class TargetArch(Enum):
    M32 = 'm32'
    M64 = 'm64'


class OptimizationMode(Enum):
    NONE = '-O0'
    LVL_1 = '-O1'
    LVL_2 = '-O2'
    LVL_3 = '-O3'
    MIN_SIZE = '-Os'
    FAST = '-Oz'


def ClangBuild(
        # Пути к папкам с библиотеками
        includePaths: list[str] = DEFAULT,
        libsPaths: list[str] = DEFAULT,
        
        # Файлы для сборки
        libs: list[str] = DEFAULT,
        startFile: list[str] = 'main.c',
        endFile: list[str] = DEFAULT,
        
        # Настройки компиляции
        linker: Linker = DEFAULT,
        target: tuple[Arch, Vendor, OS, ABI] = DEFAULT,

        # Платформенная компиляция
        native: bool = True,

        # Настройки языка
        lang: Language = DEFAULT,
        targetArch: TargetArch = DEFAULT,
        optimization: OptimizationMode = DEFAULT,
        std: LangStandart = DEFAULT,
):
    '''
    Функция для реализации сборки проектов на clang
    '''

    rprint(f'[blue bold]Лог: начало сборки проекта...[/]')

    # Проверка на правильность указанных путей
    if includePaths and libsPaths:
        for path in includePaths + libsPaths:
            if not os.path.exists(path):
                rprint(f'[red bold]Ошибка: указанный путь [green]"{path}"[/] [red bold]- не существует![/]')
                exit(1)
    
    # Проверка на правильность файла "startFile"
    if not os.path.exists(startFile):
        rprint(f'[red bold]Ошибка: startFile [green]"{startFile}"[/] [red bold]- не существует![/]')
        exit(1)

    if not os.path.isfile(startFile):
        rprint(f'[red bold]Ошибка: startFile [green]"{startFile}"[/] [red bold]- не файл![/]')
        exit(1)
    
    # Подключения
    resultIncludePaths = ''
    resultLibsPaths = ''
    resultEndFile = ''

    if includePaths:
        temp = [f' -I"{path}"' for path in includePaths]
        resultIncludePaths = ''.join(temp)
    
    if libsPaths:
        temp = [f' -L"{path}"' for path in libsPaths]
        resultLibsPaths = ''.join(temp)
    
    if endFile:
        resultEndFile = f' -o {endFile}'
    
    # Парсинг tanget
    resultTarget = ''
    
    if target:
        resultTarget = f'{target[0]}-{target[1]}-{target[2]}'

        if target[3]:
            resultTarget += f'-{target[3]}'

        return f' --target=' + resultTarget

    # Подключение статических библиотек
    resultLibs = ''

    if libs:
        temp = [f' -l"{lib}"' for lib in libs]
        resultLibsPaths = ''.join(temp)

    resultCommand = (
        f'clang '
        + startFile
        + resultEndFile
        + resultIncludePaths
        + resultLibsPaths
        + ( f' -fuse-ld={linker}' if linker else '' )
        + resultTarget
        + resultLibs
        + ( f' -std={std}' if std else '' )
        + ( f' -x {lang}' if lang else '' )
        + ( f' {targetArch}' if targetArch else '' )
        + ( f' {optimization}' if optimization else '' )
        + ( f' -march=native' if native else '' )
    )

    rprint(f'[blue bold]Лог: проект был собра, исходная команда:\n[/]')
    rprint(f'[green]{resultCommand}\n[/]')

    rprint(f'[yellow]=> Компиляция с помощью clang:\n[/]')

    os.system(resultCommand)

    rprint(f'\n[yellow]=> Компиляция завершена![/]')
