from collections import deque

from core.base import BaseList
from core.engine import (
    Checks,
    UnitTest,
)


class TestBaseList(UnitTest):
    """."""

    def test___init__(self):
        """."""
        item = BaseList()
        self.assertIsInstance(item, deque)
        self.assertIsInstance(item, Checks)
        self.assertTrue(hasattr(item, 'db'))

        item = BaseList(range(0, 3))
        self.assertListEqual(list(item), [0, 1, 2])

        item = BaseList([('ololo', 1), ('test', 'purpur')])
        self.assertListEqual(list(item), [('ololo', 1), ('test', 'purpur')])
