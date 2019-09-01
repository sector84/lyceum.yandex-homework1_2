class SqliteDrvSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        db_name = kwargs.get('db_name')
        if not db_name:
            raise Exception('Ошибка инициализации SqliteDrvSingleton')
        # классически мы складируем в переменную класса объекты по классу
        # здесь реализован частный случай - будем складировать по имени
        # целевой БД - поэтому и класс не абстрактный Singleton,
        # а уточненный SqliteDrvSingleton
        if db_name not in cls._instances:
            cls._instances[db_name] = super(SqliteDrvSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[db_name]
        # if cls not in cls._instances:
        #     cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # return cls._instances[cls]
