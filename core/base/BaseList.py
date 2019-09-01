from collections import deque

from core.engine import (
    Checks,
    SqliteDriver,
    create_sqlite_driver
)


class BaseList(deque, Checks):
    """Базовый класс для списка сущностей.

    :param list data: Значения для инициализации
    """

    _db = None

    def db(self) -> SqliteDriver:
        """Получение объекта подключения к БД."""
        if self._db is None:
            self._db = create_sqlite_driver()
        return self._db

    # todo: при необходимости добавить метод load_from_json(self, data):
