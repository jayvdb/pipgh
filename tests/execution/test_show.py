import unittest

import pipgh


class TestShow(unittest.TestCase):

    def test_execution(self):
        argv = ['show', 'docopt/docopt']
        response, readme = pipgh.show(True, argv, output=False)
        self.assertGreaterEqual(response['full_name'], argv[1])
