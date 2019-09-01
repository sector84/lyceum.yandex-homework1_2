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
        'login': "login",
        'password': "password",
        'name': "name",
        'is_admin': 'is_admin',
    }
    ERR_PREFIX = 'Ошибка работы с пользователем'

    def toDict(self) -> dict:
        """Правильное представление для сериализации в JSON через ujson."""
        return {
            'id': self.ID,
            'login': self.login,
            'name': self.name,
            'password': self.password,
            'is_admin': self.is_admin,
        }

    def _check(self):
        """Проверка данных"""
        if 'id' in self:
            self.ID = self['id']
        self.login = self['login']
        self.password = self['password']
        self.name = self['name']
        self.is_admin = self['is_admin']

    def _create(self):
        """."""
        GLog.debug('Вставка пользователя в БД')
        passw = self.check_str(self.password, arg='Пароль пользователя')
        passw = sha256(passw.encode('utf-8')).hexdigest()
        self.ID = self.db().execute('''
            INSERT INTO "users" (
                "login", "passw", "name", "is_admin"
            ) VALUES (?, ?, ?, ?);
        ''', [
            self.login, passw, self.name, self.is_admin
        ], with_result=True)

    def _update(self):
        """."""
        GLog.debug('Изменениее пользователя в БД')
        passw = self.check_str(self.passw, arg='Пароль пользователя')
        passw = sha256(passw.encode('utf-8')).hexdigest()
        self.db().execute('''
            UPDATE "users" SET 
                "login" = ?,
                "passw" = ?,
                "name" = ?,
                "is_admin" = ?
            WHERE "id" = ?;
        ''', [
            self.login, passw, self.name, self.is_admin, self.ID
        ])

    def _delete(self):
        """."""
        GLog.debug('Удаление пользователя из БД')
        self.db().execute('''
            DELETE FROM "users"
            WHERE "id" = ?;
        ''', [
            self.ID
        ])

    @property
    def admin(self):
        return self['is_admin'] > 0

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, new_one):
        self['id'] = self.check_int(new_one, 'Идентификатор пользователя')

    @property
    def is_admin(self):
        return self['is_admin']

    @is_admin.setter
    def is_admin(self, new_one):
        self['is_admin'] = self.check_int(new_one, 'Флаг администратора')

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
    def select_by_credentials(cls, login: str, password: str) -> BaseItem:
        """Создание пользователя.

        :param login:       логин пользователя
        :param password:    пароль пользователя
        :rtype: entities.User
        """
        GLog.info('Выборка пользователя по логину/паролю')
        password = cls.check_str(password, arg='Пароль пользователя')
        password = sha256(password.encode('utf-8')).hexdigest()
        db = create_sqlite_driver()
        sql = '''
            SELECT * FROM "users" 
            WHERE "login" = ? AND "passw" = ?;
        '''
        args = [login, password]
        return db.select(sql, args, one_row=True, item_type=User)

    @classmethod
    def create(cls, role_id: int, data: dict) -> BaseItem:
        """Создание пользователя.

        :param role_id:  идентификатор роли пользователя
        :param data:     данные пользователя
        :rtype: entities.User
        """
        GLog.info('Создание пользователя')
        data.update({'role_id': role_id})
        res = User().load_from_json(data)
        res._create()
        return res

    @classmethod
    def edit(cls, user_id: int, data: dict) -> BaseItem:
        """Изменение пользователя.

        :param user_id:       идентификатор пользователя
        :param data:     данные пользователя
        :rtype: entities.User
        """
        GLog.info('Изменение пользователя')
        data.update({'id': user_id})
        res = User().load_from_json(data)
        res._update()
        return res

    @classmethod
    def delete(cls, user_id: int):
        """Удаление пользователя.

        :param user_id:   идентификатор пользователя
        :rtype: None
        """
        GLog.info('Удаление пользователя')
        res = User().load_from_json({'id': user_id})
        res._delete()


class Users(BaseList):
    """Список пользователей.

    :param list data:   Данные для инициализации
    """

    ERR_PREFIX = 'Ошибка работы со списком пользователей'

    @classmethod
    async def list(cls) -> BaseList:
        """Список пользователей.

        :rtype entities.Users
        """
        GLog.info('Запрос списка пользователей')

        db = create_sqlite_driver()
        sql = 'SELECT * FROM "users";'
        args = []
        return db.select(sql, args, list_type=cls, item_type=User)
