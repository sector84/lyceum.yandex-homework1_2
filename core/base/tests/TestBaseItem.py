from core.base import BaseItem
from core.engine import (
    Checks,
    UnitTest,
)


class TestBaseItem(UnitTest):
    """."""

    def test___init__(self):
        """."""
        item = BaseItem()
        self.assertIsInstance(item, dict)
        self.assertIsInstance(item, Checks)
        self.assertTrue(hasattr(item, 'db'))
        self.assertTrue(hasattr(item, 'load_from_json'))

        item = BaseItem({'ololo': 1})
        self.assertDictEqual(item, {'ololo': 1})

        item = BaseItem(ololo=1)
        self.assertDictEqual(item, {'ololo': 1})

        item = BaseItem([('ololo', 1), ('test', 'purpur')])
        self.assertDictEqual(item, {'ololo': 1, 'test': 'purpur'})
