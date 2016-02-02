from __future__ import print_function
import unittest

import pipgh


class TestShow(unittest.TestCase):

    def test_cli_usage(self):
        usage = 'pipgh [--auth] show [--<key>...] <full_name>'
        self.assertTrue(usage in pipgh.__doc__)
        try:
            pipgh.show(False, ['hello', 'arg'])
        except SystemExit as e:
            self.assertTrue(usage in e.args[0])

    def test_cli_fails(self):
        # show <full_name>
        # show [--<key>...] <full_name>
        argvs = [
            ['show'],
            ['sho', 'requests'],
            ['sho', '-clone-url', 'requests'],
            ['show', '-clone-url', 'requests'],
            ['show', '--full-name', '-clone-url', 'requests'],
            ['show', '--full-name', '-clone-url', '--lone-url', 'requests'],
        ]
        auth_flag = None
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.show, auth_flag, argv)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise
