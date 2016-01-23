import unittest

import pipgh


class TestInstall(unittest.TestCase):

    def test_cli_fail(self):
        # install (<full_name> | -r <requirements.txt>)
        argvs = [
            ['install'],
            ['instal', 'docopt/docopt'],
            ['install', '-r'],
            ['install', '-r', 'reqs.txt', 'docopt/docopt'],
        ]
        auth_flag = None
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.install, auth_flag, argv)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise
