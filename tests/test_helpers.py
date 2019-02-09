from unittest import TestCase
from murmuration.helpers import as_bytes
from murmuration.helpers import b64_str
from murmuration.helpers import from_b64_str
from murmuration.helpers import prefix_alias


__all__ = [
    'Helpers',
]


class Helpers(TestCase):
    def test_as_bytes(self):
        st = 'hello'
        b = as_bytes(st)
        self.assertIsInstance(b, bytes)
        self.assertEqual(b, b'hello')

        st = b'hello'
        b = as_bytes(st)
        self.assertEqual(b, st)

    def test_b64_str(self):
        st = 'hello'
        b = b64_str(st)
        self.assertIsInstance(b, str)
        b = from_b64_str(b)
        self.assertIsInstance(b, bytes)
        self.assertEqual(b'hello', b)

    def test_prefix_alias(self):
        alias = 'dev'
        k = prefix_alias(alias)
        self.assertEqual('alias/dev', k)
        alias = 'alias/dev'
        k = prefix_alias(alias)
        self.assertEqual('alias/dev', k)
