'''
PyCBS - пакет для обеспечения удобдного механизма
сборки проектов для языка Си через Python пакет
'''

from .Target import (
    # Enums
    Arch,
    Vendor,
    OS,
    ABI,

    # Типы
    Target_T,
)

from .ClangBuild import (
    # Enums
    CompileModes,
    Linker,
    Language,
    TargetArch,
    OptimizationMode,

    # Константы
    DEFAULT,

    # Функции для сборки
    ClangBuild,
)

from .LangSTD import (
    C_STD,
    LangStandart
)

from . import Windows
from . import OCM
