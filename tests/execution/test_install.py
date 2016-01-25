import unittest
import subprocess

import pipgh


class TestInstall(unittest.TestCase):

    def test_execution(self):
        argv = ['install', 'docopt/docopt']
        pipgh.install(False, argv, dry_run=False, output=False)
        rst = subprocess.check_output(['pip', 'freeze'], stderr=subprocess.PIPE)
        self.assertTrue(any(l.startswith(u'docopt'.encode('utf-8'))
                            for l in rst.split()))

