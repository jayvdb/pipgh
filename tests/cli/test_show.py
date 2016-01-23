import unittest

import pipgh


class TestShow(unittest.TestCase):

    def test_cli_fails(self):
        # show <full_name>
        argvs = [
            ['sho', 'requests'],
            ['show'],
        ]
        auth_flag = None
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.show, auth_flag, argv)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise
