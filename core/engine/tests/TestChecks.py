from core.engine import (
    Checks,
    UnitTest
)


class TestChecks(UnitTest):
    """."""

    def test_check_str(self):
        """."""
        arg = 'какой-то параметр'
        check_str = Checks.check_str

        tpl = Checks.TPL_STR_NONE
        self.assertIsNone(check_str(None, arg, allow_none=True))
        with self.assertError(tpl % arg):
            check_str(None, arg, allow_none=False)
        with self.assertError(tpl % arg):
            check_str(None, arg)

        tpl = Checks.TPL_STR_EMPTY
        self.assertEqual('', check_str('', arg, allow_empty=True))
        with self.assertError(tpl % arg):
            check_str('', arg, allow_empty=False)
        with self.assertError(tpl % arg):
            check_str('', arg)

        tpl = Checks.TPL_STR_ERR
        for value in [1, {1}, [1], object(), str, Checks, True]:
            with self.assertError(tpl % arg):
                check_str(value, arg)

        self.assertEqual(check_str('ololo', arg), 'ololo')

    def test_check_int(self):
        """."""
        arg = 'какой-то параметр'
        check_int = Checks.check_int

        tpl = Checks.TPL_INT_NONE
        self.assertIsNone(check_int(None, arg, allow_none=True))
        with self.assertError(tpl % arg):
            check_int(None, arg, allow_none=False)
        with self.assertError(tpl % arg):
            check_int(None, arg)

        tpl = Checks.TPL_INT_NEGATIVE
        self.assertEqual(-12, check_int(-12, arg, allow_negative=True))
        with self.assertError(tpl % arg):
            check_int(-12, arg, allow_negative=False)
        with self.assertError(tpl % arg):
            check_int(-12, arg)

        tpl = Checks.TPL_INT_ERR
        for value in [{1}, [1], object(), str, Checks, 'True']:
            with self.assertError(tpl % arg):
                check_int(value, arg)

        self.assertEqual(check_int(100.500, arg), 100)
        self.assertEqual(check_int(100500, arg), 100500)
        self.assertEqual(check_int('100500', arg), 100500)
        self.assertEqual(check_int('-15', arg, allow_negative=True), -15)

    def test_check_float(self):
        """."""
        arg = 'какой-то параметр'
        check_float = Checks.check_float

        tpl = Checks.TPL_FLOAT_NONE
        self.assertIsNone(check_float(None, arg, allow_none=True))
        with self.assertError(tpl % arg):
            check_float(None, arg, allow_none=False)
        with self.assertError(tpl % arg):
            check_float(None, arg)

        tpl = Checks.TPL_FLOAT_NEGATIVE
        self.assertEqual(-12.5, check_float(-12.5, arg, allow_negative=True))
        with self.assertError(tpl % arg):
            check_float(-12.5, arg, allow_negative=False)
        with self.assertError(tpl % arg):
            check_float(-12.5, arg)

        tpl = Checks.TPL_FLOAT_ERR
        for value in [{1}, [1], object(), str, Checks, 'True']:
            with self.assertError(tpl % arg):
                check_float(value, arg)

        self.assertEqual(check_float(100.500, arg), 100.5)
        self.assertEqual(check_float('100.500', arg), 100.5)
        self.assertEqual(check_float('-1.1', arg, allow_negative=True), -1.1)

    def test_check_bool(self):
        """."""
        arg = 'какой-то параметр'
        check_bool = Checks.check_bool

        tpl = Checks.TPL_BOOL_NONE
        self.assertIsNone(check_bool(None, arg, allow_none=True))
        with self.assertError(tpl % arg):
            check_bool(None, arg, allow_none=False)
        with self.assertError(tpl % arg):
            check_bool(None, arg)

        for value in [[], {}, {1}, [1], object(), str, Checks, 'True']:
            self.assertEqual(bool(value), check_bool(value, arg))

        for value in ['0', 'false', 'no', 'n', 'нет', 'н', 'off']:
            self.assertFalse(check_bool(value, arg))
            self.assertTrue(check_bool(value, arg, smart=False))

        self.assertTrue(check_bool(True, arg))
        self.assertFalse(check_bool('False', arg))
