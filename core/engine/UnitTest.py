import unittest
import contextlib

from core.engine import Error


class UnitTest(unittest.TestCase):
    """Базовый класс для всех юнит-тестов фреймворка."""

    maxDiff = 4096

    @classmethod
    def setUpClass(cls):
        """."""
        # todo:
        pass

    def setUp(self):
        """."""
        # todo:
        pass

    def tearDown(self):
        """."""
        # todo:
        pass

    def shortDescription(self):
        """Функция автоматического форматирования nosetests."""
        _cls = self.__class__.__name__.replace('Test', '')
        _fnc = self._testMethodName.replace('test_', '')
        return '%s.%s' % (_cls, _fnc)

    def assertError(self, regex, status=500):
        """Функция проверки ошибки core.Error."""
        @contextlib.contextmanager
        def mgr():
            failed = True
            try:
                yield
                failed = False
            except Error as err:
                msg = 'Не совпадает сообщение об ошибке'
                self.assertRegex(str(err), regex, msg=msg)
            except Exception as exp:
                tpl = 'Ожидалась ошибка core.engine.Error, но получена %s'
                raise Exception(tpl % repr(exp))
            msg = 'Все прошло слишком гладко! Нужна ошибка с текстом "%s"'
            self.assertTrue(failed, msg=msg % regex)
        return mgr()
