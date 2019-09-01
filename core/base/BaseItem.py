import ujson
from core.engine import (
    Checks,
    SqliteDriver,
    create_sqlite_driver
)


class BaseItem(dict, Checks):
    """Базовый класс для сущностей.

    :param list[tuple]|dict data: Значения для инициализации
    """
    MAPPING_JSON = {}
    _db = None

    def db(self) -> SqliteDriver:
        """Получение объекта подключения к БД."""
        if self._db is None:
            self._db = create_sqlite_driver()
        return self._db

    def load_from_json(self, data):
        """Загрузка полей сущности из данных (json|dict)."""
        if not isinstance(data, dict):
            try:
                data = ujson.loads(data)
            except Exception as e:
                err = 'Ошибка загрузки данных из JSON: %s' % str(e)
                self.error(err)

        for self_name, data_name in self.MAPPING_JSON.items():
            if data_name not in data:
                continue

            _item = self
            _item.__setattr__(self_name, data[data_name])
        return self
