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
        # pipgh [--auth] install (...)
        # pipgh [-h | --help]
        argvs = [
            ['unknown_command'],
            ['--auth'],
            ['--auth', 'searched'],
            ['--aut', 'search'],
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
        argvs = [
            (['search'],            ('search', False, ['search'])),
            (['--auth', 'search'],  ('search', True, ['search'])),
            (['show'],              ('show', False, ['show'])),
            (['--auth', 'show'],    ('show', True, ['show'])),
            (['install'],           ('install', False, ['install'])),
            (['--auth', 'install'], ('install', True, ['install'])),
        ]
        for argv, ref in argvs:
            rst = pipgh.main(argv, dry_run=True)
            self.assertEqual(rst, ref)
