import unittest

import pipgh


class TestMain(unittest.TestCase):

    def test_init_doc(self):
        doc = pipgh.__doc__
        self.assertTrue(doc != None)
        self.assertTrue('Usage:' in doc)
        self.assertTrue('Commands:' in doc)
        self.assertTrue('Options:' in doc)
        self.assertTrue('Examples:' in doc)

    def test_cli_fails(self):
        # pipgh [--auth] search (...)
        # pipgh [--auth] show (...)
        # pipgh install (...)
        # pipgh [-h | --help | --version]
        argvs = [
            [],
            ['unknown_command'],
            ['--auth'],
            ['--auth', 'searched'],
            ['--aut', 'search'],
            ['--aut', 'show'],
            ['--auth', 'install'],
            ['--auth', 'install', 'docopt/docopt'],
            ['--auth', 'show'],
            ['--auth', 'search'],
            ['-h'],
            ['--help'],
            ['-help'],
            ['--h'],
            ['-v'],
            ['--version'],
        ]
        for argv in argvs:
            try:
                self.assertRaises(SystemExit, pipgh.main, argv, dry_run=True)
            except AssertionError as e:
                e.args = (e.args[0] + ' for ' + str(argv),)
                raise

    def test_dry_run(self):
        # pipgh show <full_name>                2
        # pipgh install <full_name>             2
        # pipgh search <query>...               2+
        # pipgh install <full_name> <ref>       3
        # pipgh install -r <requirements.txt>   3
        # pipgh --auth show <full_name>         3
        # pipgh --auth search <query>...        3+
        argvs = [
            (['show', 'requests'],             ('show', False, ['show', 'requests'])),
            (['install', 'requests'],          ('install', False, ['install', 'requests'])),
            (['search', 'requests'],           ('search', False, ['search', 'requests'])),
            (['install', 'requests', 'v0.1'],          ('install', False, ['install', 'requests', 'v0.1'])),
            (['install', '-r', 'reqs.txt'],          ('install', False, ['install', '-r', 'reqs.txt'])),
            (['--auth', 'show', 'requests'],   ('show', True, ['show', 'requests'])),
            (['--auth', 'search', 'requests'], ('search', True, ['search', 'requests'])),
            (['--auth', 'search', 'requests', 'http'], ('search', True, ['search', 'requests', 'http'])),
        ]
        for argv, ref in argvs:
            rst = pipgh.main(argv, dry_run=True)
            self.assertEqual(rst, ref)
