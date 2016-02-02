import unittest

import pipgh


class TestInstall(unittest.TestCase):

    def test_cli_fail(self):
        # install ( (<full_name> [ref]) | (-r <requirements.txt>) )'
        argvs = [
            ['instal'],
            ['install'],
            ['instal', 'docopt/docopt'],
            ['install', '-r'],
            ['install', '-r', 'reqs.txt', 'docopt/docopt'],
            ['install', 'docopt', 'reqs.txt', 'docopt/docopt'],
        ]
        auth_flag = False
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.install, auth_flag, argv)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise
        try:
            argv = ['install', 'docopt/docopt']
            self.assertRaises(SystemExit, pipgh.install, True, argv)
        except AssertionError as e:
            e.args = (e.args[0] + ' for auth_flag=True',)
            raise

    def test_dry_run(self):
        # pipgh install <full_name>             2
        # pipgh install <full_name> <ref>       3
        # pipgh install -r <requirements.txt>   3
        argvs = [
            (['install', 'requests'],
             ['requests'],
             [None]),
            (['install', 'requests', 'special'],
             ['requests'],
             ['special']),
            (['install', '-r', 'tests/execution/requirements.txt'],
             ['docopt/docopt', 'mitsuhiko/flask', 'tornadoweb/tornado', 'kennethreitz/requests'],
             ['0.6.2', '23cf923c7c2e4a3808e6c71b6faa34d1749d4cb6', 'stable', None]),
        ]
        for argv, repo_labels, refs in argvs:
            rst = pipgh.install(False, argv, dry_run=True)
            self.assertEqual(rst, (repo_labels, refs))

