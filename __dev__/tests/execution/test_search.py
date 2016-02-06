import unittest

import pipgh


class TestSearch(unittest.TestCase):

    def test_execution(self):
        argv = ['search', 'docopt/docopt']
        total_count, lines = pipgh.search(True, argv, output=False)
        self.assertGreaterEqual(total_count, len(lines))
