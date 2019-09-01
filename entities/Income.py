from datetime import datetime

from core.base import (
    BaseList,
    BaseItem,
)
from core.engine import (
    GLog,
    create_sqlite_driver,
)


class Income(BaseItem):
    """Доход.

    :param list|dict data:  Данные для инициализации
    """

    MAPPING_JSON = {
        # self_name -> json_name
        'ID': "id",
        'date': "date",
        'value': "value",
        'note': "note",
    }
    ERR_PREFIX = 'Ошибка работы с доходом'

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
        GLog.debug('Вставка дохода в БД')
        self.ID = self.db().execute('''
            INSERT INTO "incomes" (
                "date", "value", "note"
            ) VALUES (?, ?, ?);
        ''', [
            self.date, self.value, self.note
        ], with_result=True)

    def _update(self):
        """."""
        GLog.debug('Изменениее дохода в БД')
        self.db().execute('''
            UPDATE "incomes" SET 
                "date" = ?,
                "value" = ?,
                "note" = ?
            WHERE "id" = ?;
        ''', [
            self.date, self.value, self.note, self.ID
        ])

    def _delete(self):
        """."""
        GLog.debug('Удаление дохода из БД')
        self.db().execute('''
            DELETE FROM "incomes"
            WHERE "id" = ?;
        ''', [
            self.ID
        ])

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, new_one):
        self['id'] = self.check_int(new_one, 'Идентификатор дохода')

    @property
    def date(self):
        return datetime.utcfromtimestamp(self['date']).strftime('%Y-%m-%d %H:%M:%S')

    @date.setter
    def date(self, new_one):
        # todo: привести к unix timestamp
        self['date'] = self.check_int(new_one, 'Дата дохода')

    @property
    def value(self):
        return self['value']

    @value.setter
    def value(self, new_one):
        self['value'] = self.check_float(new_one, 'Значение дохода')

    @property
    def note(self):
        return self['note']

    @note.setter
    def note(self, new_one):
        self['note'] = self.check_str(new_one, 'Примечание по доходу')

    @classmethod
    def create(cls, data: dict) -> BaseItem:
        """Создание дохода.

        :param data:     данные по доходу
        :rtype: entities.Income
        """
        GLog.info('Создание дохода')
        res = Income().load_from_json(data)
        res._create()
        return res

    @classmethod
    def edit(cls, income_id: int, data: dict) -> BaseItem:
        """Изменение дохода.

        :param income_id:  идентификатор дохода
        :param data:       данные дохода
        :rtype: entities.Income
        """
        GLog.info('Изменение дохода')
        data.update({'id': income_id})
        res = Income().load_from_json(data)
        res._update()
        return res

    @classmethod
    def delete(cls, expense_id: int):
        """Удаление дохода.

        :param expense_id:   идентификатор дохода
        :rtype: None
        """
        GLog.info('Удаление дохода')
        res = Income().load_from_json({'id': expense_id})
        res._delete()


class Incomes(BaseList):
    """Список доходов.

    :param list data:   Данные для инициализации
    """

    ERR_PREFIX = 'Ошибка работы со списком доходов'

    @classmethod
    def list(cls) -> BaseList:
        """Список доходов.

        :rtype entities.Incomes
        """
        GLog.info('Запрос списка доходов')

        db = create_sqlite_driver()
        sql = 'SELECT * FROM "incomes" ORDER BY "date" DESC;'
        args = []
        return db.select(sql, args, list_type=cls, item_type=Income)
