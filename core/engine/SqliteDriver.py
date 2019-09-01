import sqlite3
import ujson

from core.engine import (
    config,
    SqliteDrvSingleton,
    Errors,
    Error,
    GLog
)


class SqliteDriver(Errors, metaclass=SqliteDrvSingleton):
    """Класс для удобной работы с Sqlite."""

    ERR_PREFIX = 'Ошибка работы с БД'

    def __init__(self, *, db_name: str = 'postgres'):
        self.db_name = db_name
        self._connection = None
        self._cursor = None

    def init_driver(self, database):
        """Инициализация подключения, курсора и всякое это вот"""
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()


    def close(self):
        """Закрытие подключения."""
        if self._connection:
            self._connection.close()

    @property
    def driver_exists(self):
        return self._connection is not None

    def catch(self, error: Exception, text: str):
        """Перехват и обработка ошибки запроса."""
        error_str = str(error)
        query_str = text
        GLog.error(
            'Ошибка запроса:\n%s\n\tПричина: %s', query_str, error_str,
        )
        msg = 'ошибка синтаксиса или данных'
        self.error('%s (%s)' % (msg, error_str))

    def select(
            self, text: str, args: list = None, one_row: bool = False,
            list_type: object = None, item_type: object = None
    ):
        """Хелпер для выполнения запросов выборки данных.

        :param str text:        Текст запроса с подстановками из args
        :param list args:       Список со значениями параметров
        :param bool one_row:    Указывает, что нужна только первая строка
        :param object list_type: Тип списка, в который будет идти загрузка
        :param object item_type: Тип элемента, в который будет идти загрузка
        """
        list_type = list_type or list
        item_type = item_type or dict
        if args is None:
            args = []

        try:
            if one_row:
                self._cursor.execute(text, args)
                row = self.expect(self._cursor.fetchone(), msg='', code=404)
                return item_type({k: row[k] for k in row.keys()})

            result = list_type()
            for row in self._cursor.execute(text, args):
                result.append(item_type(row))
            return result
            # todo: добавить возможность выборки через генератор
        except Error as e:
            raise e
        except sqlite3.Error as error:
            self.catch(error, text)
        except Exception as error:
            self.catch(error, text)

    def execute(self, text: str, args: list = None,
                many: bool = False, with_result: bool = False):
        """Хелпер для выполнения всех запросов, кроме select.

        :param text:        Текст запроса с подстановками из args
        :param args:        Список со значениями параметров
        :param many:        Флаг, определяющий множественную вставку
        :param with_result: Флаг, возвращать ли результат выполнения запроса
        """
        if args is None:
            args = []
        try:
            # Выполняем запрос
            if many:
                self._cursor.executemany(text, args)
                self._connection.commit()
            else:
                self._cursor.execute(text, args)
                self._connection.commit()
                if with_result:
                    return self._cursor.lastrowid
        except sqlite3.Error as error:
            self.catch(error, text)
        except Exception as error:
            self.catch(error, text)


def create_sqlite_driver(database: str = None) -> SqliteDriver:
    """Создать экземпляр класса драйвера работы с Sqlite.

    :return: Экземпляр класса Sqlite
    """
    database = database or config.DB_CONF['dbname']
    result = SqliteDriver(db_name=database)
    if not result.driver_exists:
        result.init_driver(database)
    return result


def close_sqlite_drivers():
    """Закрыть все подключения к Sqlite."""
    for instance in SqliteDriver._instances.values():
        instance.close()
    SqliteDriver._instances.clear()
