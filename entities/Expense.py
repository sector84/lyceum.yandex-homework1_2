from datetime import datetime

from core.base import (
    BaseList,
    BaseItem,
)
from core.engine import (
    GLog,
    create_sqlite_driver,
)


class Expense(BaseItem):
    """Расход.

    :param list|dict data:  Данные для инициализации
    """

    MAPPING_JSON = {
        # self_name -> json_name
        'ID': "id",
        'date': "date",
        'value': "value",
        'note': "note",
    }
    ERR_PREFIX = 'Ошибка работы с расходом'

    def toDict(self) -> dict:
        """Правильное представление для сериализации в JSON через ujson."""
        return {
            'id': self.ID,
            'date': self.date,
            'value': self.value,
            'note': self.note,
        }

    def _check(self):
        """Проверка данных"""
        if 'id' in self:
            self.ID = self['id']
        self.date = self['date']
        self.value = self['value']
        self.note = self['note']

    def _create(self):
        """."""
        GLog.debug('Вставка расхода в БД')
        self.ID = self.db().execute('''
            INSERT INTO "expenses" (
                "date", "value", "note"
            ) VALUES (?, ?, ?);
        ''', [
            self.date, self.value, self.note
        ], with_result=True)

    def _update(self):
        """."""
        GLog.debug('Изменениее расхода в БД')
        self.db().execute('''
            UPDATE "expenses" SET 
                "date" = ?,
                "value" = ?,
                "note" = ?
            WHERE "id" = ?;
        ''', [
            self.date, self.value, self.note, self.ID
        ])

    def _delete(self):
        """."""
        GLog.debug('Удаление расхода из БД')
        self.db().execute('''
            DELETE FROM "expenses"
            WHERE "id" = ?;
        ''', [
            self.ID
        ])

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, new_one):
        self['id'] = self.check_int(new_one, 'Идентификатор расхода')

    @property
    def date(self):
        # возвращаем в человеко-читаемом виде вместо unix timestamp
        return datetime.utcfromtimestamp(self['date']).strftime('%Y-%m-%d %H:%M:%S')

    @date.setter
    def date(self, new_one):
        # todo: привести к unix timestamp
        self['date'] = self.check_int(new_one, 'Дата расхода')

    @property
    def value(self):
        return self['value']

    @value.setter
    def value(self, new_one):
        self['value'] = self.check_float(new_one, 'Значение расхода')

    @property
    def note(self):
        return self['note']

    @note.setter
    def note(self, new_one):
        self['note'] = self.check_str(new_one, 'Примечание по расходу')

    @classmethod
    def create(cls, data: dict) -> BaseItem:
        """Создание расхода.

        :param data:     данные по расходу
        :rtype: entities.Expense
        """
        GLog.info('Создание расхода')
        res = Expense().load_from_json(data)
        res._create()
        return res

    @classmethod
    def edit(cls, expense_id: int, data: dict) -> BaseItem:
        """Изменение расхода.

        :param expense_id:       идентификатор расхода
        :param data:     данные расхода
        :rtype: entities.Expense
        """
        GLog.info('Изменение расхода')
        data.update({'id': expense_id})
        res = Expense().load_from_json(data)
        res._update()
        return res

    @classmethod
    def delete(cls, expense_id: int):
        """Удаление расхода.

        :param expense_id:   идентификатор расхода
        :rtype: None
        """
        GLog.info('Удаление расхода')
        res = Expense().load_from_json({'id': expense_id})
        res._delete()


class Expenses(BaseList):
    """Список расходов.

    :param list data:   Данные для инициализации
    """

    ERR_PREFIX = 'Ошибка работы со списком расходов'

    @classmethod
    def list(cls) -> BaseList:
        """Список расходов.

        :rtype entities.Users
        """
        GLog.info('Запрос списка расходов')

        db = create_sqlite_driver()
        sql = 'SELECT * FROM "expenses" ORDER BY "date" DESC;'
        args = []
        return db.select(sql, args, list_type=cls, item_type=Expense)
