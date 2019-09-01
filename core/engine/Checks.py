from typing import Optional
from core.engine import Errors


class Checks(Errors):
    """Базовый интерфейс подсистемы проверки данных."""

    ERR_PREFIX = 'Ошибка проверки данных'
    BOOL_CAST_TO_FALSE = frozenset((
        '0', 'false', 'no', 'n', 'нет', 'н', 'off',
    ))

    TPL_STR_ERR = 'параметр "%s" должен быть строкой'
    TPL_STR_NONE = 'параметр "%s" не указан, но должен быть строкой'
    TPL_STR_EMPTY = 'параметр "%s" должен быть непустой строкой'

    TPL_INT_ERR = 'параметр "%s" должен быть целым числом'
    TPL_INT_NONE = 'параметр "%s" не указан, но должен быть целым числом'
    TPL_INT_NEGATIVE = 'параметр "%s" не может быть меньше нуля'

    TPL_FLOAT_ERR = 'параметр "%s" должен быть дробным числом'
    TPL_FLOAT_NONE = 'параметр "%s" не указан, но должен быть дробным числом'
    TPL_FLOAT_NEGATIVE = 'параметр "%s" не может быть меньше нуля'

    TPL_BOOL_NONE = 'параметр "%s" не указан, но должен быть логического типа'

    # Публичные методы

    @classmethod
    def check_str(
            cls, data: object, arg: str,
            allow_empty: bool = False, allow_none: bool = False,
    ) -> Optional[str]:
        """Проверка строки.

        :param object data:         Данные, предположительно строка
        :param str arg:             Имя проверяемого параметра
        :param bool allow_empty:    Флаг разрешения пустой строки
        :param bool allow_none:     Флаг допустимости None
        :rtype:                     str|None
        """
        if data is None:
            if allow_none:
                return None
            else:
                cls.error(cls.TPL_STR_NONE % arg)
        elif not isinstance(data, str):
            # todo: подумать - возмоно приводить к строке прочие типы?
            cls.error(cls.TPL_STR_ERR % arg)
        elif not data:
            if allow_empty:
                return ''
            else:
                cls.error(cls.TPL_STR_EMPTY % arg)
        return data

    @classmethod
    def check_int(
            cls, data: object, arg: str,
            allow_negative: bool = False, allow_none: bool = False,
    ) -> Optional[int]:
        """Проверка на целое число.

        :param object data:         Данные, предположительно строка
        :param str arg:             Имя проверяемого параметра
        :param bool allow_negative: Флаг разрешения отрицательных значений
        :param bool allow_none:     Флаг допустимости None
        :rtype:                     int|None
        """
        if data is None:
            if allow_none:
                return None
            else:
                cls.error(cls.TPL_INT_NONE % arg)
        try:
            number = int(data)
        except Exception:
            cls.error(cls.TPL_INT_ERR % arg)
        if allow_negative or number >= 0:
            return number
        else:
            cls.error(cls.TPL_INT_NEGATIVE % arg)

    @classmethod
    def check_float(
            cls, data: object, arg: str,
            allow_negative: bool = False, allow_none: bool = False,
    ) -> Optional[float]:
        """Проверка на дробное число.

        :param object data:         Данные, предположительно число
        :param str arg:             Имя проверяемого параметра
        :param bool allow_negative: Флаг разрешения отрицательных значений
        :param bool allow_none:     Флаг допустимости None
        :rtype:                     float|None
        """
        if data is None:
            if allow_none:
                return None
            else:
                cls.error(cls.TPL_FLOAT_NONE % arg)
        try:
            number = float(data)
        except Exception:
            cls.error(cls.TPL_FLOAT_ERR % arg)
        if allow_negative or number >= 0:
            return number
        else:
            cls.error(cls.TPL_FLOAT_NEGATIVE % arg)

    @classmethod
    def check_bool(
            cls, data: object, arg: str,
            smart: bool = True, allow_none: bool = False,
    ) -> Optional[bool]:
        """Проверка логического типа.

        :param object data:     Данные, предположительно логический тип
        :param str arg:         Имя проверяемого параметра
        :param bool smart:      Флаг распознавания из строки
        :param bool allow_none: Флаг допустимости None
        :rtype:                 bool
        """
        if data is None:
            if allow_none:
                return None
            else:
                cls.error(cls.TPL_BOOL_NONE % arg)
        if smart and isinstance(data, str):
            return data.lower() not in cls.BOOL_CAST_TO_FALSE
        return bool(data)
