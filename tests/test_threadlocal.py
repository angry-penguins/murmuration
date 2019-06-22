from concurrent.futures import ThreadPoolExecutor
from unittest import TestCase
from murmuration.aws import threadlocal_var


__all__ = [
    'ThreadLocalCase',
]


class ThreadLocalCase(TestCase):

    def test_simple(self):
        """ Can we set a value unseen from another thread? """
        bert = 'bert'

        def set_value():
            x = threadlocal_var('foo', dict)
            x['bar'] = bert

        def get_value():
            return threadlocal_var('foo', dict).get('bar')

        set_value()

        with ThreadPoolExecutor(max_workers=1) as pool:
            result = pool.submit(get_value)

        self.assertEqual(get_value(), bert)
        self.assertEqual(result.result(), None)

    def test_simple_default(self):
        """ Can we set a value in our factory? """

        bert = 'berty'

        def get_default_value():
            return threadlocal_var('foo', dict, bar=bert).get('bar')

        with ThreadPoolExecutor(max_workers=1) as pool:
            result = pool.submit(get_default_value)

        self.assertEqual(result.result(), bert)
