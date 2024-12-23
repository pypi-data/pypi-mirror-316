'''
Перечисления для настройки целевой платформы
для компиляции
'''

from enum import Enum


class Arch(Enum):
    '''
    Архитектуры проецессоров
    '''
    # Intel / AMD
    I386 = 'i386'
    X86_64 = 'x86_64'
    
    # ARM
    ARM = 'arm'
    ARMV7 = 'armv7'
    AARCH64 = 'aarch64'
    
    # RISC-V
    RISCV32 = 'riscv32'
    RISCV64 = 'riscv64'

    # MSPS
    MIPS = 'mips'
    MIPS64 = 'mips64'

    # PowerPC
    POWERPC = 'powerpc'
    POWERPC64LE = 'powerpc64le'


class Vendor(Enum):
    '''
    Производители аппаратного обеспечения
    '''
    PC = 'pc'
    APPLE = 'apple'
    UNKNOWN = 'unknown'
    EABI = 'eabi'


class OS(Enum):
    # Стандартные системы ПК
    WINDOWS = 'windows'
    LINUX = 'linux'
    DARWIN = 'darwin'
    
    # BSD системы
    FREEBSD = 'freebsd'
    NETBSD = 'netbsd'
    OPENBSD = 'openbsd'

    # Для bare-metal приложений
    NONE = 'none'


class ABI(Enum):
    MINGW = 'mingw'
    GNU = 'gnu'
    GNUEABIHF = 'gnueabihf'
    MSVC = 'msvc'
    ELF = 'elf'


# Тип цели
type Target_T = tuple[Arch, Vendor, OS, ABI]
