from enum import Enum


class C_STD(Enum):
    C89 = 'c89'
    C99 = 'c99'
    C11 = 'c11'
    C17 = 'c17'
    C23 = 'c23'


type LangStandart = C_STD
