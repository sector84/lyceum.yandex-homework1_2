class Error(Exception):
    """Базовый класс ошибки."""

    DEFAULT_MESSAGE = 'Неизвестная ошибка.'

    CODE_UNKNOWN = 0
    CODE_UNAUTHORIZED = 401

    def __init__(
            self, message: str = None, code=None, data=None
    ):
        """Инициализация собственных параметров."""
        Exception.__init__(self)
        self.data = data
        self.code = code or self.CODE_UNKNOWN
        self.message = message or self.DEFAULT_MESSAGE

    def to_http(self) -> dict:
        """Правильное представление для сериализации в HTTP."""
        return {
            "data": self
        }

    def to_dict(self) -> dict:
        """Правильное представление для сериализации в JSON."""
        return {
            'code': self.code,
            'name': self.message,
            'descr': self.data,
        }

    # поможем ujson правильно сериализовать ошибку
    toDict = to_dict

    def __str__(self) -> str:
        """Сериализация для принта в логи."""
        return "[%s] %s" % (self.code, self.message)


class Errors:
    """Базовый интерфейс подсистемы обработки ошибок."""

    ERR_PREFIX = 'Ошибка'

    @classmethod
    def error(
            cls, msg: str, prefix: str = None, code=None, data=None
    ):
        """Основная функция безусловного вызова ошибки.

        :param str msg:     Человекопонятное сообщение об ошибке
        :param int code:    Код ошибки из констант
        :param object data: Объект данных об ошибке
        :param str prefix:  Строка префикса текста сообщения
        """
        message = '%s: %s' % (prefix or cls.ERR_PREFIX, msg)
        raise Error(message, code, data)

    @classmethod
    def expect(
            cls, cond: object, msg: str, prefix: str = None, code=None, data=None
    ) -> object:
        """Хелпер проверки условия для более краткого райза ошибок.

        Используется, когда нужна ошибка при невыполнении условия::

            self.expect(len(_code) > 0, msg="Код не должен быть пустым")

        Это можно прочитать так: Я ожидаю, что длина кода будет больше
        нуля, иначе это ошибка с текстом "Код не должен быть пустым"

        :param bool cond:   Условие, которое должно быть выполнено
        :param str msg:     Человекопонятное сообщение об ошибке
        :param int code:    Код ошибки из констант
        :param object data: Объект данных об ошибке
        :param str prefix:  Строка префикса текста сообщения
        :rtype:             typeof(cond)
        """
        return cond or cls.error(msg, prefix, code, data)
