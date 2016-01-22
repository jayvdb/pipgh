import unittest

import pipgh


class TestSearch(unittest.TestCase):

    def test_cli_fails(self):
        # search <query>...
        argvs = [
            ['install', 'requests'],
            ['search'],
        ]
        auth_flag = None
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.search, auth_flag, argv)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise

    def test_execution(self):
        argv = ['search', 'docopt/docopt']
        total_count, lines = pipgh.search(True, argv, output=False)
        self.assertGreaterEqual(total_count, len(lines))
