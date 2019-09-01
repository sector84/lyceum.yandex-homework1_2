from hashlib import sha256

from core.base import (
    BaseList,
    BaseItem,
)
from core.engine import (
    GLog,
    create_sqlite_driver,
)


class User(BaseItem):
    """Пользователь.

    :param list|dict data:  Данные для инициализации
    """

    MAPPING_JSON = {
        # self_name -> json_name
        'ID': "id",
        'role_id': "role_id",
        'role_name': "role_name",
        'login': "login",
        'name': "name",
    }
    ERR_PREFIX = 'Ошибка работы с пользователем'

    def toDict(self) -> dict:
        """Правильное представление для сериализации в JSON через ujson."""
        return {
            'id': self.ID,
            'role_id': self.role_id,
            'role_name': self.role_name,
            'login': self.login,
            'name': self.name,
        }

    def _check(self):
        """Проверка данных"""
        if 'id' in self:
            self.ID = self['id']
        self.role_id = self['role_id']
        self.role_name = self['role_name']
        self.login = self['login']
        self.name = self['name']
        self.passw = ''

    def _create(self):
        """."""
        GLog.debug('Вставка пользователя в БД')
        passw = self.check_str(self.passw, arg='Пароль пользователя')
        passw = sha256(passw.encode('utf-8')).hexdigest()
        self.ID = self.db().execute('''
            INSERT INTO "users" (
                "id_role", "login", "passw", "name"
            ) VALUES ($1, $2, $3, $4)
            RETURNING "id";
        ''', [
            self.role_id, self.login, passw, self.name
        ], with_result=True)

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, new_one):
        self['id'] = self.check_int(new_one, 'Идентификатор пользователя')

    @property
    def role_id(self):
        return self['role_id']

    @role_id.setter
    def role_id(self, new_one):
        self['role_id'] = self.check_int(new_one, 'Идентификатор роли')

    @property
    def role_name(self):
        return self['role_name']

    @role_name.setter
    def role_name(self, new_one):
        self['role_name'] = self.check_str(new_one, 'Имя роли')

    @property
    def login(self):
        return self['login']

    @login.setter
    def login(self, new_one):
        self['login'] = self.check_str(new_one, 'Логин пользователя')

    @property
    def name(self):
        return self['name']

    @name.setter
    def name(self, new_one):
        self['name'] = self.check_str(new_one, arg='Имя пользователя', allow_empty=True)

    @classmethod
    def create(cls, role_id: int, data: dict) -> BaseItem:
        """Создание проекта.

        :param role_id: идентификатор роли пользователя
        :param data:     данные проекта
        :rtype: entities.Project
        """
        GLog.info('Создание пользователя')
        data.update({'role_id': role_id})
        res = User().load_from_json(data)
        res._create()
        return res


class Projects(BaseList):
    """Список пользователей.

    :param list data:   Данные для инициализации
    """

    ERR_PREFIX = 'Ошибка работы со списком пользователей'

    @classmethod
    async def list(cls, role_id: int, include: list = None) -> BaseList:
        """Список проектов.

        :param role_id:     Идентификатор роли пользователя (0 - все пользователи)
        :param include:     Доп. параметры ответа
        :rtype entities.Projects
        """
        GLog.info('Запрос списка пользователей')

        include = include or []
        args = [role_id]
        GLog.debug('Запрос пользователей: include=%s args=%s', include, args)

        db = create_sqlite_driver()
        if role_id == 0:
            sql = 'SELECT * FROM "users";'
            args = []
        else:
            sql = 'SELECT * FROM "projects" WHERE id_role = $1;'
        return db.select(sql, args, list_type=cls, item_type=User)
